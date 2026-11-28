#!/usr/bin/env bash
# Garde-fou de fin de tâche du site (Stop et SubagentStop), repris du logiciel JARVIS.
#
# - Si du travail a été fait, scripts/check.sh doit passer avant que Claude
#   puisse dire « terminé ». Sans check.sh utilisable: on bloque.
# - main n'est pas une branche de travail: travailler dessus bloque; main
#   locale en avance sur origin/main bloque; origin sans origin/main bloque.
# - Le dossier doit être un dépôt Git, et le verrou d'envoi (.githooks/pre-push)
#   doit être actif s'il existe.
# - À la fin d'un sous-agent (SubagentStop), check.sh n'est pas lancé (un agent
#   rend son travail au chef), mais les autres vérifications s'appliquent.
# - Boucle de blocages: le compte (par session et par agent) repart à zéro
#   quand tout passe ou quand Claude Code signale un nouvel arrêt
#   (stop_hook_active faux). Au 4e blocage de suite (le premier arrêt, puis la
#   3e relance), le message demande
#   d'écrire à James ce qui échoue; au-delà, la fin est permise et James est
#   averti à l'écran (systemMessage).
# Sans remote « origin », les vérifications de remote sont sautées (dépôts
# d'essai). L'entrée JSON illisible vaut stop_hook_active faux.

entree=$(cat)
lire() {  # lire <clé> : la valeur JSON en texte, vide si absente ou entrée illisible
  printf '%s' "$entree" | python3 -I -c '
import json, sys
try:
    d = json.load(sys.stdin)
    v = d.get(sys.argv[1], "") if isinstance(d, dict) else ""
except Exception:
    v = ""
print("true" if v is True else ("" if v is False or v is None else str(v)))
' "$1" 2>/dev/null
}
stop_hook_active=$(lire stop_hook_active)
session_id=$(lire session_id)
agent_id=$(lire agent_id)
evenement=$(lire hook_event_name)

racine="${CLAUDE_PROJECT_DIR:-.}"
if ! cd "$racine" 2>/dev/null; then
  echo "Dossier de projet introuvable ($racine): rien ne peut être vérifié. Refus par prudence." >&2
  exit 2
fi

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Le dossier du projet ($racine) n'est pas un dépôt Git: rien ne peut être vérifié. Refus par prudence." >&2
  exit 2
fi

problemes=()
branche=$(git symbolic-ref --short -q HEAD 2>/dev/null || echo "")
travail=$(git status --porcelain 2>/dev/null)

# 1. Les vérifications automatiques, quand du travail existe.
rien_a_verifier=0
if [ -z "$travail" ] && { [ "$branche" = "main" ] || [ -z "$branche" ]; }; then
  rien_a_verifier=1
fi
if [ "$evenement" != "SubagentStop" ] && [ "$rien_a_verifier" -eq 0 ]; then
  if [ ! -x scripts/check.sh ]; then
    problemes+=("scripts/check.sh est absent ou n'est pas exécutable: impossible de vérifier le travail. Rétablis-le avant de terminer.")
  elif ! resultat=$(scripts/check.sh 2>&1); then
    problemes+=("Les vérifications automatiques échouent (scripts/check.sh). Corrige avant de terminer, ou explique à James ce qui bloque.
---
$(printf '%s\n' "$resultat" | tail -n 40)")
  fi
fi

# 2. main n'est pas une branche de travail.
if [ "$branche" = "main" ] && [ -n "$travail" ]; then
  problemes+=("Tu travailles sur main. Crée une branche (git switch -c <nom>): main ne change que par une fusion approuvée par James.")
fi

# 3. main locale ne dépasse jamais origin/main.
if git remote get-url origin >/dev/null 2>&1; then
  if git rev-parse --verify -q refs/remotes/origin/main >/dev/null; then
    if git rev-parse --verify -q refs/heads/main >/dev/null; then
      en_avance=$(git rev-list --count origin/main..main 2>/dev/null || echo 0)
      if [ "${en_avance:-0}" -gt 0 ]; then
        problemes+=("main locale a $en_avance commit(s) que origin/main n'a pas. Remets main sur origin/main (git branch -f main origin/main, ou git reset --hard origin/main si tu es dessus) et garde le travail sur une branche.")
      fi
    fi
  else
    problemes+=("origin/main est inconnu de ce clone: lance git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*' puis git fetch origin.")
  fi
fi

# 4. Le verrou d'envoi doit être actif s'il existe.
if [ -e .githooks/pre-push ]; then
  haut=$(git rev-parse --show-toplevel 2>/dev/null)
  chemin=$(git config --get core.hooksPath 2>/dev/null || echo "")
  actif=0
  if [ -n "$chemin" ]; then
    case "$chemin" in
      /*) attendu="$chemin" ;;
      *) attendu="$haut/$chemin" ;;
    esac
    if [ "$(cd "$attendu" 2>/dev/null && pwd -P)" = "$(cd "$haut/.githooks" && pwd -P)" ]; then
      actif=1
    fi
  fi
  if [ "$actif" -ne 1 ]; then
    problemes+=("Le verrou d'envoi n'est pas actif (core.hooksPath). Lance: git config core.hooksPath .githooks.")
  elif [ ! -x .githooks/pre-push ]; then
    problemes+=("Le verrou d'envoi .githooks/pre-push n'est pas exécutable: rétablis-le (chmod +x, avec l'accord de James).")
  fi
fi

# 5. Compte des blocages de suite, par session et par agent.
compteur=""
if [ -n "$session_id" ]; then
  dossier_compte="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)/site-jarvis"
  mkdir -p "$dossier_compte" 2>/dev/null || dossier_compte="${TMPDIR:-/tmp}"
  cle=$(printf '%s-%s' "$session_id" "${agent_id:-chef}" | tr -c 'A-Za-z0-9_.-' '_')
  compteur="$dossier_compte/fin-de-tache-$cle.compteur"
fi

if [ "${#problemes[@]}" -eq 0 ]; then
  [ -n "$compteur" ] && rm -f "$compteur"
  exit 0
fi

if [ -n "$compteur" ] && [ "$stop_hook_active" = "true" ]; then
  n=$(head -c 8 "$compteur" 2>/dev/null || true)
  case "$n" in
    ''|*[!0-9]*) n=0 ;;
  esac
  n=$((10#$n + 1))
elif [ -n "$compteur" ]; then
  n=0  # nouvel arrêt (stop_hook_active faux): le compte repart à zéro
else
  n=0
fi
[ -n "$compteur" ] && printf '%s' "$n" > "$compteur"

if [ "$n" -gt 3 ]; then
  avertissement="Attention James: la tâche se termine alors que des vérifications échouent encore (après 4 blocages de suite: le premier arrêt, puis trois relances). Rien n'est prêt à fusionner."
  printf '%s\n' "$avertissement" "${problemes[@]}" >&2
  AVERTISSEMENT="$avertissement" python3 -I -c 'import json, os; print(json.dumps({"systemMessage": os.environ["AVERTISSEMENT"]}, ensure_ascii=False))'
  exit 0
fi

printf '%s\n\n' "${problemes[@]}" >&2
if [ "$n" -eq 3 ]; then
  echo "Dernier blocage: écris à James, dans ton rapport, ce qui échoue encore." >&2
fi
exit 2

#!/usr/bin/env bash
# Vérifications automatiques du site JARVIS.
# Lancées par le garde-fou de fin de tâche, par les agents avant de rendre leur travail, et par
# GitHub Actions sur chaque demande de fusion (CI=true).
#
# Python est lancé avec -I quand c'est possible : un fichier piège ne peut pas se glisser dans le
# chemin des modules.

set -u
cd "$(dirname "$0")/.." || exit 1
echec=0
etape() { echo "▶ $1"; }

etape "Dépôt Git"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "  pas un dépôt Git"; echec=1; }

etape "Documents obligatoires"
for f in CLAUDE.md docs/SITE.md docs/plan_du_site.json docs/FEUILLE_DE_ROUTE.md docs/IDEES.md docs/OFFRE.md; do
  [ -f "$f" ] || { echo "  manquant : $f"; echec=1; }
done

etape "Agents"
for a in architecte redacteur developpeur reviseur securite; do
  [ -f ".claude/agents/$a.md" ] || { echo "  agent manquant : $a"; echec=1; }
done

etape "Réglages locaux qui couperaient les garde-fous"
if [ -f .claude/settings.local.json ]; then
  python3 -I - <<'EOF' || echec=1
import json, sys
try:
    d = json.load(open(".claude/settings.local.json", encoding="utf-8"))
except Exception as e:
    print(f"  .claude/settings.local.json illisible ({e})"); sys.exit(1)
if d.get("disableAllHooks") or "hooks" in d:
    print("  .claude/settings.local.json coupe ou remplace les garde-fous : retire « disableAllHooks » et « hooks »."); sys.exit(1)
EOF
fi

etape "Secrets"
if git ls-files | grep -iqE '(^|/)(\.env(\..*)?|\.dev\.vars|wrangler\.toml|[^/]*\.pem|[^/]*\.key|\.npmrc)$'; then
  echo "  un fichier secret est suivi par Git :"; git ls-files | grep -iE '(^|/)(\.env(\..*)?|\.dev\.vars|wrangler\.toml|[^/]*\.pem|[^/]*\.key|\.npmrc)$' | grep -v '\.example$' | sed 's/^/    /'
  git ls-files | grep -iE '(^|/)(\.env(\..*)?|\.dev\.vars|wrangler\.toml|[^/]*\.pem|[^/]*\.key|\.npmrc)$' | grep -qv '\.example$' && echec=1
fi
if git grep -n -I -E 'ghp_[A-Za-z0-9]{20}|github_pat_[A-Za-z0-9_]{20}|-----BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{24}|xox[bap]-[A-Za-z0-9-]{10}' -- . ':!media' >/dev/null 2>&1; then
  echo "  un jeton ou une clé semble écrit dans le code :"
  git grep -n -I -l -E 'ghp_[A-Za-z0-9]{20}|github_pat_[A-Za-z0-9_]{20}|-----BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{24}|xox[bap]-[A-Za-z0-9-]{10}' -- . ':!media' | sed 's/^/    /'
  echec=1
fi

etape "Construction du site"
if python3 tools/build.py >/tmp/site-build.log 2>&1; then
  # En CI : les fichiers bâtis commis doivent être ceux de la source. Deux fichiers portent la date
  # du jour de la construction (le plan pour Google, et l'échéance d'exemple de la démo Environnements).
  sauf=(':!sitemap.xml' ':!solutions/environnements-intelligents/index.html')
  if [ "${CI:-}" = "true" ] && ! git diff --quiet -- . "${sauf[@]}"; then
    echo "  les fichiers bâtis ne correspondent pas à la source : lance python3 tools/build.py et commets le résultat."
    git diff --stat -- . "${sauf[@]}" | tail -n 15 | sed 's/^/    /'
    echec=1
  fi
else
  echo "  la construction échoue :"; tail -n 20 /tmp/site-build.log | sed 's/^/    /'; echec=1
fi

etape "Référencement"
python3 tools/verifier_seo.py | tail -n 5 | sed 's/^/  /'
[ "${PIPESTATUS[0]}" -eq 0 ] || echec=1

etape "Loi du site"
python3 -I scripts/verifier_site.py | sed 's/^/  /'
[ "${PIPESTATUS[0]}" -eq 0 ] || echec=1

etape "Parcours du configurateur"
if python3 -c "import playwright" 2>/dev/null; then
  serveur=""
  if ! (exec 3<>/dev/tcp/127.0.0.1/4173) 2>/dev/null; then
    python3 -m http.server 4173 >/dev/null 2>&1 &
    serveur=$!
    sleep 1
  fi
  if python3 tools/test_offre.py >/tmp/site-parcours.log 2>&1 && grep -q "tout passe" /tmp/site-parcours.log; then
    echo "  tout passe"
  else
    echo "  le parcours échoue :"; tail -n 15 /tmp/site-parcours.log | sed 's/^/    /'; echec=1
  fi
  [ -n "$serveur" ] && kill "$serveur" 2>/dev/null
else
  echo "  sauté : Playwright n'est pas installé ici"
fi

if [ "$echec" -ne 0 ]; then
  echo "✗ Des vérifications échouent."
  exit 1
fi
echo "✓ Toutes les vérifications passent."

const year = document.querySelector("#year");
const form = document.querySelector("#assistant-form");
const input = document.querySelector("#assistant-input");
const log = document.querySelector("#assistant-log");

year.textContent = new Date().getFullYear();

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const message = input.value.trim();
  if (!message) {
    input.focus();
    return;
  }

  appendEntry("James", message);
  appendEntry(
    "Jarvis",
    "Bien reçu. Pour répondre pour vrai, il faudra brancher un backend et une API. Le site est déjà prêt pour cette prochaine étape."
  );

  input.value = "";
  input.focus();
});

function appendEntry(name, text) {
  const entry = document.createElement("p");
  const speaker = document.createElement("strong");
  speaker.textContent = name;
  entry.appendChild(speaker);
  entry.append(document.createTextNode(text));
  log.appendChild(entry);
  log.scrollTop = log.scrollHeight;
}

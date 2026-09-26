const header = document.querySelector("[data-header]");
const menuToggle = document.querySelector("[data-menu-toggle]");
const navigation = document.querySelector("[data-nav]");
const solutionTabs = [...document.querySelectorAll("[data-solution]")];
const solutionStage = document.querySelector(".solution-stage");
const solutionNumber = document.querySelector("[data-solution-number]");
const solutionStatus = document.querySelector("[data-solution-status]");
const solutionLabel = document.querySelector("[data-solution-label]");
const solutionTitle = document.querySelector("[data-solution-title]");
const solutionCopy = document.querySelector("[data-solution-copy]");
const solutionExample = document.querySelector("[data-solution-example]");
const solutionResult = document.querySelector("[data-solution-result]");
const solutionVisualLabel = document.querySelector("[data-solution-visual-label]");
const ambulanceTabs = [...document.querySelectorAll("[data-ambulance-system]")];
const automationScenarios = [...document.querySelectorAll("[data-automation-scenario]")];
const automationStage = document.querySelector(".automation-scenario-stage");
const automationKicker = document.querySelector("[data-automation-kicker]");
const automationTitle = document.querySelector("[data-automation-title]");
const automationCopy = document.querySelector("[data-automation-copy]");
const automationObserve = document.querySelector("[data-automation-observe]");
const automationDecide = document.querySelector("[data-automation-decide]");
const automationAct = document.querySelector("[data-automation-act]");
const automationRecord = document.querySelector("[data-automation-record]");
const roadmapTabs = [...document.querySelectorAll("[data-roadmap-horizon]")];
const roadmapStage = document.querySelector(".roadmap-stage");
const roadmapIndex = document.querySelector("[data-roadmap-index]");
const roadmapKicker = document.querySelector("[data-roadmap-kicker]");
const roadmapTitle = document.querySelector("[data-roadmap-title]");
const roadmapCopy = document.querySelector("[data-roadmap-copy]");
const roadmapFocus = document.querySelector("[data-roadmap-focus]");
const roadmapOutcome = document.querySelector("[data-roadmap-outcome]");
const roadmapRule = document.querySelector("[data-roadmap-rule]");
const roadmapMoment = document.querySelector("[data-roadmap-moment]");
const coachTabs = [...document.querySelectorAll("[data-coach-mode]")];
const coachStage = document.querySelector(".coach-stage");
const coachKicker = document.querySelector("[data-coach-kicker]");
const coachTitle = document.querySelector("[data-coach-title]");
const coachCopy = document.querySelector("[data-coach-copy]");
const coachPrimary = document.querySelector("[data-coach-primary]");
const coachPrimaryLabel = document.querySelector("[data-coach-primary-label]");
const coachSignalOne = document.querySelector("[data-coach-signal-one]");
const coachSignalTwo = document.querySelector("[data-coach-signal-two]");
const coachSignalThree = document.querySelector("[data-coach-signal-three]");
const coachAction = document.querySelector("[data-coach-action]");
const coachReason = document.querySelector("[data-coach-reason]");
const coachSource = document.querySelector("[data-coach-source]");
const coachChoice = document.querySelector("[data-coach-choice]");
const coachChoiceLabel = document.querySelector("[data-coach-choice-label]");

const updateHeader = () => {
  header?.classList.toggle("scrolled", window.scrollY > 28);
};

menuToggle?.addEventListener("click", () => {
  const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
  menuToggle.setAttribute("aria-expanded", String(!isOpen));
  navigation?.classList.toggle("open", !isOpen);
  document.body.classList.toggle("menu-open", !isOpen);
});

navigation?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuToggle?.setAttribute("aria-expanded", "false");
    navigation.classList.remove("open");
    document.body.classList.remove("menu-open");
  });
});

window.addEventListener("scroll", updateHeader, { passive: true });
updateHeader();

const visualLabels = {
  spaces: "Lieux",
  "private-ai": "Savoir",
  security: "Sécurité",
  business: "Travail",
  network: "Réseau",
  diagnostics: "Diagnostic",
};

const selectSolution = (tab) => {
  solutionTabs.forEach((item) => {
    const isActive = item === tab;
    item.classList.toggle("active", isActive);
    item.setAttribute("aria-selected", String(isActive));
  });

  solutionStage?.classList.remove("changing");
  void solutionStage?.offsetWidth;
  solutionStage?.classList.add("changing");
  solutionStage?.setAttribute("data-active-solution", tab.dataset.solution);

  if (solutionNumber) solutionNumber.textContent = tab.dataset.number;
  if (solutionStatus) solutionStatus.textContent = tab.dataset.status;
  if (solutionLabel) solutionLabel.textContent = tab.dataset.label;
  if (solutionTitle) solutionTitle.textContent = tab.dataset.title;
  if (solutionCopy) solutionCopy.textContent = tab.dataset.copy;
  if (solutionExample) solutionExample.textContent = tab.dataset.example;
  if (solutionResult) solutionResult.textContent = tab.dataset.result;
  if (solutionVisualLabel) solutionVisualLabel.textContent = visualLabels[tab.dataset.solution] || "JARVIS";
};

solutionTabs.forEach((tab) => {
  tab.addEventListener("click", () => selectSolution(tab));
});

if (solutionTabs[0]) {
  selectSolution(solutionTabs[0]);
}

const selectAmbulanceSystem = (tab) => {
  ambulanceTabs.forEach((item) => {
    const isActive = item === tab;
    item.setAttribute("aria-expanded", String(isActive));
    item.closest(".lab-domain")?.classList.toggle("active", isActive);
  });
};

ambulanceTabs.forEach((tab) => {
  tab.addEventListener("click", () => selectAmbulanceSystem(tab));
});

if (ambulanceTabs[0]) {
  selectAmbulanceSystem(ambulanceTabs[0]);
}

const selectAutomationScenario = (scenario) => {
  automationScenarios.forEach((item) => {
    const isActive = item === scenario;
    item.classList.toggle("active", isActive);
    item.setAttribute("aria-selected", String(isActive));
  });

  automationStage?.classList.remove("changing");
  void automationStage?.offsetWidth;
  automationStage?.classList.add("changing");

  if (automationKicker) automationKicker.textContent = scenario.dataset.kicker;
  if (automationTitle) automationTitle.textContent = scenario.dataset.title;
  if (automationCopy) automationCopy.textContent = scenario.dataset.copy;
  if (automationObserve) automationObserve.textContent = scenario.dataset.observe;
  if (automationDecide) automationDecide.textContent = scenario.dataset.decide;
  if (automationAct) automationAct.textContent = scenario.dataset.act;
  if (automationRecord) automationRecord.textContent = scenario.dataset.record;
};

automationScenarios.forEach((scenario) => {
  scenario.addEventListener("click", () => selectAutomationScenario(scenario));
});

if (automationScenarios[0]) {
  selectAutomationScenario(automationScenarios[0]);
}

const selectCoachMode = (tab) => {
  coachTabs.forEach((item) => {
    const isActive = item === tab;
    item.classList.toggle("active", isActive);
    item.setAttribute("aria-selected", String(isActive));
  });

  coachStage?.classList.remove("changing");
  void coachStage?.offsetWidth;
  coachStage?.classList.add("changing");
  coachStage?.style.setProperty("--ring-a", `${tab.dataset.ringA}%`);
  coachStage?.style.setProperty("--ring-b", `${tab.dataset.ringB}%`);
  coachStage?.style.setProperty("--ring-c", `${tab.dataset.ringC}%`);

  if (coachKicker) coachKicker.textContent = tab.dataset.kicker;
  if (coachTitle) coachTitle.textContent = tab.dataset.title;
  if (coachCopy) coachCopy.textContent = tab.dataset.copy;
  if (coachPrimary) coachPrimary.textContent = tab.dataset.primary;
  if (coachPrimaryLabel) coachPrimaryLabel.textContent = tab.dataset.primaryLabel;
  if (coachSignalOne) coachSignalOne.textContent = tab.dataset.signalOne;
  if (coachSignalTwo) coachSignalTwo.textContent = tab.dataset.signalTwo;
  if (coachSignalThree) coachSignalThree.textContent = tab.dataset.signalThree;
  if (coachAction) coachAction.textContent = tab.dataset.action;
  if (coachReason) coachReason.textContent = tab.dataset.reason;
  if (coachSource) coachSource.textContent = tab.dataset.source;
  coachChoice?.setAttribute("aria-pressed", "false");
  if (coachChoiceLabel) coachChoiceLabel.textContent = "Choisir cette action";
};

coachTabs.forEach((tab) => {
  tab.addEventListener("click", () => selectCoachMode(tab));
});

if (coachTabs[0]) {
  selectCoachMode(coachTabs[0]);
}

coachChoice?.addEventListener("click", () => {
  const isChosen = coachChoice.getAttribute("aria-pressed") === "true";
  coachChoice.setAttribute("aria-pressed", String(!isChosen));
  if (coachChoiceLabel) coachChoiceLabel.textContent = isChosen ? "Choisir cette action" : "Action choisie";
});

const selectRoadmapHorizon = (tab) => {
  roadmapTabs.forEach((item) => {
    const isActive = item === tab;
    item.classList.toggle("active", isActive);
    item.setAttribute("aria-selected", String(isActive));
  });

  roadmapStage?.classList.remove("changing");
  void roadmapStage?.offsetWidth;
  roadmapStage?.classList.add("changing");
  roadmapStage?.setAttribute("data-roadmap-state", tab.dataset.roadmapHorizon);

  if (roadmapIndex) roadmapIndex.textContent = tab.dataset.index;
  if (roadmapKicker) roadmapKicker.textContent = tab.dataset.kicker;
  if (roadmapTitle) roadmapTitle.textContent = tab.dataset.title;
  if (roadmapCopy) roadmapCopy.textContent = tab.dataset.copy;
  if (roadmapFocus) roadmapFocus.textContent = tab.dataset.focus;
  if (roadmapOutcome) roadmapOutcome.textContent = tab.dataset.outcome;
  if (roadmapRule) roadmapRule.textContent = tab.dataset.rule;
  if (roadmapMoment) roadmapMoment.textContent = tab.dataset.moment;
};

roadmapTabs.forEach((tab) => {
  tab.addEventListener("click", () => selectRoadmapHorizon(tab));
});

if (roadmapTabs[0]) {
  selectRoadmapHorizon(roadmapTabs[0]);
}

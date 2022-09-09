function parseWebsocketMessage(event, serverMessage) {
  serverMessage.textContent = event.data;
}

const websocket = new WebSocket(`ws://${window.location.host}/ws`);

serverMessage = document.createElement("div");
websocket.onmessage = (event) => {
  parseWebsocketMessage(event, serverMessage);
};

const addToScheduleControls = document.createElement("div");
addToScheduleControls.style.display = "flex";
addToScheduleControls.style.flexDirection = "column";
addToScheduleControls.style.alignItems = "flex-end";

const daysLabel = document.createElement("label");
daysLabel.textContent = "days";
const daysInput = document.createElement("input");
daysInput.type = "number";

const monthsLabel = document.createElement("label");
monthsLabel.textContent = "months";
const monthsInput = document.createElement("input");
monthsInput.type = "number";

const yearsLabel = document.createElement("label");
yearsLabel.textContent = "years";
const yearsInput = document.createElement("input");
yearsInput.type = "number";

const whatLabel = document.createElement("label");
whatLabel.textContent = "what";
const whatInput = document.createElement("input");

const button = document.createElement("button");
button.textContent = "add";
button.onclick = () => {
  websocket.send(JSON.stringify({
    method: "add",
    what: whatInput.value,
    months: monthsInput.value,
    years: yearsInput.value,
  }));
};

document.body.append(addToScheduleControls);
document.body.append(serverMessage);
addToScheduleControls.append(whatLabel);
whatLabel.append(whatInput);
addToScheduleControls.append(daysLabel);
daysLabel.append(daysInput);
addToScheduleControls.append(monthsLabel);
monthsLabel.append(monthsInput);
addToScheduleControls.append(yearsLabel);
yearsLabel.append(yearsInput);
addToScheduleControls.append(button);

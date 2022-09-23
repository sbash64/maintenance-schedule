function parseWebsocketMessage(event, serverMessage) {
  serverMessage.textContent = event.data;
}

function createRemoveFromScheduleControls() {
  const controls = document.createElement("div");
  controls.style.display = "flex";
  controls.style.flexDirection = "column";
  controls.style.alignItems = "flex-end";

  const whatLabel = document.createElement("label");
  whatLabel.textContent = "what";
  const whatInput = document.createElement("input");

  const button = document.createElement("button");
  button.textContent = "remove";
  button.onclick = () => {
    websocket.send(JSON.stringify({
      method: "remove",
      what: whatInput.value,
    }));
  };

  controls.append(whatLabel);
  whatLabel.append(whatInput);
  controls.append(button);
  return controls;
}

function createAddToScheduleControls() {
  const controls = document.createElement("div");
  controls.style.display = "flex";
  controls.style.flexDirection = "column";
  controls.style.alignItems = "flex-end";

  const fromDateLabel = document.createElement("label");
  fromDateLabel.textContent = "from date";
  const fromDateInput = document.createElement("input");
  fromDateInput.type = "date";

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
      fromDate: fromDateInput.value,
      howOften: {
        days: daysInput.value,
        months: monthsInput.value,
        years: yearsInput.value,
      },
    }));
  };

  controls.append(whatLabel);
  whatLabel.append(whatInput);
  controls.append(fromDateLabel);
  fromDateLabel.append(fromDateInput);
  controls.append(daysLabel);
  daysLabel.append(daysInput);
  controls.append(monthsLabel);
  monthsLabel.append(monthsInput);
  controls.append(yearsLabel);
  yearsLabel.append(yearsInput);
  controls.append(button);
  return controls;
}

const websocket = new WebSocket(`ws://${window.location.host}/ws`);

serverMessage = document.createElement("pre");
websocket.onmessage = (event) => {
  parseWebsocketMessage(event, serverMessage);
};

const removeFromScheduleControls = document.createElement("div");
removeFromScheduleControls.style.display = "flex";
removeFromScheduleControls.style.flexDirection = "column";
removeFromScheduleControls.style.alignItems = "flex-end";

document.body.append(createAddToScheduleControls());
document.body.append(createRemoveFromScheduleControls());
document.body.append(serverMessage);

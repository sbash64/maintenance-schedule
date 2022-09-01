function parseWebsocketMessage(event, serverMessage) {
serverMessage.textContent = event.data;
}

const websocket = new WebSocket(`ws://${window.location.host}/ws`);

serverMessage = document.createElement("div");
websocket.onmessage = (event) => { parseWebsocketMessage(event, serverMessage); };

const monthsLabel = document.createElement("label")
monthsLabel.textContent = "months"
const monthsInput = document.createElement("input")
monthsInput.type = "number"

const yearsLabel = document.createElement("label")
yearsLabel.textContent = "years"
const yearsInput = document.createElement("input")
yearsInput.type = "number"

const whatLabel = document.createElement("label")
whatLabel.textContent = "what"
const whatInput = document.createElement("input")

const button = document.createElement("button");
button.textContent = "add"
button.onclick = () => { websocket.send(JSON.stringify({
	method: "add",
	what: whatInput.value,
	months: monthsInput.value,
	years: yearsInput.value
})); };

document.body.append(serverMessage)
document.body.append(whatLabel)
whatLabel.append(whatInput)
document.body.append(monthsLabel)
monthsLabel.append(monthsInput)
document.body.append(yearsLabel)
yearsLabel.append(yearsInput)
document.body.append(button)

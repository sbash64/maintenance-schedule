function parseWebsocketMessage(event, serverMessage) {
serverMessage.textContent = event.data;
}

const websocket = new WebSocket(`ws://${window.location.host}/ws`);

serverMessage = document.createElement("div");
websocket.onmessage = (event) => { parseWebsocketMessage(event, serverMessage); };

const clientMessage = document.createElement("input")

const button = document.createElement("button");
button.textContent = "send"
button.onclick = () => { websocket.send(clientMessage.value); };

document.body.append(serverMessage)
document.body.append(clientMessage)
document.body.append(button)

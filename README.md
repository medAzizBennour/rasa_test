import express, { Application } from "express";
import WebSocket from "ws";

const app: Application = express();

const PORT: string | number = process.env.PORT || 5000;

// create a WebSocket server
const wss = new WebSocket.Server({ port: 4000 });

wss.on("connection", (ws: WebSocket) => {
    console.log("WebSocket client connected");

    // send a JSON message to the client
    const message = {
        type: "message",
        data: { action: "navigate", parameters: { page: "Dashboard" } },
    };
    ws.send(JSON.stringify(message));
});

wss.on("message", (message: string) => {
    console.log(`Received message: ${message}`);

    
});


app.listen(PORT, () =>
    console.log(` 📡 Backend server: ` + ` Running  on port ${PORT}`)
);

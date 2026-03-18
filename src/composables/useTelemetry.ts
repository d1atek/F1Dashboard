import { ref, onMounted, onUnmounted } from 'vue';

export interface TelemetryData {
  trc: number;
  air: number;
  hum: number;
  fl: number;
  fr: number;
  rl: number;
  rr: number;
}

export function useTelemetry() {
  const statusMessage = ref('Waiting for server...');
  const statusColor = ref('yellow');
  const telemetry = ref<TelemetryData>({ trc: 0, air: 0, hum: 0, fl: 0, fr: 0, rl: 0, rr: 0 });
  const latestMessage = ref('');
  const isAnalysing = ref(false);
  let ws: WebSocket | null = null;
  let intervalId: number | null = null;

  const sendMessage = (messageText: string) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ text: messageText }));
      isAnalysing.value = true;
    }
  };

  const sendDataToServer = (dataObject: any) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(dataObject));
    }
  };

  const connectWebSocket = () => {
    ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => {
      statusMessage.value = "Connected !";
      statusColor.value = "lime";
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.msg) {
        latestMessage.value = data.msg;
        isAnalysing.value = false;
      }
      if (data.tyres) {
        telemetry.value.fl = 0;
        telemetry.value.fr = 0;
        telemetry.value.rl = 0;
        telemetry.value.rr = 0;
      }
    };

    ws.onclose = () => {
      statusMessage.value = "Connection lost. Reconnecting in 3s...";
      statusColor.value = "red";
      setTimeout(connectWebSocket, 3000);
    };
  };

  onMounted(() => {
    connectWebSocket();
    telemetry.value.trc = 60 + (Math.random() - 0.5) * 10;
    telemetry.value.air = 20 + (Math.random() - 0.5) * 10;
    telemetry.value.hum = 50 + (Math.random() - 0.5) * 10;
    telemetry.value.fl = 0;
    telemetry.value.fr = 0;
    telemetry.value.rl = 0;
    telemetry.value.rr = 0;

    intervalId = setInterval(() => {
      telemetry.value.trc += (Math.random() - 0.5) / 10;
      telemetry.value.air += (Math.random() - 0.5) / 10;
      telemetry.value.hum += (Math.random() - 0.5) / 10;
      telemetry.value.fl = Math.min(telemetry.value.fl + Math.random() / 50, 100);
      telemetry.value.fr = Math.min(telemetry.value.fr + Math.random() / 50, 100);
      telemetry.value.rl = Math.min(telemetry.value.rl + Math.random() / 50, 100);
      telemetry.value.rr = Math.min(telemetry.value.rr + Math.random() / 50, 100);
      sendDataToServer({ trc: telemetry.value.trc, air: telemetry.value.air, hum: telemetry.value.hum, fl: telemetry.value.fl, fr: telemetry.value.fr, rl: telemetry.value.rl, rr: telemetry.value.rr });
    }, 50) as unknown as number;
  });

  onUnmounted(() => {
    if (ws) ws.close();
    if (intervalId !== null) clearInterval(intervalId);
  });

  return {
    statusMessage,
    statusColor,
    telemetry,
    latestMessage,
    isAnalysing,
    sendMessage
  };
}

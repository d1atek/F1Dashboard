<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Gauge from './components/Gauge.vue';
import TrackMap from './components/TrackMap.vue';
import CommandBox from './components/CommandBox.vue';
import TeamRadio from './components/TeamRadio.vue';

const statusMessage = ref('Waiting for server...');
const statusColor = ref('yellow');
const telemetry = ref({ trc: 0, air: 0, hum: 0 });
const latestMessage = ref('');
let ws = null;

const sendMessage = (messageText) => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ text: messageText }));
  }
};

const sendDataToServer = (dataObject) => {
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
    latestMessage.value = JSON.parse(event.data);
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
});
onUnmounted(() => { if (ws) ws.close(); });

const trackProgress = ref(0);

setInterval(() => {
  trackProgress.value += 0.5;
  if (trackProgress.value >= 100) trackProgress.value = 0;
  telemetry.value.trc += (Math.random() - 0.5) / 10;
  telemetry.value.air += (Math.random() - 0.5) / 10;
  telemetry.value.hum += (Math.random() - 0.5) / 10;
  sendDataToServer({ trc: telemetry.value.trc, air: telemetry.value.air, hum: telemetry.value.hum });
}, 50);

</script>

<template>
  <div class="dashboard-wrapper">
    <h1>F1 dashboard</h1>
    
    <div :style="{ color: statusColor, marginBottom: '20px' }">
      {{ statusMessage }}
    </div>

    <div class="dashboard-row">
      <Gauge title="TRC" :value="telemetry.trc" :max="100" unit="°C" color="#b2ff05" />
      <Gauge title="AIR" :value="telemetry.air" :max="100"  unit="°C" color="#b2ff05" />
      <Gauge title="HUM" :value="telemetry.hum" :max="100" unit="%"  color="#3344ff" />
    </div>
    <TrackMap :progress="trackProgress" />

    <TeamRadio :latestMessage="latestMessage" />
    <CommandBox @sendCommand="sendMessage" />
  </div>
</template>

<style scoped>
.dashboard-wrapper {
  display: flex; flex-direction: column; align-items: center; padding-top: 50px;
}
.dashboard-row {
  display: flex; gap: 30px; margin-top: 20px;
}
.message-box {
  margin-top: 30px; padding: 15px; border: 1px solid #333; 
  border-radius: 8px; color: #ccc; min-width: 300px; text-align: center;
}
</style>
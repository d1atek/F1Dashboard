<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Gauge from './components/Gauge.vue';
import TrackMap from './components/TrackMap.vue';

const statusMessage = ref('Waiting for server...');
const statusColor = ref('yellow');
const telemetry = ref({ trc: 0, air: 0, hum: 0, message: '' });
let ws = null;

const connectWebSocket = () => {
  ws = new WebSocket("ws://localhost:8000/ws");

  ws.onopen = () => { 
    statusMessage.value = "Connected !"; 
    statusColor.value = "lime";
  };

  ws.onmessage = (event) => {
    telemetry.value = JSON.parse(event.data);
  };
  
  ws.onclose = () => {
    statusMessage.value = "Connection lost. Reconnecting in 3s...";
    statusColor.value = "red";
    setTimeout(connectWebSocket, 3000); 
  };
};

onMounted(() => connectWebSocket());
onUnmounted(() => { if (ws) ws.close(); });

const trackProgress = ref(0);

setInterval(() => {
  trackProgress.value += 0.5;
  if (trackProgress.value >= 100) trackProgress.value = 0;
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

    <div class="message-box"> {{ telemetry.message }}</div>
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
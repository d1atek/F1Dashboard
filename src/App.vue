<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import Gauge from './components/Gauge.vue';
import TrackMap from './components/TrackMap.vue';
import CommandBox from './components/CommandBox.vue';
import TeamRadio from './components/TeamRadio.vue';
import CarStatus from './components/CarStatus.vue';
import { useTelemetry } from './composables/useTelemetry';

const { statusMessage, statusColor, telemetry, latestMessage, sendMessage } = useTelemetry();

const trackProgress = ref(0);
let intervalId: number | null = null;

onMounted(() => {
  intervalId = setInterval(() => {
    trackProgress.value += 0.5;
    if (trackProgress.value >= 100) trackProgress.value = 0;
  }, 50) as unknown as number;
});

onUnmounted(() => {
  if (intervalId !== null) clearInterval(intervalId);
});

</script>

<template>
  <div class="dashboard-wrapper">
    <h1>F1 dashboard</h1>
    
    <div :style="{ color: statusColor, marginBottom: '20px' }">
      {{ statusMessage }}
    </div>

    <div class="dashboard-row">
      <div> 
        <div class="dashboard-row">
          <Gauge title="TRC" :value="telemetry.trc" :max="100" unit="°C" color="#b2ff05" />
          <Gauge title="AIR" :value="telemetry.air" :max="100"  unit="°C" color="#b2ff05" />
          <Gauge title="HUM" :value="telemetry.hum" :max="100" unit="%"  color="#3344ff" />
        </div>
        <TrackMap :progress="trackProgress" />
        <CarStatus :tires="{ fl: telemetry.fl.toFixed(0), fr: telemetry.fr.toFixed(0), rl: telemetry.rl.toFixed(0), rr: telemetry.rr.toFixed(0) }" />
      </div>
      <div>
        <TeamRadio :latestMessage="latestMessage" />
      </div>
    </div>

    <CommandBox @sendCommand="sendMessage" />
  </div>
</template>

<style scoped>
.dashboard-wrapper {
  display: flex; flex-direction: column; align-items: center; padding: 20px; width: 100%; max-width: 1200px; margin: 0 auto; box-sizing: border-box;
}
.dashboard-row {
  display: flex; gap: 30px; margin-top: 20px; flex-wrap: wrap; justify-content: center;
}
</style>
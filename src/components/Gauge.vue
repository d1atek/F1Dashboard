<script setup>
import { computed } from 'vue';

const props = defineProps({
  title: { type: String, required: true },
  value: { type: Number, required: true },
  max:   { type: Number, default: 100 },
  unit:  { type: String, default: '' },
  color: { type: String, default: '#b2ff05' }
});

const percentage = computed(() => {
  return Math.min((props.value / props.max) * 100, 100);
});

const gaugeStyle = computed(() => ({
  background: `conic-gradient(${props.color} 0%, ${props.color} ${percentage.value}%, #222 ${percentage.value}%)`
}));
</script>

<template>
  <div class="gauge-container" :style="gaugeStyle">
    <div class="gauge-center">
      <span class="gauge-value">{{ value.toFixed(1) }}</span>
      <span class="gauge-unit" v-if="unit">{{ unit }}</span>
      <span class="gauge-label" :style="{ color: color }">{{ title }}</span>
    </div>
  </div>
</template>

<style scoped>
.gauge-container {
  width: 80px; height: 80px; border-radius: 50%;
  display: flex; justify-content: center; align-items: center;
  transition: background 0.3s ease-in-out;
}
.gauge-center {
  width: 65px; height: 65px; background-color: #111; border-radius: 50%;
  display: flex; flex-direction: column; justify-content: center; align-items: center;
}
.gauge-value { font-size: 18px; font-weight: bold; margin: 0; }
.gauge-unit { font-size: 8px; color: #888; }
.gauge-label { font-size: 12px; font-weight: bold; }
</style>
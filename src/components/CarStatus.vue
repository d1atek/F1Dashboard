<template>
  <div class="car-status-container">
    
    <div class="side-column">
      <div class="tyre-wrapper">
        <div class="tyre-box" :style="getBoxStyle(tires.fl)">
          <span class="tyre-value">{{ tires.fl }}%</span>
        </div>
        <div class="dashed-line right"></div>
      </div>
      
      <div class="tyre-wrapper">
        <div class="tyre-box" :style="getBoxStyle(tires.rl)">
          <span class="tyre-value">{{ tires.rl }}%</span>
        </div>
        <div class="dashed-line right"></div>
      </div>
    </div>

    <div class="car-center">
      <svg viewBox="0 0 100 250" class="f1-car-svg">
        <path d="M 20 40 L 80 40 L 85 55 L 15 55 Z" fill="#2a323c" stroke="#445" stroke-width="2"/>
        <rect x="10" y="55" width="15" height="35" rx="3" fill="#111" stroke="#445" />
        <rect x="75" y="55" width="15" height="35" rx="3" fill="#111" stroke="#445" />
        <path d="M 45 40 L 55 40 L 60 120 L 40 120 Z" fill="#111" stroke="#445" />
        <path d="M 35 110 L 65 110 L 75 180 L 25 180 Z" fill="#2a323c" stroke="#445" stroke-width="1.5"/>
        <rect x="5" y="170" width="20" height="40" rx="3" fill="#111" stroke="#445" />
        <rect x="75" y="170" width="20" height="40" rx="3" fill="#111" stroke="#445" />
        <path d="M 25 210 L 75 210 L 75 230 L 25 230 Z" fill="#2a323c" stroke="#445" stroke-width="2"/>
      </svg>
    </div>

    <div class="side-column">
      <div class="tyre-wrapper">
        <div class="dashed-line left"></div>
        <div class="tyre-box" :style="getBoxStyle(tires.fr)">
          <span class="tyre-value">{{ tires.fr }}%</span>
        </div>
      </div>
      
      <div class="tyre-wrapper">
        <div class="dashed-line left"></div>
        <div class="tyre-box" :style="getBoxStyle(tires.rr)">
          <span class="tyre-value">{{ tires.rr }}%</span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { onMounted } from 'vue';

const props = defineProps({
  tires: {
    type: Object,
    default: () => ({ fl: 0, fr: 0, rl: 1, rr: 1 })
  }
});

const getBoxStyle = (wearPercentage) => {
  let color = '#00ff33'; 
  let bgAlpha = '0.15';

  if (wearPercentage > 40) color = '#ffcc00'; 
  if (wearPercentage > 70) color = '#ff003c'; 

  return {
    borderColor: color,
    backgroundColor: `rgba(${hexToRgb(color)}, ${bgAlpha})`,
    color: 'white', 
  };
};

const hexToRgb = (hex) => {
  let r = 0, g = 0, b = 0;
  if (hex.length == 7) {
    r = parseInt(hex.substring(1, 3), 16);
    g = parseInt(hex.substring(3, 5), 16);
    b = parseInt(hex.substring(5, 7), 16);
  }
  return `${r}, ${g}, ${b}`;
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');

.car-status-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  background-color: #00000000; 
  padding: 30px;
  border-radius: 12px;
  width: max-content;
  margin: 0 auto;
}

.side-column {
  display: flex;
  flex-direction: column;
  gap: 80px; 
}

.tyre-wrapper {
  display: flex;
  align-items: center;
}

.tyre-box {
  width: 70px;
  height: 90px;
  border: 4px solid;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.tyre-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
}

.dashed-line {
  width: 40px;
  border-bottom: 2px dashed rgba(255, 255, 255, 0.3);
}
.dashed-line.right {
  margin-left: 5px;
}
.dashed-line.left {
  margin-right: 5px;
}

.car-center {
  width: 100px;
  display: flex;
  justify-content: center;
}
.f1-car-svg {
  width: 100%;
  height: auto;
  filter: drop-shadow(0 10px 10px rgba(0,0,0,0.5));
}
</style>
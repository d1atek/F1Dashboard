<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  latestMessage: { type: String, required: true }
});

const activeMessages = ref([]);
let messageIdCounter = 0;

watch(() => props.latestMessage, (newMsg, oldMsg) => {
  if (newMsg && newMsg !== oldMsg && newMsg !== '...') {
    const id = messageIdCounter++;
    activeMessages.value.unshift({ id, text: newMsg });

    if (activeMessages.value.length > 3) {
      activeMessages.value.pop();
    }
  }
});
</script>

<template>
  <div class="radio-container">
    <TransitionGroup name="radio-anim" tag="div" class="radio-list">
      
      <div v-for="msg in activeMessages" :key="msg.id" class="radio-box">
        <div class="radio-header">
          TEAM RADIO
        </div>
        <div class="radio-text">
          {{ msg.text }}
        </div>
      </div>
      
    </TransitionGroup>
  </div>
</template>

<style scoped>
.radio-container {
  width: 100%;
  height: 240px;
  max-width: 400px;
  overflow: hidden; 
}
.radio-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.radio-box {
  background-color: rgba(15, 15, 15, 0.95);
  border-left: 5px solid #ff003c;
  border-radius: 4px;
  padding: 8px 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  border-top: 1px solid #333;
  border-right: 1px solid #333;
  border-bottom: 1px solid #333;
}
.radio-header {
  color: #fbd304;
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 1.5px;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.radio-text {
  color: white;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.4;
}

.radio-anim-enter-active,
.radio-anim-leave-active {
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
}

.radio-anim-enter-from {
  opacity: 0;
  transform: translateX(-40px);
}

.radio-anim-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
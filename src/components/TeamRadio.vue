<script setup lang="ts">
import { ref, watch } from 'vue';
import { marked } from 'marked';

interface Props {
  latestMessage: string;
  isAnalysing: boolean;
}

const props = defineProps<Props>();

interface Message {
  id: number;
  text: string;
}

const activeMessages = ref<Message[]>([]);
let messageIdCounter = 0;

watch(() => props.latestMessage, (newMsg, oldMsg) => {
  if (newMsg && newMsg !== oldMsg && newMsg !== '...') {
    const id = messageIdCounter++;
    activeMessages.value.unshift({ id, text: newMsg });

    //if (activeMessages.value.length > 3) {
    //  activeMessages.value.pop();
    //}
  }
});
</script>

<template>
  <div class="radio-container">
    <TransitionGroup name="radio-anim" tag="div" class="radio-list">

      <div v-if="isAnalysing" key="loading-indicator" class="radio-box loading-box">
        <div class="radio-header">
          RACE ENGINEER
        </div>
        <div class="radio-text loading-text">
          Analysing telemetry<span class="dots">...</span>
        </div>
      </div>
      
      <div v-for="msg in activeMessages" :key="msg.id" class="radio-box">
        <div class="radio-header">
          TEAM RADIO
        </div>
        <div class="radio-text markdown-content" v-html="marked.parse(msg.text)"></div>
      </div>
      
    </TransitionGroup>
  </div>
</template>

<style scoped>
.radio-container {
  min-width: 400px;
  width: 100%;
  height: 800px;
  max-width: 400px;
  margin-top: 20px;
  overflow-y: auto; 
  overflow-x: hidden; 
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-right: 5px;
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

.radio-text :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  margin-bottom: 10px;
  font-size: 13px;
}

.radio-text :deep(th), 
.radio-text :deep(td) {
  border: 1px solid #444;
  padding: 6px 10px;
  text-align: left;
}

.radio-text :deep(p) {
  margin: 0 0 8px 0; 
}

.radio-container::-webkit-scrollbar {
  width: 6px; 
}

.radio-container::-webkit-scrollbar-track {
  background: rgba(20, 20, 20, 0.5); 
  border-radius: 4px;
}

.radio-container::-webkit-scrollbar-thumb {
  background: #ff003c; 
  border-radius: 4px;
}

.radio-container::-webkit-scrollbar-thumb:hover {
  background: #cc0030; 
}

.loading-box {
  border-left: 5px solid #fbd304; 
  background-color: rgba(25, 20, 0, 0.95);
}

.loading-text {
  color: #fbd304 !important;
  font-style: italic;
  font-weight: bold;
  animation: pulse 1.5s infinite; 
}

@keyframes pulse {
  0% { opacity: 0.4; }
  50% { opacity: 1; }
  100% { opacity: 0.4; }
}

.dots {
  display: inline-block;
  overflow: hidden;
  vertical-align: bottom;
  animation: dots 1.5s linear infinite;
  width: 0px;
}

@keyframes dots {
  to { width: 1.25em; }
}
</style>
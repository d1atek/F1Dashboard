<script setup lang="ts">
import { ref } from 'vue';

const emit = defineEmits<{
  (e: 'sendCommand', text: string): void
}>();

const text = ref('');

const onSubmit = () => {
  if (text.value.trim() !== '') {
    emit('sendCommand', text.value);
    text.value = ''; 
  }
};
</script>

<template>
  <div class="command-center">
    <input 
      v-model="text" 
      @keyup.enter="onSubmit"
      type="text" 
      placeholder="Speak to your race engineer..." 
      class="command-input"
    />
    <button @click="onSubmit" class="command-btn">Send</button>
  </div>
</template>

<style scoped>
.command-center {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  width: 100%;
  max-width: 800px;
}
.command-input {
  flex: 1;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #444;
  background-color: #222;
  color: white;
  font-family: inherit;
}
.command-input:focus {
  outline: none;
  border-color: #ff003c;
}
.command-btn {
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  background-color: #ff003c;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}
.command-btn:hover {
  background-color: #cc0030;
}
</style>
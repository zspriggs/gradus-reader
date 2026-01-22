<template>
  <div class="syntax-sidebar">
    <h3>Syntax</h3>
    <div class="tip-text">
      <strong>Tip:</strong> Toggle syntax help in the settings menu.
    </div>
    <div class="syntax-list">
      <div v-if="syntaxPhrases.length === 0">
        No syntax phrases to display on this page.
      </div>
      <div
        v-for="(phrase, index) in syntaxPhrases"
        :key="index"
        class="syntax-item"
        :class="{ 'is-hovered': isPhrasehovered(phrase) }"
        @mouseenter="handleMouseEnter(phrase)"
        @mouseleave="handleMouseLeave"
      >
        <button 
          class="pin-button" 
          @click="pinSyntax(phrase)" 
          :class="{ 'is-active': activeId === phrase.syntax_id }"
        >
          📌
        </button>
        <div class="syntax-type">{{getWordDisplay(phrase)}}</div>
        <div class="syntax-meta">
          {{ phrase.type }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import {ref} from 'vue';

const activeId=ref(null)

const props = defineProps({
  syntaxPhrases: {
    type: Array,
    required: true,
    default: () => []
  },
  hoveredSyntaxPhrase: {
    type: Object, // { uids: [...] } or null
    default: null
  }
});

const emit = defineEmits(['syntax-hover', 'syntax-unhover', 'pin-toggle']);

const handleMouseEnter = (phrase) => {
  emit('syntax-hover', phrase);
};

const handleMouseLeave = () => {
  emit('syntax-unhover');
};

const pinSyntax = (phrase) => {
  if(activeId.value && activeId.value === phrase.syntax_id){
    activeId.value = null;
  } else { activeId.value = phrase.syntax_id; }
  emit('pin-toggle', phrase);
}

const isPhrasehovered = (phrase) => {
  if (!props.hoveredSyntaxPhrase) return false;
  
  // Check if the arrays have any overlap
  return phrase.uids.some(uid => 
    props.hoveredSyntaxPhrase.uids?.includes(uid)
  );
};

const getWordDisplay = (phrase) => {
  if (!phrase) return false;
  const firstWord = phrase.firstWord
  const lastWord = phrase.lastWord
  return `${firstWord} ${lastWord ? ' ... ' + lastWord : ''}`;
}
</script>

<style scoped>
.syntax-sidebar {
  padding: 1rem;
  padding-top: 60px;
  background: #f8f9fa;
  border-left: 1px solid #dee2e6;
  height: 100%;
  min-width: 330px;
  overflow-y: auto;
  overflow-x: auto;
  z-index: 10;
}

.syntax-sidebar h3 {
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  color: #212529;
}

.syntax-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.syntax-item {
  padding: 0.75rem;
  background: white;
  min-width: 7rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.syntax-item:hover {
  border-color: #0d6efd;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.syntax-item.is-hovered {
  background: #e7f1ff;
  border-color: #0d6efd;
}

.syntax-type {
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.25rem;
}

.syntax-meta {
  font-size: 0.875rem;
  color: #6c757d;
}

.pin-button {
  position: relative;
  padding: 5px;
  left: 90%;
  background: var(--yellow-syntax-highlight);
  border-color: var(--yellow-syntax-underline);
  border-radius: 4px;
  cursor: pointer;
}

.pin-button.is-active {
  background: var(--yellow-syntax-underline);
}

.tip-text {
  margin-top: 16px;
  margin-bottom: 16px;
  font-size: 0.875rem;
  color: var(--gray-text);
}
</style>
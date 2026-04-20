<template>
  <div class="syntax-sidebar">
    <h3>Syntax</h3>
    <div class="tip-text">
      <strong>Tip:</strong> You can close this syntax panel in the settings menu.
    </div>
    <div class="tip-text">
      <strong>Warning:</strong> Syntax phrases are automatically detected, and may be prone to errors.
    </div>
    <div class="pin-button-box">
      <button
        class="pin-all-button"
        @click="pinAll"
      >
        Pin All
      </button>
      <button
        class="unpin-all-button"
        @click="unpinAll"
      >
        Unpin All
      </button>
    </div>
    <div class="syntax-list">
      <div v-if="syntaxPhrases.length === 0">
        No syntax phrases to display on this page.
      </div>
      <div
        v-for="(phrase, index) in syntaxPhrases"
        :key="phrase.syntax_id"
        class="syntax-item"
        @mouseenter="handleMouseEnter(phrase)"
        @mouseleave="handleMouseLeave"
      >
        <button 
          class="pin-button" 
          @click="pinSyntax(phrase)" 
          :class="{ 'is-active': isPhrasePinned(phrase)}"
        >
          📌
        </button>
        <div class="syntax-type">{{getWordDisplay(phrase)}}</div>
        <a class="syntax-meta" :href=phrase.grammar_ref target="_blank">{{phrase.type}}</a>
      </div>
    </div>
  </div>
</template>

<script setup>

import {ref} from 'vue';

const activeIds=ref([]);

const props = defineProps({
  syntaxPhrases: {
    type: Array,
    required: true,
    default: () => []
  },
  hoveredSyntaxId: {
    type: Number
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
  // if item is in the active ids, remove it, otherwise, add it
  if(activeIds.value && activeIds.value.includes(phrase.syntax_id)) {
    const index = activeIds.value.indexOf(phrase.syntax_id);
    if (index > -1) {
      activeIds.value.splice(index, 1); 
    }
  } else { activeIds.value.push(phrase.syntax_id); }

  emit('pin-toggle', activeIds.value);
};

const pinAll = () => {
  activeIds.value = []
  props.syntaxPhrases.forEach(phrase => {
    activeIds.value.push(phrase.syntax_id);
  });

  emit('pin-toggle', activeIds.value);
};

const unpinAll = () => {
  activeIds.value = []
  emit('pin-toggle', activeIds.value);
};

const isPhrasePinned = (phrase) => {
  if (!activeIds.value) return false;
  return activeIds.value.includes(phrase.syntax_id);
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
  height: 100vh;
  width: 20rem;
  overflow-y: auto;
  overflow-x: auto;
  resize: horizontal;
  z-index: 10;
}

@media (max-width: 1200px) {
  .syntax-sidebar {
    width: 40%;
  }
}

.syntax-sidebar h3 {
  margin: 0 0 1rem 0;
  font-size: 1.125rem;
  color: #212529;
}

.pin-button-box {
  padding: 0 0 1rem 0;
}

.pin-all-button {
  position: relative;
  padding: 5px;
  left: 20%;
  background: var(--yellow-syntax-highlight);
  border-color: var(--yellow-syntax-underline);
  border-radius: 4px;
  cursor: pointer;
}

.unpin-all-button {
  position: relative;
  padding: 5px;
  left: 40%;
  background: var(--yellow-syntax-highlight);
  border-color: var(--yellow-syntax-underline);
  border-radius: 4px;
  cursor: pointer;
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

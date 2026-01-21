<template>
  <div class="syntax-sidebar">
    <h3>Syntax</h3>
    <div class="syntax-list">
      <div
        v-for="(phrase, index) in syntaxPhrases"
        :key="index"
        class="syntax-item"
        :class="{ 'is-hovered': isPhrasehovered(phrase) }"
        @mouseenter="handleMouseEnter(phrase)"
        @mouseleave="handleMouseLeave"
      >
        <div class="syntax-type">{{getWordDisplay(phrase)}}</div>
        <div class="syntax-meta">
          {{ phrase.type }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

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

const emit = defineEmits(['syntax-hover', 'syntax-unhover']);

const handleMouseEnter = (phrase) => {
  emit('syntax-hover', phrase);
};

const handleMouseLeave = () => {
  emit('syntax-unhover');
};

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
  border: 1px solid #dee2e6;
  border-radius: 4px;
  cursor: pointer;
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
</style>
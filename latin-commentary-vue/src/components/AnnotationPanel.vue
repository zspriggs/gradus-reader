<template>
  <div class="annotation-panel">
    <h3 class="annotation-title">{{ word.word }}</h3>
    <p class="annotation-lemma">
      <span class="lemma-label">Lemma:</span> {{ word.lemma }}
    </p>
    
    <!-- Beginner level annotations -->
    <div v-if="level === 'beginner' && word.beginner">
      <div v-if="word.beginner.vocab" class="annotation-section">
        <span class="annotation-label beginner">Vocabulary:</span>
        <p class="annotation-text">{{ word.beginner.vocab }}</p>
      </div>
      <div v-if="word.beginner.grammar" class="annotation-section">
        <span class="annotation-label beginner">Grammar:</span>
        <p class="annotation-text">{{ word.beginner.grammar }}</p>
      </div>
      <div v-if="word.beginner.notes" class="annotation-section">
        <span class="annotation-label beginner">Notes:</span>
        <p class="annotation-text">{{ word.beginner.notes }}</p>
      </div>
    </div>
    
    <!-- Intermediate/Advanced level annotations -->
    <div v-if="(level === 'intermediate' || level === 'advanced') && word.intermediate">
      <div v-if="word.intermediate.syntax" class="annotation-section">
        <span class="annotation-label intermediate">Syntax:</span>
        <p class="annotation-text">{{ word.intermediate.syntax }}</p>
      </div>
      <div v-if="word.intermediate.style" class="annotation-section">
        <span class="annotation-label intermediate">Style:</span>
        <p class="annotation-text">{{ word.intermediate.style }}</p>
      </div>
    </div>
    
    <!-- Advanced only annotations -->
    <div v-if="level === 'advanced' && word.advanced">
      <div v-if="word.advanced.rhetoric" class="annotation-section">
        <span class="annotation-label advanced">Rhetoric:</span>
        <p class="annotation-text">{{ word.advanced.rhetoric }}</p>
      </div>
      <div v-if="word.advanced.etymology" class="annotation-advanced">
        <em>Etymology: {{ word.advanced.etymology }}</em>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  word: {
    type: Object,
    required: true
  },
  level: {
    type: String,
    required: true
  }
});
</script>

<style scoped>
.annotation-panel {
  margin-top: 24px;
  padding: 16px;
  border: 2px solid #d1d5db;
  border-radius: 8px;
  background-color: #f9fafb;
}

.annotation-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #1d4ed8;
  margin-bottom: 8px;
}

.annotation-lemma {
  color: #6b7280;
  margin-bottom: 12px;
}

.annotation-lemma .lemma-label {
  font-weight: 600;
}

.annotation-section {
  margin-bottom: 8px;
}

.annotation-label {
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
}

.annotation-label.beginner {
  color: #059669;
}

.annotation-label.intermediate {
  color: #7c3aed;
}

.annotation-label.advanced {
  color: #dc2626;
}

.annotation-text {
  color: #374151;
  margin: 0;
}

.annotation-advanced {
  margin-top: 8px;
  font-size: 0.875rem;
  color: #6b7280;
  font-style: italic;
}
</style>
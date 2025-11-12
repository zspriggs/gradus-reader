<template>
  <div class="annotation-panel">
    <h3 class="annotation-title">{{ word.word }}</h3>
    <p class="annotation-lemma">
      <span class="lemma-label">Lemma:</span> {{ word.lemma }}
    </p>
    
    <!-- Vocabulary -->
    <div v-if="features.vocab && word.vocab" class="annotation-section">
      <span class="annotation-label vocab">Vocabulary:</span>
      <p class="annotation-text">{{ word.vocab }}</p>
    </div>
    
    <!-- Morphology -->
    <div v-if="features.morphology && word.morphology">
      <div v-if="word.morphology.grammar" class="annotation-section">
        <span class="annotation-label morphology">Grammar:</span>
        <p class="annotation-text">{{ word.morphology.grammar }}</p>
      </div>
      <div v-if="word.morphology.notes" class="annotation-section">
        <span class="annotation-label morphology">Notes:</span>
        <p class="annotation-text">{{ word.morphology.notes }}</p>
      </div>
    </div>
    
    <!-- Syntax -->
    <div v-if="features.syntax && word.syntax" class="annotation-section">
      <span class="annotation-label syntax">Syntax:</span>
      <p class="annotation-text">{{ word.syntax }}</p>
    </div>
    
    <!-- Style -->
    <div v-if="features.style && word.style" class="annotation-section">
      <span class="annotation-label style">Style:</span>
      <p class="annotation-text">{{ word.style }}</p>
    </div>
    
    <!-- Rhetoric -->
    <div v-if="features.rhetoric && word.rhetoric" class="annotation-section">
      <span class="annotation-label rhetoric">Rhetoric:</span>
      <p class="annotation-text">{{ word.rhetoric }}</p>
    </div>
    
    <!-- Message if no features enabled -->
    <div v-if="!hasFeatureEnabled" class="no-features-message">
      <p>Enable display options above to see annotations.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  word: {
    type: Object,
    required: true
  },
  features: {
    type: Object,
    required: true
  }
});

const hasFeatureEnabled = computed(() => {
  return Object.values(props.features).some(value => value === true);
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
  margin-bottom: 12px;
}

.annotation-label {
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
  font-size: 0.95rem;
}

.annotation-label.vocab {
  color: #059669;
}

.annotation-label.morphology {
  color: #0891b2;
}

.annotation-label.syntax {
  color: #7c3aed;
}

.annotation-label.style {
  color: #db2777;
}

.annotation-label.rhetoric {
  color: #dc2626;
}

.annotation-text {
  color: #374151;
  margin: 0;
  line-height: 1.5;
}

.annotation-etymology {
  font-style: italic;
  font-size: 0.9rem;
}

.no-features-message {
  text-align: center;
  padding: 20px;
  color: #6b7280;
  font-style: italic;
}

.no-features-message p {
  margin: 0;
}
</style>
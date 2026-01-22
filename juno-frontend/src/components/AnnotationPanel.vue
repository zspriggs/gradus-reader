<template>
  <div class="morphology-viewer">
    <!-- Annotation Popover -->
    <Teleport to="body">
      <template v-if="isOpen">
        <div 
          class="popover-backdrop"
          @click="handleClose"
        />
        <div class="popover-wrapper">
          <div class="popover-main">
            <div class="popover-header">
              <h3 class="popover-title">{{ word.form }}</h3>
              <button
                @click="handleClose"
                class="close-button"
                aria-label="Close"
              >x
              </button>
            </div>

            <div class="popover-body">
              <p class="annotation-lemma">
                <span class="lemma-label">Lemma:</span> {{ word.lemma }}
              </p>
              
              <!-- Vocabulary TODO: Add link-->
              <div v-if="features.vocab" class="annotation-section">
                <span class="annotation-label vocab">Vocabulary:
                  <a class="link-text" :href="vocabLink" target="_blank">
                    Perseus 
                  </a> 
                </span>
              </div>
              
              <!-- Morphology -->
              <div v-if="features.morphology && word.morphology">
                <div v-if="word.morphology.pos" class="annotation-section">
                  <span class="annotation-label morphology">Part of Speech:
                    <span class="annotation-text">{{ word.morphology.pos }}</span>
                  </span>
                </div>
                <div v-if="word.morphology.case" class="annotation-section">
                  <span class="annotation-label morphology">Case:
                    <span class="annotation-text">{{ word.morphology.case }}</span>
                  </span>
                </div>
                <div v-if="word.morphology.number" class="annotation-section">
                  <span class="annotation-label morphology">Number:
                    <span class="annotation-text">{{ word.morphology.number }}</span>
                  </span>
                </div>
                <div v-if="word.morphology.gender" class="annotation-section">
                  <span class="annotation-label morphology">Gender:
                    <span class="annotation-text">{{ word.morphology.gender }}</span>
                  </span>
                </div>
                <div v-if="word.morphology.degree" class="annotation-section">
                  <span class="annotation-label morphology">Degree:
                    <span class="annotation-text">{{ word.morphology.degree }}</span>
                  </span>
                </div>

                <div v-if="word.morphology.person" class="annotation-section">
                  <span class="annotation-label morphology">Person:
                    <span class="annotation-text">{{ word.morphology.person }}</span>
                  </span>
                </div>
                <div v-if="word.morphology.tense" class="annotation-section">
                  <span class="annotation-label morphology">Tense:
                    <span class="annotation-text">{{ word.morphology.tense }}</span>
                  </span>
                </div>
                <div v-if="word.morphology.mood" class="annotation-section">
                  <span class="annotation-label morphology">Mood:
                    <span class="annotation-text">{{ word.morphology.mood }}</span>
                  </span>
                </div>
                <div v-if="word.morphology.voice" class="annotation-section">
                  <span class="annotation-label morphology">Voice:
                    <span class="annotation-text">{{ word.morphology.voice }}</span>
                  </span> 
                </div>
              </div>
              
              <!-- Syntax -->
              <div v-if="features.syntax && word.syntax" class="annotation-section">
                <span class="annotation-label syntax">Syntax:</span>
                <p class="annotation-text">{{ word.syntax }}</p>
              </div>
              
              <!-- Message if no features enabled -->
              <div v-if="!hasFeatureEnabled" class="no-features-message">
                <p>Enable display options above to see annotations.</p>
              </div>
            </div>
            </div>

            </div>

      </template>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';

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

const isOpen=ref(false);

const emit = defineEmits(['close']);

onMounted(() => {
  nextTick(() => {
    isOpen.value = true;
  });
});

const hasFeatureEnabled = computed(() => {
  if (!props.features) return false;
  return Object.values(props.features).some(value => value === true);
});

const isAlphanumeric = (char) => {
  return /^[\p{L}\p{N}]$/u.test(char);
};

const vocabLink = computed(() => {
  let form = props.word.form;
  if (!isAlphanumeric(form.at(-1))) {
    form = form.slice(0, -1);
  }

  return `https://www.perseus.tufts.edu/hopper/morph?l=${form}&la=la`
});

const handleClose = () => {
  isOpen.value = false;
  emit('close');
};

</script>

<style scoped>
.morphology-viewer {
  position: relative;
}

.text-display {
  font-size: 1.5rem;
  line-height: 2.5;
}

.popover-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.1);
  z-index: 40;
}

.popover-wrapper {
  position: fixed;
  top: 150px;
  width: fit-content;
  height: auto;
  display: flex; 
  align-items: flex-start; 
  z-index: 50;
  max-width: 90vw; 
}

.popover-main {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

  resize: both;
  overflow: auto; 
  
  width: 14rem;
  height: auto;
  min-height: 300px;
  max-height: 80vh;
  
  display: flex;
  flex-direction: column;
}

.annotation-popover {
  position: fixed;
  top: 150px;
  z-index: 50;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  width: 14rem;
  max-height: calc(90vh - 100px);
  overflow: visible;
  resize: both;
}

.popover-inner {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  max-height: calc(90vh - 100px);
  overflow-y: auto;    
  display: flex;       
  flex-direction: column;
}

.popover-header {
  position: sticky;
  top: 0;
  background-color: var(--orange-button-hover);
  color: white;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 0.5rem 0.5rem 0 0;
}

.popover-title {
  font-weight: bold;
  font-size: 1.125rem;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s;
  font-size: 125%;
}

.close-button:hover {
  color: var(--title-dark);
}

.popover-body {
  padding: 1rem;
}

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
  color: var(--green-button-hover);
}

.annotation-label.morphology {
  color: var(--orange-button-hover);
}

.annotation-label.syntax {
  color: var(--dark-blue)
}

.annotation-text {
  color: #374151;
  margin: 0;
  line-height: 1.5;
}

.link-text {
  color: #1d4ed8;
  text-decoration: underline;
  cursor: pointer;
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
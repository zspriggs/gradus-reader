<template>
  <div class="morphology-annotator">
    <!-- Annotation Popover -->
    <Teleport to="body">
      <template v-if="isOpen">
        <div 
          class="popover-backdrop"
          @click="handleClose"
        />
        
        <div 
          class="annotation-popover"
          :style="{ 
            top: `${popoverPosition.top}px`, 
            left: `${popoverPosition.left}px`
          }"
        >
          <div class="popover-header">
            <h3 class="popover-title">{{ props.wordData.form }}</h3>
            <button
              @click="handleClose"
              class="close-button"
              aria-label="Close"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="popover-body">
            <p class="instruction-text">
              Select any features you want to practice:
            </p>
            
            <div class="form-fields">
              <div 
                v-for="(label, feature) in featureLabels" 
                :key="feature"
                class="form-field"
              >
                <label class="field-label">
                  {{ label }}
                </label>
                <select
                  v-model="annotations[feature]"
                  @change="validationResult = null"
                  class="field-select"
                >
                  <option value="">—</option>
                  <option 
                    v-for="option in morphologyOptions[feature]" 
                    :key="option" 
                    :value="option"
                  >
                    {{ option }}
                  </option>
                </select>
              </div>
            </div>

            <div class="button-group">
              <button
                @click="validateAnnotation"
                class="btn btn-primary"
              >
                Check
              </button>
              <button
                @click="handleClose"
                class="btn btn-secondary"
              >
                Skip
              </button>
            </div>

            <div 
              v-if="validationResult"
              :class="[
                'validation-result',
                validationResult.isCorrect ? 'validation-correct' : 'validation-incorrect'
              ]"
            >
              <svg 
                v-if="validationResult.isCorrect"
                xmlns="http://www.w3.org/2000/svg" 
                width="18" 
                height="18" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                stroke-width="2"
                class="validation-icon"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <svg 
                v-else
                xmlns="http://www.w3.org/2000/svg" 
                width="18" 
                height="18" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                stroke-width="2"
                class="validation-icon"
              >
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <div class="validation-content">
                <p class="validation-message">
                  {{ validationResult.message }}
                </p>
                <div 
                  v-if="validationResult.correctValues"
                  class="correct-answers"
                >
                  <strong>Correct:</strong>
                  <div 
                    v-for="(value, key) in validationResult.correctValues" 
                    :key="key"
                    class="correct-answer-item"
                  >
                    {{ featureLabels[key] }}: <span class="answer-value">{{ value }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';

const props = defineProps({
  wordData: {
    type: Object,
    required: true,
  },
  // Optional: which features to show (defaults to all)
  visibleFeatures: {
    type: Array,
    default: () => ['pos', 'case', 'number', 'gender', 'tense', 'mood', 'voice', 'person', 'declension', 'conjugation']
  }
});

const emit = defineEmits(['close', 'annotation-checked', 'annotation-correct', 'annotation-incorrect']);

// Latin morphological feature options
const morphologyOptions = {
  pos: ["noun", "verb", "adjective", "preposition", "conjunction", "pronoun", "adverb", "participle"],
  case: ["nominative", "genitive", "dative", "accusative", "ablative", "vocative", "locative"],
  number: ["singular", "plural"],
  gender: ["masculine", "feminine", "neuter"],
  tense: ["present", "imperfect", "future", "perfect", "pluperfect", "future perfect"],
  mood: ["indicative", "subjunctive", "imperative", "infinitive"],
  voice: ["active", "passive"],
  person: ["1st", "2nd", "3rd"]//,
  //declension: ["1st", "2nd", "3rd", "4th", "5th"],
  //conjugation: ["1st", "2nd", "3rd", "3rd-io", "4th"]
};

const featureLabels = {
  pos: "Part of Speech",
  case: "Case",
  number: "Number",
  gender: "Gender",
  tense: "Tense",
  mood: "Mood",
  voice: "Voice",
  person: "Person"//,
  //declension: "Declension",
  //conjugation: "Conjugation"
};

const isOpen = ref(false);
const annotations = ref({});
const validationResult = ref(null);
const popoverPosition = ref({ top: 0, left: 0 });

const calculatePosition = () => {
  // Find the word element in the DOM
  // We need to find the Word component that has is-selected class
  const selectedWordElement = document.querySelector('.word.is-selected');
  
  if (selectedWordElement) {
    const rect = selectedWordElement.getBoundingClientRect();
    popoverPosition.value = {
      top: rect.bottom + window.scrollY + 8,
      left: rect.left + window.scrollX
    };
  } else {
    // Fallback to center of screen if we can't find the element
    popoverPosition.value = {
      top: window.scrollY + 100,
      left: window.innerWidth / 2 - 192 // 192 = half of popover width (24rem = 384px)
    };
  }
};

// Open the popover when component mounts
onMounted(() => {
  nextTick(() => {
    calculatePosition();
    isOpen.value = true;
  });
});

// const handleClick = (word, index, event) => {
//   const rect = event.target.getBoundingClientRect();
//   popoverPosition.value = {
//     top: rect.bottom + window.scrollY + 8,
//     left: rect.left + window.scrollX
//   };
  
//   selectedWord.value = word;
//   selectedWordIndex.value = index;
//   annotations.value = {};
//   validationResult.value = null;
// };

const handleClose = () => {
  isOpen.value = false
  annotations.value = {};
  validationResult.value = null;
  emit('close');
};

const validateAnnotation = () => {
  const correctAnswer = props.wordData.morphology;
  
  if (!correctAnswer) {
    validationResult.value = {
      isCorrect: false,
      message: "No morphology data available for this word"
    };
    return;
  }

  // Get only the features the user filled in
  const filledFeatures = Object.keys(annotations.value).filter(key => annotations.value[key]);
  
  if (filledFeatures.length === 0) {
    validationResult.value = {
      isCorrect: false,
      message: "Please select at least one feature to check"
    };
    return;
  }

  // Check only the features they filled in
  const allCorrect = filledFeatures.every(key => 
    annotations.value[key] === correctAnswer[key]
  );

  const incorrectFeatures = filledFeatures.filter(key => 
    annotations.value[key] !== correctAnswer[key]
  );

  if (allCorrect) {
    const result = {
      isCorrect: true,
      message: `Correct! ${filledFeatures.map(f => featureLabels[f]).join(', ')} ✓`,
      checkedFeatures: filledFeatures,
      word: props.wordData.form,
      annotations: { ...annotations.value }
    };
    validationResult.value = result;
    emit('annotation-checked', result);
    emit('annotation-correct', result);
  } else {
    const correctValues = {};
    incorrectFeatures.forEach(key => {
      if (!correctAnswer[key]) {
        correctValues[key] = "N/A"
      }
      else {
        correctValues[key] = correctAnswer[key];
      }

    });
    
    const result = {
      isCorrect: false,
      message: `Incorrect: ${incorrectFeatures.map(f => featureLabels[f]).join(', ')}`,
      correctValues,
      word: props.wordData.form,
      annotations: { ...annotations.value }
    };
    validationResult.value = result;
    emit('annotation-checked', result);
    emit('annotation-incorrect', result);
  }
};
</script>

<style scoped>
.morphology-annotator {
  position: relative;
}

.text-display {
  font-size: 1.5rem;
  line-height: 2.5;
}

.word-clickable {
  display: inline-block;
  margin: 0 0.5rem;
  padding: 0.25rem 0.75rem;
  cursor: pointer;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.word-clickable:hover {
  background-color: #dbeafe;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.word-selected {
  background-color: #3b82f6;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.popover-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.1);
  z-index: 40;
}

.annotation-popover {
  position: fixed;
  z-index: 50;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border: 2px solid #bfdbfe;
  width: 24rem;
  max-height: calc(100vh - 100px);
  overflow: auto;
}

.popover-header {
  position: sticky;
  top: 0;
  background-color: #3b82f6;
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
}

.close-button:hover {
  color: #dbeafe;
}

.popover-body {
  padding: 1rem;
}

.instruction-text {
  font-size: 0.875rem;
  color: #4b5563;
  margin-bottom: 1rem;
}

.form-fields {
  max-height: 20rem;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.form-field {
  margin-bottom: 0.75rem;
}

.field-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
}

.field-select {
  width: 100%;
  padding: 0.375rem 0.5rem;
  font-size: 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
}

.field-select:focus {
  outline: none;
  ring: 2px;
  ring-color: #3b82f6;
  border-color: transparent;
}

.button-group {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  font-size: 0.875rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary {
  flex: 1;
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.btn-secondary {
  padding-left: 1rem;
  padding-right: 1rem;
  background-color: #e5e7eb;
  color: #374151;
}

.btn-secondary:hover {
  background-color: #d1d5db;
}

.validation-result {
  margin-top: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.375rem;
  display: flex;
  align-items: start;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.validation-correct {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
}

.validation-incorrect {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
}

.validation-icon {
  flex-shrink: 0;
}

.validation-correct .validation-icon {
  color: #16a34a;
}

.validation-incorrect .validation-icon {
  color: #dc2626;
}

.validation-content {
  flex: 1;
}

.validation-message {
  font-weight: 500;
  margin: 0;
}

.validation-correct .validation-message {
  color: #166534;
}

.validation-incorrect .validation-message {
  color: #991b1b;
}

.correct-answers {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #374151;
}

.correct-answer-item {
  margin-left: 0.5rem;
}

.answer-value {
  font-weight: 500;
}
</style>

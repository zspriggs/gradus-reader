<template>
  <div class="morphology-annotator">
    <!-- Annotation Popover -->
    <Teleport to="body">
      <template v-if="isOpen">
        <div 
          class="popover-backdrop"
          @click="handleClose"
        />
        
        <div class="popover-wrapper" >

          <div class="popover-main">

            <div class="popover-header">
              <h3 class="popover-title">{{ wordData.form }}</h3>
              <button
                @click="handleClose"
                class="close-button"
                aria-label="Close"
              >x
              </button>
            </div>

            <div class="popover-body">

              <div class="form-fields">
              <p class="instruction-text">
                Select any features you want to practice:
              </p>
                <div 
                  v-for="(label, feature) in featureLabels" 
                  :key="feature"
                  class="form-field"
                >
                  <label class="field-label">
                    {{ label }}
                  </label>

                  <template v-if="feature==='custom'">
                    <textarea
                      v-model="annotations[feature]"
                      placeholder="Type your notes here..."
                      class="field-customtext"
                      @input="validationResult = null"
                    ></textarea>
                  </template>

                  <template v-else>
                    <select
                      v-model="annotations[feature]"
                      @change="validationResult = null"
                      class="field-select"
                    >
                      <option value="">—</option>
                      <option 
                        v-for="option in morphologyOptions[language][feature]" 
                        :key="option" 
                        :value="option"
                      >
                        {{ option }}
                      </option>
                    </select>
                  </template>
                </div>
              </div>
              <div class="button-group">
                <button
                  @click="validateAnnotation"
                  class="btn btn-check"
                >
                  Check
                </button>
                <button
                @click="addAnnotation" 
                :disabled="!canAddAnnotation" 
                :class="{ 'button-disabled': !canAddAnnotation }"
                >
                  Add
                </button>
                <button
                  @click="handleClose"
                  class="btn btn-finish"
                >
                  Finish
                </button>
              </div>
            </div>



            <div 
              v-if="validationResult"
              :class="[
                'validation-result',
                validationResult.isCorrect ? 'validation-correct' : 'validation-incorrect'
              ]"
            >
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

          <!--Mistake viewer-->
          <div class="popover-sidecar">
            <button
              class="mistake-viewer-toggle"
              @click="mistakeViewerOpen = !mistakeViewerOpen"
              :class="{'mistake-viewer-open': mistakeViewerOpen}"
            >
              <span v-if="!mistakeViewerOpen">View Mistakes</span>
              <span v-else>x</span>
            </button>

            <div class="mistake-viewer" :class="{ 'open': mistakeViewerOpen }">
              <div class="mistake-viewer-content">
                <MistakeViewer
                  :mistake-tracker="mistakeTracker"
                  @clear-mistakes="handleClearMistakes" 
                />
              </div>
            </div>
          </div>

        </div>
      </template>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue';
import MistakeViewer from './MistakeViewer.vue';

const mistakeViewerOpen = ref(false);

const props = defineProps({
  wordData: {
    type: Object,
    required: true,
  },
  language: {
    type: String,
    required: true,
  },
  // which features to show (defaults to all)
  visibleFeatures: {
    type: Array,
    default: () => ['pos', 'case', 'number', 'gender', 'tense', 'mood', 'voice', 'person', 'degree']
  },
  mistakeTracker: {
    type: Object,
    default: {},
  }
});

const emit = defineEmits(['close', 'annotation-checked', 'annotation-correct', 'annotation-incorrect', 'annotation-added', 'clear-mistakes']);

// Latin morphological feature options
const morphologyOptions = {
  grc: {  
    pos: ["noun", "verb", "adjective", "preposition", "conjunction", "pronoun", "adverb", "participle", "particle", "article", "numeral", "interjection", "exclamation", "irregular"],
    case: ["nominative", "genitive", "dative", "accusative", "locative", "vocative", "locative"],
    number: ["singular", "dual", "plural"],
    gender: ["masculine", "feminine", "neuter"],
    tense: ["present", "imperfect", "future", "perfect", "pluperfect", "future perfect", "aorist"],
    mood: ["indicative", "subjunctive", "optative", "gerund", "gerundive", "imperative", "infinitive"],
    voice: ["active", "passive", "middle", "mediopassive"],
    person: ["first", "second", "third"], 
    degree: ["positive", "comparative", "superlative"]},
  lat: {
    pos: ["noun", "verb", "adjective", "preposition", "conjunction", "pronoun", "adverb", "participle"],
    case: ["nominative", "genitive", "dative", "accusative", "ablative", "vocative", "locative"],
    number: ["singular", "plural"],
    gender: ["masculine", "feminine", "neuter"],
    tense: ["present", "imperfect", "future", "perfect", "pluperfect", "future perfect"],
    mood: ["indicative", "subjunctive", "imperative", "infinitive"],
    voice: ["active", "passive", "deponent"],
    person: ["first", "second", "third"],
    degree: ["positive", "comparative", "superlative"]}
};

const featureLabels = {
  pos: "Part of Speech",
  case: "Case",
  number: "Number",
  gender: "Gender",
  tense: "Tense",
  mood: "Mood",
  voice: "Voice",
  person: "Person",
  degree: "Degree", 
  custom: "Custom Note"
  //declension: "Declension",
  //conjugation: "Conjugation"
};

const isOpen = ref(false);
const annotations = ref({});
const validationResult = ref(null);
const lastValidationResult = ref(null);
//const popoverPosition = ref({ top: 0, left: 0 });

const canAddAnnotation = computed(() => {
  // button enabled iff the last time validation ran, it found >= 1 correct feat
  // and also there's no new stale (unvalidated) data
  // OR button enabled if there's a custom note do add

  const hasCustomNote = !!annotations.value.custom && annotations.value.custom.trim() !== '';
  if (hasCustomNote) {
    return true;
  }

  const lastResult = lastValidationResult.value;
  if (!lastResult) {
    return false;
  }

  const isStale = lastResult.correctFeatures.some(key => 
    lastResult.annotations[key] !== annotations.value[key]
  );
  return !isStale;
});

const handleClearMistakes = () => {
  emit('clear-mistakes');
}

// Open the popover when component mounts
onMounted(() => {
  nextTick(() => {
    console.log(props.language);
    isOpen.value = true;
  });
});

const handleClose = () => {
  isOpen.value = false
  annotations.value = {};
  validationResult.value = null;
  emit('close');
};

//helper func with check logic
const checkAnnotation = () => {
  const correctAnswer = props.wordData.morphology;
  if (!correctAnswer) {
    return {
      isCorrect: false,
      message: "No morphology data available for this word"
    };
  }
  
  const filledFeatures = Object.keys(annotations.value).filter(key => 
    key != 'custom' && annotations.value[key]);
  if (filledFeatures.length === 0) {
    return {
      isCorrect: false,
      message: "Please select at least one feature to check"
    };
  }
  
  const allCorrect = filledFeatures.every(key => 
    annotations.value[key] === correctAnswer[key]
  );
  
  const correctFeatures = filledFeatures.filter(key => 
    annotations.value[key] === correctAnswer[key]
  );
  if(annotations.value['custom']){
    correctFeatures.push('custom')
  } 

  const incorrectFeatures = filledFeatures.filter(key => 
    annotations.value[key] !== correctAnswer[key]
  );
  if (incorrectFeatures) {
    console.log(filledFeatures);
    incorrectFeatures.forEach(feature => {
      if (props.mistakeTracker[feature]) {
        props.mistakeTracker[feature]++;
      } else {
        props.mistakeTracker[feature] = 1;
      }
    });
  }
  
  const baseResult = {
    word: props.wordData.form,
    checkedFeatures: filledFeatures,
    correctFeatures,
    incorrectFeatures,
    annotations: { ...annotations.value }
  };

  if (allCorrect) {
    return {
      ...baseResult,
      isCorrect: true,
      message: `Correct! ${filledFeatures.map(f => featureLabels[f]).join(', ')} ✓`
    };
  } else {
    // Collect correct values for incorrect features for feedback
    const correctValues = {};
    incorrectFeatures.forEach(key => {
      correctValues[key] = correctAnswer[key] || "N/A";
    });

    return {
      ...baseResult,
      isCorrect: false,
      message: `Incorrect: ${incorrectFeatures.map(f => featureLabels[f]).join(', ')}`,
      correctValues
    };
  }
};

const validateAnnotation = () => {
  const result = checkAnnotation();

  validationResult.value = result; 

  if (result.correctFeatures && result.correctFeatures.length > 0) {
    lastValidationResult.value = result;
  }
  else {
    lastValidationResult.value = null;
  }

  emit('annotation-checked', result);
  if (result.isCorrect) {
    emit('annotation-correct', result);
  } else {
    emit('annotation-incorrect', result);
  }
};

const addAnnotation = () => {
  const result = lastValidationResult.value;
  const hasCustomNote = !!annotations.value.custom && annotations.value.custom.trim() !== '';

  if (!hasCustomNote && (!result || result.correctFeatures?.length === 0)) {
    console.log("result issue");
    validationResult.value = {
      isCorrect: false,
      message: "You must select at least one feature correctly before adding the annotation."
    };
    return;
  }

  const featuresToAdd = []
  // If they have validated grammar, grab those correct features
  if (result && result.correctFeatures) {
    result.correctFeatures.forEach(key => {
      featuresToAdd[key] = result.annotations[key];
    });
  }
  if (hasCustomNote) {
    featuresToAdd.custom = annotations.value.custom;
  }



  const annotation = {
    word: props.wordData.form,
    uid: props.wordData.uid,
    features: featuresToAdd
  }

  emit('annotation-added', annotation);
  console.log('emitted annotation');

  //reset state so user must re-validate to add new annotaiton
  lastValidationResult.value = null;
  
  return;
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

.popover-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.1);
  z-index: 40;
}

/* 1. The Wrapper - Holds them side-by-side */
.popover-wrapper {
  position: fixed;
  top: 150px;
  width: fit-content;
  height: auto;
  /* Use Flex to put Main and Sidecar next to each other */
  display: flex; 
  align-items: flex-start; /* Aligns them to the top */
  z-index: 50;
  max-width: 90vw; /* Prevent it from going off screen */
}

/* 2. The Main Box - Handles Resize & Scroll */
.popover-main {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  
  /* RESIZABILITY IS BACK */
  resize: both;
  overflow: auto; /* Required for resize to work */
  
  /* Initial dimensions */
  width: 14rem;
  height: auto;
  min-height: 300px;
  max-height: 80vh;
  
  display: flex;
  flex-direction: column;
}

/* 3. The Sidecar Container */
.popover-sidecar {
  flex-shrink: 0;
  position: static;
  display: flex;
  flex-direction: column; /* Toggle on top, panel below */
  align-items: flex-start;
  margin-left: 0; 
  z-index: auto;
}

.mistake-viewer {
  position: absolute;
  left: 100%;
  top: 0;
  height: 100%; /* Match the height of the shell */
  width: 14rem; /* Or whatever width you want */
  
  /* Hide it by default */
  display: none; 
  
  /* Styling */
  background-color: var(--hover-khaki); /* Slightly different color to distinguish */
  border-radius: 0 0.5rem 0.5rem 0;
  box-shadow: 5px 0 15px rgba(0,0,0,0.05);
  border-left: 1px solid #e2e8f0;
  padding-top: 2rem;
}

.mistake-viewer.open {
  display: block;
}

/* 4. The Toggle Button */
.mistake-viewer-toggle {
  position: absolute;
  left: 97%;
  top: 0;
  height: 50px;
  padding-left: 20px;
  z-index: -1;

  color: white;
  background-color: var(--green-button);
  border: none;
  border-radius: 8px;
}


.mistake-viewer-toggle:hover {
  background-color: var(--green-button-hover);
}

.mistake-viewer-toggle.mistake-viewer-open {
  z-index: 1;
  left: calc(100% + 14rem - 30px);
  padding-left: 5px;
  width: 30px;
  font-size: 115%;
  background-color: var(--delete-red);
}

.mistake-viewer-toggle.mistake-viewer-open:hover {
  background-color: var(--delete-red-hover);
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
  overflow-y: auto;    /* Scrolling happens here */
  display: flex;       /* Helps keep header sticky working */
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

.instruction-text {
  font-size: 0.875rem;
  color: var(--title-dark);
  margin-bottom: 1rem;
}

.form-fields {
  max-height: 50rem;
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

.field-textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: inherit; /* Keeps font consistent with selects */
  font-size: 0.9rem;
  min-height: 60px;
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
  border-color: var(--orange-button);
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

.btn-check {
  flex: 1;
  background-color: var(--green-button);
  color: white;
}

.btn-check:hover {
  background-color: var(--green-button-hover);
}

.btn-finish {
  padding-left: 1rem;
  padding-right: 1rem;
  background-color: #e5e7eb;
  color: #374151;
}

.btn-finish:hover {
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

<template>
  <span 
    ref="wordElement"
    :class="wordClasses"
    @mousedown="$emit('word-mousedown', wordData)"
    @mouseenter="$emit('word-mouseenter', wordData)"
    @mouseup="$emit('word-mouseup', wordData)"
    @click="$emit('word-click', wordData)"
    class="word-wrapper"
  >
    <span :class="['word', highlightClass, 
    {'syntax-hovered': isSyntaxHovered}, 
    {'syntax-pinned': isSyntaxPinned}, 
    {'syntax-hovered-and-pinned': isSyntaxHovered && isSyntaxPinned}]">
      {{ wordData.form + '\u00A0' + '\u00A0' }}
    </span>

    <span v-if="wordData.annotations" class="inline-annotations">
      <span class="annotation-tag" v-if="abbreviatedFeatures">
        {{ '\u00A0' + abbreviatedFeatures  + '\u00A0'}}
      </span>
    </span>

    <span v-if="wordData.annotations?.custom" class="custom-annotations">
      <span class="custom-annotation-tag" v-if="wordData.annotations.custom">
        {{ '\u00A0' + wordData.annotations.custom + '\u00A0'}}
      </span>
    </span>

    <button
      v-if="wordData.annotations"
      class="delete-button"
      @click.stop="$emit('word-delete', wordData)"
    >
    x
    </button>
  </span>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  activeRanges: {
    type: Array,
    default: () => []
  },
  wordData: {
    type: Object,
    required: true
  },
  features: {
    type: Object,
    required: true
  },
  isSelected: {
    type: Boolean,
    default: false
  },
  isSyntaxHovered: {
    type: Boolean
  },
  isSyntaxPinned: {
    type: Boolean
  }
});

const emit = defineEmits(['word-click', 'word-mouseup', 'word-mousedown', 'word-mouseenter', 'word-delete']);

const wordClasses = computed(() => {
  let classes = ['word'];
  
  if (props.isSelected) {
    classes.push('selected');
  }
  
  // Case highlighting
  if (props.features.caseHighlight) {
    if (props.wordData.morphology?.case) {
      const wordCase = props.wordData.morphology?.case;
      if (wordCase) {
        classes.push(`case-${wordCase}`);
      }
    }
  }
  
  // POS highlighting
  if (props.features.posHighlight) {
    if (props.wordData.morphology?.pos) {
      classes.push(`pos-${props.wordData.morphology?.pos}`);
    }
  }
  
  return classes.join(' ');
});

const highlightClass = computed(() => {
  const rangeCount = props.activeRanges.length;
  if (rangeCount === 0) return 'highlight-0';
  if (rangeCount === 1) return 'highlight-1';
  if (rangeCount === 2) return 'highlight-2';
  if (rangeCount >= 3) return 'highlight-3';
});

//TODO add greek!!
const abbreviationMap = {
  gender: { masculine: 'm', feminine: 'f', neuter: 'n' },
  number: { singular: 'sg', plural: 'pl' },
  case: { vocative: 'voc', nominative: 'nom', genitive: 'gen', dative: 'dat', accusative: 'acc', ablative: 'abl'},
  tense: { present: 'pres', future: 'fut', imperfect: 'impf', perfect: 'pf', 
    futureperfect: 'fpf', pluperfect: 'plpf'},
  mood: {indicative: 'indic', subjunctive: 'subj', imperative: 'imper', infinitive: 'inf'},
  voice: {active: 'act', passive: 'pass'},
  person: {1: '1', 2: '2', 3: '3'} //fix this prolly
};
  
const abbreviatedFeatures = computed(() => {
  const features = props.wordData.annotations;
  if (!features) return '';

  const { custom: _, ...feats } = features;

  console.log('Abbreviating', features);

  return Object.entries(feats)
    .map(([key, value]) => abbreviationMap[key]?.[value] || value)
    .join(' ');
});

</script>

<style scoped>
.word-wrapper {
  position: relative;
  display: inline-flex;
  flex-direction: column;
  padding: 0;
  margin: 0;
  font-size: 0;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.word {
  padding: 1px 0px;
  font-size: 1.1rem;
  font-family: var(--font-serif);
}

.word.syntax-hovered {
  background-color: var(--yellow-syntax-highlight);
}

.word.syntax-pinned {
  background-color: var(--yellow-syntax-highlight);
  border-bottom: 2px solid #ffc107;
}

.word.syntax-hovered-and-pinned {
  background-color: #ffdf80;
  border-bottom: 2px solid #ffc107;

}

.inline-annotations {
  display: inline-flex;
  flex-wrap: wrap; 
  gap: 3px;
  padding: 1px 0px;
  margin-top: -2px;
  min-height: 8px;
  font-family: system-ui;
}

.custom-annotations {
  display: flex;
  flex-wrap: wrap; 
  gap: 2px;
  padding: 1px 0px;
  margin-top: 2px; 
  min-height: 8px;
  font-family: system-ui;
}

.annotation-tag {
  font-size: 0.75rem;
  color: black;
  background-color: rgb(212, 254, 205); 
  border-radius: 3px;
  border-left: 1px solid green;
  border-right: 1px solid green;
  line-height: 1;
  white-space: nowrap; 
}

.custom-annotation-tag{
  font-size: 0.75rem;
  color: black;
  background-color: white; 
  border-left: 1px solid gray;
  border-right: 1px solid gray;
  border-radius: 3px;
  line-height: 1;
  white-space: nowrap; 
}

.delete-button {
  position: absolute;
  top: -8px;
  right: -8px;

  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  padding: 0;
  z-index: 10;

  opacity: 0;
  transition: opacity 0.2s ease;

  background-color: white;
  color: red;
  border-color: red;
}

.word-wrapper:hover .delete-button {
  opacity: 1;
}

.word-wrapper:hover {
  background-color: var(--hover-khaki);
  transform: translateY(-1px);
}

.word-wrapper.selected {
  background-color: var(--selected-khaki) !important;
  box-shadow: 0 0 0 2px var(--outline-khaki);
}

.highlight-1 {
  background-color: var(--highlight-1);

}
.highlight-2 {
  background-color: var(--highlight-2);
}
.highlight-3 {
  background-color: var(--highlight-3);
}

/* Case-based underline colors (for nouns/adjectives) */
.word-wrapper.case-nominative {
  border-bottom: 3px solid #ef4444;
}

.word-wrapper.case-genitive {
  border-bottom: 3px solid #f59e0b;
}

.word-wrapper.case-dative {
  border-bottom: 3px solid #eab308;
}

.word-wrapper.case-accusative {
  border-bottom: 3px solid #22c55e;
}

.word-wrapper.case-ablative {
  border-bottom: 3px solid #3b82f6;
}

.word-wrapper.case-vocative {
  border-bottom: 3px solid #a855f7;
}

/* Part of speech underline styles */
.word-wrapper.pos-noun {
  border-bottom: 3px solid #8b5cf6;
}

.word-wrapper.pos-verb {
  border-bottom: 3px dashed #ec4899;
}

.word.pos-adjective {
  border-bottom: 3px dotted #14b8a6;
}

.word.pos-adverb {
  border-bottom: 3px double #f59e0b;
}

.word.pos-pronoun {
  text-decoration: wavy underline #06b6d4;
  text-decoration-thickness: 3px;
}

.word.pos-preposition {
  border-bottom: 3px solid #84cc16;
}

.word.pos-conjunction {
  border-bottom: 3px solid #a3e635;
} 

</style>

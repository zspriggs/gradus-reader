<template>
  <span 
    :class="wordClasses"
    :style="syntaxStyle"
    @click="handleClick"
  >
    {{ wordData.word }}
  </span>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
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
  syntaxPhrase: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['word-click']);

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
    if (props.wordData.pos) {
      classes.push(`pos-${props.wordData.pos}`);
    }
  }
  
  return classes.join(' ');
});

const syntaxStyle = computed(() => {
  // Only show syntax highlighting if syntax feature is enabled
  if (props.features.syntax && props.syntaxPhrase) {
    const colors = {
      'indirect_question': 'rgba(251, 191, 36, 0.25)',
      'relative_clause': 'rgba(147, 51, 234, 0.25)',
      'indirect_statement': 'rgba(59, 130, 246, 0.25)',
      'ablative_absolute': 'rgba(34, 197, 94, 0.25)',
      'purpose_clause': 'rgba(236, 72, 153, 0.25)',
      'result_clause': 'rgba(249, 115, 22, 0.25)'
    };
    
    return {
      backgroundColor: colors[props.syntaxPhrase.type] || 'rgba(156, 163, 175, 0.25)',
      borderRadius: '3px',
      padding: '2px 0'
    };
  }
  return {};
});

const handleClick = () => {
  emit('word-click', props.wordData);
};
</script>

<style scoped>
.word {
  display: inline-block;
  padding: 2px 4px;
  margin: 0 2px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.word:hover {
  background-color: rgba(59, 130, 246, 0.15);
  transform: translateY(-1px);
}

.word.selected {
  background-color: rgba(59, 130, 246, 0.3) !important;
  box-shadow: 0 0 0 2px #3b82f6;
}

/* Case-based underline colors (for nouns/adjectives) */
.word.case-nominative {
  border-bottom: 3px solid #ef4444;
}

.word.case-genitive {
  border-bottom: 3px solid #f59e0b;
}

.word.case-dative {
  border-bottom: 3px solid #eab308;
}

.word.case-accusative {
  border-bottom: 3px solid #22c55e;
}

.word.case-ablative {
  border-bottom: 3px solid #3b82f6;
}

.word.case-vocative {
  border-bottom: 3px solid #a855f7;
}

/* Part of speech underline styles */
.word.pos-noun {
  border-bottom: 3px solid #8b5cf6;
}

.word.pos-verb {
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
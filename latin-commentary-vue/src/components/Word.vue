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
  level: {
    type: String,
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
  
  // Add morphology classes (underlines) for all levels
  if (props.wordData.pos === 'noun' || props.wordData.pos === 'adjective') {
    const wordCase = props.wordData.morphology?.case;
    if (wordCase) {
      classes.push(`case-${wordCase}`);
    }
  } else if (props.wordData.pos === 'verb') {
    classes.push('pos-verb');
  } else if (props.wordData.pos === 'adverb') {
    classes.push('pos-adverb');
  }
  
  return classes.join(' ');
});

const syntaxStyle = computed(() => {
  // Only show syntax highlighting for intermediate and advanced
  if ((props.level === 'intermediate' || props.level === 'advanced') && props.syntaxPhrase) {
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

/* Special styles for verbs and adverbs */
.word.pos-verb {
  border-bottom: 3px dashed #ec4899;
}

.word.pos-adverb {
  border-bottom: 3px dotted #14b8a6;
}
</style>
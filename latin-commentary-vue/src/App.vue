<template>
  <div class="app-container">
    <h1 class="main-title">Interactive Latin Commentary</h1>
    
    <DifficultySelector 
      :level="difficulty" 
      @level-change="handleLevelChange" 
    />
    
    <div class="passage-container">
      <h2 class="passage-title">{{ passageData.passage.title }}</h2>
      <div class="passage-text">
        <Word
          v-for="word in passageData.passage.text"
          :key="word.id"
          :word-data="word"
          :level="difficulty"
          :is-selected="selectedWord?.id === word.id"
          :syntax-phrase="getSyntaxPhraseForWord(word.id)"
          @word-click="handleWordClick"
        />
      </div>
      
      <div v-if="difficulty === 'beginner'" class="tip-text">
        💡 <strong>Tip:</strong> Colored underlines show grammatical cases. Click any word for details!
      </div>
      <div v-else-if="difficulty === 'intermediate'" class="tip-text">
        💡 <strong>Tip:</strong> Colored backgrounds show syntax phrases. Underlines show cases. Click for details!
      </div>
    </div>
    
    <AnnotationPanel 
      v-if="selectedWord"
      :word="selectedWord" 
      :level="difficulty" 
    />
    
    <!-- Legend -->
    <div class="legend-container">
      <h3>Legend</h3>
      <div class="legend-section">
        <h4>Morphology (Underlines):</h4>
        <div class="legend-items">
          <div class="legend-item">
            <span class="legend-example case-nominative">text</span>
            <span>Nominative</span>
          </div>
          <div class="legend-item">
            <span class="legend-example case-genitive">text</span>
            <span>Genitive</span>
          </div>
          <div class="legend-item">
            <span class="legend-example case-dative">text</span>
            <span>Dative</span>
          </div>
          <div class="legend-item">
            <span class="legend-example case-accusative">text</span>
            <span>Accusative</span>
          </div>
          <div class="legend-item">
            <span class="legend-example case-ablative">text</span>
            <span>Ablative</span>
          </div>
          <div class="legend-item">
            <span class="legend-example case-vocative">text</span>
            <span>Vocative</span>
          </div>
          <div class="legend-item">
            <span class="legend-example pos-verb">text</span>
            <span>Verb (dashed)</span>
          </div>
          <div class="legend-item">
            <span class="legend-example pos-adverb">text</span>
            <span>Adverb (dotted)</span>
          </div>
        </div>
      </div>
      <div v-if="difficulty === 'intermediate' || difficulty === 'advanced'" class="legend-section">
        <h4>Syntax (Highlights):</h4>
        <div class="legend-items">
          <div class="legend-item">
            <span class="legend-example syntax-indirect_question">text</span>
            <span>Indirect Question</span>
          </div>
          <div class="legend-item">
            <span class="legend-example syntax-relative_clause">text</span>
            <span>Relative Clause</span>
          </div>
          <div class="legend-item">
            <span class="legend-example syntax-indirect_statement">text</span>
            <span>Indirect Statement</span>
          </div>
          <div class="legend-item">
            <span class="legend-example syntax-ablative_absolute">text</span>
            <span>Ablative Absolute</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import DifficultySelector from './components/DifficultySelector.vue';
import Word from './components/Word.vue';
import AnnotationPanel from './components/AnnotationPanel.vue';
import passageData from './data/cicero-catiline-1.json';

const selectedWord = ref(null);
const difficulty = ref('beginner');

const handleWordClick = (word) => {
  selectedWord.value = word;
};

const handleLevelChange = (newLevel) => {
  difficulty.value = newLevel;
};

const getSyntaxPhraseForWord = (wordId) => {
  if (difficulty.value === 'beginner') return null;
  
  return passageData.passage.syntaxPhrases?.find(phrase => 
    phrase.wordIds.includes(wordId)
  ) || null;
};
</script>

<style>
.app-container {
  max-width: 1024px;
  margin: 0 auto;
  padding: 24px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
}

.main-title {
  font-size: 2rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 32px;
  color: #374151;
}

.passage-container {
  background-color: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.passage-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 16px;
  color: #374151;
}

.passage-text {
  font-size: 1.125rem;
  line-height: 2;
}

.tip-text {
  margin-top: 16px;
  font-size: 0.875rem;
  color: #6b7280;
}

/* Legend Styles */
.legend-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-top: 24px;
}

.legend-container h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 16px;
  color: #374151;
}

.legend-section {
  margin-bottom: 16px;
}

.legend-section h4 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #6b7280;
}

.legend-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
}

.legend-example {
  padding: 2px 8px;
  border-radius: 3px;
  font-family: Georgia, serif;
  font-weight: 500;
}

/* Case colors for legend */
.legend-example.case-nominative {
  border-bottom: 3px solid #ef4444;
}

.legend-example.case-genitive {
  border-bottom: 3px solid #f59e0b;
}

.legend-example.case-dative {
  border-bottom: 3px solid #eab308;
}

.legend-example.case-accusative {
  border-bottom: 3px solid #22c55e;
}

.legend-example.case-ablative {
  border-bottom: 3px solid #3b82f6;
}

.legend-example.case-vocative {
  border-bottom: 3px solid #a855f7;
}

.legend-example.pos-verb {
  border-bottom: 3px dashed #ec4899;
}

.legend-example.pos-adverb {
  border-bottom: 3px dotted #14b8a6;
}

/* Syntax phrase colors for legend */
.legend-example.syntax-indirect_question {
  background-color: rgba(251, 191, 36, 0.2);
  border: 1px solid rgba(251, 191, 36, 0.5);
}

.legend-example.syntax-relative_clause {
  background-color: rgba(147, 51, 234, 0.2);
  border: 1px solid rgba(147, 51, 234, 0.5);
}

.legend-example.syntax-indirect_statement {
  background-color: rgba(59, 130, 246, 0.2);
  border: 1px solid rgba(59, 130, 246, 0.5);
}

.legend-example.syntax-ablative_absolute {
  background-color: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.5);
}
</style>
<template>
  <div class="app-container">
    <!-- Sidebar toggle -->
    <button 
      class="sidebar-toggle" 
      @click="sidebarOpen = !sidebarOpen"
      :class="{ 'sidebar-open': sidebarOpen }"
    >
      <span v-if="!sidebarOpen">⚙️ Display Options</span>
      <span v-else>✕</span>
    </button>

    <!-- Sidebar -->
    <div class="sidebar" :class="{ 'open': sidebarOpen }">
      <div class="sidebar-content">
        <FeatureSelector 
          :features="features" 
          @toggle-feature="handleToggleFeature" 
        />
      </div>
    </div>

    <!-- Overlay for mobile -->
    <div 
      v-if="sidebarOpen" 
      class="sidebar-overlay"
      @click="sidebarOpen = false"
    ></div>

    <div class="main-content" :class="{'sidebar-open': sidebarOpen}"></div>
      <h1 class="main-title">Latin Commentary</h1>

      <div class="passage-container">
        <h2 class="passage-title">{{ passageData.passage.title }}</h2>
        <div class="passage-text">
          <Word
            v-for="word in passageData.passage.text"
            :key="word.id"
            :word-data="word"
            :features="features"
            :is-selected="selectedWord?.id === word.id"
            :syntax-phrase="getSyntaxPhraseForWord(word.id)"
            @word-click="handleWordClick"
          />
        </div>
      
        <div class="tip-text">
          <strong>Tip:</strong> Toggle display options to customize your view. Click any word for detailed annotations!
        </div>
      </div>
    
    <AnnotationPanel 
      v-if="selectedWord"
      :word="selectedWord" 
      :features="features" 
    />
    
    <!-- Legend -->
    <div class="legend-container">
      <h3>Legend</h3>
      <div v-if="features.caseHighlight" class="legend-section">
        <h4>Cases (Underlines):</h4>
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
        </div>
      </div>
      <div v-if="features.posHighlight" class="legend-section">
        <h4>Parts of Speech (Underlines):</h4>
        <div class="legend-items">
          <div class="legend-item">
            <span class="legend-example pos-noun">text</span>
            <span>Noun (solid)</span>
          </div>
          <div class="legend-item">
            <span class="legend-example pos-verb">text</span>
            <span>Verb (dashed)</span>
          </div>
          <div class="legend-item">
            <span class="legend-example pos-adjective">text</span>
            <span>Adjective (dotted)</span>
          </div>
          <div class="legend-item">
            <span class="legend-example pos-adverb">text</span>
            <span>Adverb (double)</span>
          </div>
          <div class="legend-item">
            <span class="legend-example pos-pronoun">text</span>
            <span>Pronoun (wavy)</span>
          </div>
        </div>
      </div>
      <div v-if="features.syntax" class="legend-section">
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
import { ref, reactive } from 'vue';
import FeatureSelector from './components/FeatureSelector.vue';
import Word from './components/Word.vue';
import AnnotationPanel from './components/AnnotationPanel.vue';
import passageData from './data/cicero-1.json';

const selectedWord = ref(null);
const sidebarOpen=ref(true);

const features = reactive({
  // Visual highlighting
  caseHighlight: true,
  posHighlight: false,
  syntax: false,
  
  // Annotation content
  vocab: true,
  morphology: true,
  style: false,
  rhetoric: false,
  etymology: false
});

const handleWordClick = (word) => {
  selectedWord.value = word;
};

const handleToggleFeature = (featureName) => {
  features[featureName] = !features[featureName];
};

const getSyntaxPhraseForWord = (wordId) => {
  if (!features.syntax) return null;
  
  return passageData.passage.syntaxPhrases?.find(phrase => 
    phrase.wordIds.includes(wordId)
  ) || null;
};
</script>

<style>
* {
  box-sizing: border-box;
}

.app-container {
  position: relative;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
}

/* Sidebar toggle button */
.sidebar-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1001;
  padding: 10px 16px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.sidebar-toggle:hover {
  background-color: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.15);
}

.sidebar-toggle.sidebar-open {
  background-color: #ef4444;
}

.sidebar-toggle.sidebar-open:hover {
  background-color: #dc2626;
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  right: -350px;
  width: 350px;
  height: 100vh;
  background-color: white;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease;
  z-index: 1000;
  overflow-y: auto;
}

.sidebar.open {
  right: 0;
}

.sidebar-content {
  padding: 80px 20px 20px 20px;
}

.sidebar-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #374151;
}

/* Sidebar overlay for mobile */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  display: none;
}

/* Main content */
.main-content {
  max-width: 1024px;
  margin: 0 auto;
  padding: 24px;
  transition: margin-left 0.3s ease;
}

@media (min-width: 1200px) {
  .main-content.sidebar-open {
    margin-right: 175px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 300px;
    right: -300px;
  }
  
  .sidebar-overlay {
    display: block;
  }
  
  .main-content.sidebar-open {
    margin-right: 0;
  }
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

/* POS styles for legend */
.legend-example.pos-noun {
  border-bottom: 3px solid #8b5cf6;
}

.legend-example.pos-verb {
  border-bottom: 3px dashed #ec4899;
}

.legend-example.pos-adjective {
  border-bottom: 3px dotted #14b8a6;
}

.legend-example.pos-adverb {
  border-bottom: 3px double #f59e0b;
}

.legend-example.pos-pronoun {
  border-bottom: 3px wavy #06b6d4;
  text-decoration: wavy underline #06b6d4;
  text-decoration-thickness: 3px;
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
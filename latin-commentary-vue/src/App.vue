<template>
  <div class="app-container">
    <MorphAnnotator
      v-if="selectedWord && features.inline"
      :wordData="selectedWord" 
      :features="features"
      @close="selectedWord = null"
      @annotation-added="handleAnnotationAdded" 
    />

    <!-- Sidebar toggle -->
    <button 
      class="sidebar-toggle" 
      @click="sidebarOpen = !sidebarOpen"
      :class="{ 'sidebar-open': sidebarOpen }"
    >
      <span v-if="!sidebarOpen">⚙️ Settings</span>
      <span v-else>x</span>
    </button>

    <!-- Sidebar -->
    <div class="sidebar" :class="{ 'open': sidebarOpen }">
      <div class="sidebar-content">
        <FeatureSelector 
          :features="features" 
          @toggle-feature="handleToggleFeature" 
          @import-annotations="importAnnotations"
          @export-annotations="exportAnnotations"
        />
      </div>
    </div>

    <!--Document selector toggle-->
    <button
      class="docselector-toggle"
      @click="docselectorOpen = !docselectorOpen"
      :class="{'docselector-open': docselectorOpen}"
    >
      <span v-if="!docselectorOpen"> Documents</span>
      <span v-else>x</span>
    </button>

    <div class="docselector" :class="{ 'open': docselectorOpen }">
      <div class="docselector-content">
        <DocumentSelector
          @document-selected="handleDocumentChange" 
        />
      </div>
    </div>

    <!-- Overlay for mobile -->
    <div 
      v-if="sidebarOpen" 
      class="sidebar-overlay"
      @click="sidebarOpen = false"
    ></div>

    <div v-if="passageData" class="main-content" :class="{'sidebar-open': sidebarOpen}">
      <h1 class="main-title">{{ passageData.passage.title}}</h1>

      <button class="prev-button"
        @click="prevSection"
        :class="{'hidden': docselectorOpen}"
      >🡸</button>

      <button class="next-button"
        @click="nextSection"
        :class="{'hidden': docselectorOpen}"
      >🡺</button>

      <div v-if="annotatedText" class="passage-container">
        <h2 class="passage-title">Section {{currentSection }}</h2>
        <div class="passage-text">
          <template 
            v-for="word in annotatedText[currentSection]"
            :key="word.uid"
          >
            <Word
              :word-data="word"
              :active-ranges="getActiveRanges(word.uid)"
              :features="features"
              :is-selected="selectedWord?.uid === word.uid"
              :syntax-phrase="getSyntaxPhraseForWord(word.uid)"
              @word-click="handleWordClick"
              @word-delete="handleWordAnnotationDelete"
              @word-mouseup="handleMouseUp"
              @word-mousedown="handleMouseDown"
              @word-mouseenter="handleMouseEnter"
            />
            <span 
              v-if="getRangesEndingAt(word.uid).length > 0" 
              class="line-note-icon"
              @click="(event) => openExistingRangeNote(word.uid, event)"
            >
              💬
            </span>
          </template>

          <div 
            v-if="showRangeInput && pendingAnnotation" 
            class="annotation-modal"
            @click.self="cancelRangeInput">
            <div class="modal-content">
              <h3>Add Note</h3>
              <textarea 
                v-model="pendingAnnotation.text" 
                class="modal-input"
                placeholder="Type your commentary here..."
              ></textarea>

              <div class="modal-actions">
                <button @click="cancelRangeInput" class="btn-cancel">Cancel</button>
                <button @click="saveRangeInput" class="btn-save">Save Note</button>
              </div>
            </div>
          </div>

          <div
            v-if="rangeView"
            class="range-note-tooltip"
            :style="{
              top: rangeViewPosition.top + 'px',
              left: rangeViewPosition.left + 'px'
            }"
          >
            <div class="tooltip-content">
              <button class="tooltip-close" @click="closeRangeNote">x</button>
              <div class="tooltip-text"> {{ rangeView.text }}</div>
              <button class="tooltip-delete" @click="handleRangeAnnotationDelete(rangeView)">Delete</button>
            </div>
          </div>
          <div 
            v-if="rangeView"
            class="tooltip-overlay"
            @click="closeRangeNote"
          ></div>
        </div>
        <div class="tip-text">
          <strong>Tip:</strong> Toggle display options to customize your view. Click any word for detailed annotations!
        </div>
      </div>
      
      <div v-else class="loading-screen">
        Loading library...
      </div>
    
    <AnnotationPanel 
      v-if="selectedWord && !features.inline"
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
      <!-- <div v-if="features.syntax" class="legend-section">
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
      </div> -->
    </div>
  </div>
  </div>

</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import FeatureSelector from './components/FeatureSelector.vue';
import Word from './components/Word.vue';
import AnnotationPanel from './components/AnnotationPanel.vue';
import MorphAnnotator from './components/MorphAnnotator.vue';
import DocumentSelector from './components/DocumentSelector.vue';
import { annotationStorage } from './utils/annotationStorage.js';

const currentUrn = ref(''); 
const passageData = ref(null); 
const currentSection = ref('1.1'); //default
const availableSections = computed(() => Object.keys(passageData?.value.text));

const allAnnotations = ref({});
const selectedWord = ref(null);

const sidebarOpen = ref(false);
const docselectorOpen=ref(false);

const isDragging = ref(false);
const dragStart = ref(null);
const dragEnd = ref(null);

const pendingAnnotation = ref(null);
const showRangeInput = ref(false);

const rangeView = ref(null);
const rangeViewPosition = ref({top: 0, left: 0});



const features = reactive({
  inline: true,
  line: false,
  
  // Visual highlighting
  caseHighlight: true,
  posHighlight: false,
  syntax: false,
  
  // Annotation content - TODO remove unused
  // vocab: true,
  morphology: true,
  // syntax: false
});

onMounted(() => {
  allAnnotations.value = annotationStorage.load();
});

watch(allAnnotations, (newValue) => {
  console.log("Syncing to localStorage...");
  annotationStorage.save(newValue);
}, { deep: true }); 

const annotatedText = computed(() => {
  const docURN = currentUrn.value;
  if (!docURN ||!passageData.value || !passageData.value.passage){ return; }

  const savedAnnotations = allAnnotations.value[docURN] || {};
  
  const sections = {};
  Object.keys(passageData.value.text).forEach(sectionKey => {
    sections[sectionKey] = passageData.value.text[sectionKey].map(word => {
      return {
        ...word,
        annotations: savedAnnotations[word.uid] || null
      };
    });
  });

  return sections;
});

const handleAnnotationAdded = (newAnnotation) => {
  const targetWord  = passageData.value.text[currentSection.value].find(w => w.uid === newAnnotation.uid);
  if (targetWord) {
    targetWord.annotations = {
      ...targetWord.annotations,
      ...newAnnotation.features
    }

    const docURN = currentUrn.value;
    if(!allAnnotations.value[docURN]) {
      allAnnotations.value[docURN] = {};
    }
    allAnnotations.value[docURN][targetWord.uid] = targetWord.annotations;
    //console.log("Added annotation to:", targetWord.form, targetWord.annotations);
  }
};

const handleDocumentChange = (newDocument) => {
  console.log('handledocchange')
  currentUrn.value = newDocument.urn
  passageData.value = newDocument.data;
  currentSection.value = Object.keys(passageData.value.text)[0]; // Reset to first!
  selectedWord.value = null;
};

const exportAnnotations = () => {
  annotationStorage.export();
};

const importAnnotations = () => {  
  annotationStorage.import((newData) => {
    const merged = { ...allAnnotations.value };

    for (const urn in newData) {
      if (merged[urn]) {
        merged[urn] = {
          ...merged[urn],    // Keep existing words
          ...newData[urn]    // Add imported words
        };
      } else {
        merged[urn] = newData[urn];
      }
    }

    allAnnotations.value = merged;
  });
};

const nextSection = () => {
  const index = availableSections.value.indexOf(currentSection.value);
  if (index < availableSections.value.length - 1) {
    currentSection.value = availableSections.value[index + 1];
  }
};

const prevSection = () => {
  const index = availableSections.value.indexOf(currentSection.value);
  if (index > 0) {
    currentSection.value = availableSections.value[index - 1];
  }
};

const getRangesEndingAt = (uid) => {
  const docURN = currentUrn.value;
  const docAnnos = allAnnotations.value[docURN] || {};
  
  return Object.values(docAnnos).filter(anno => 
    anno.type === 'range' && anno.enduid === uid
  );
};

const getActiveRanges = (uid) => {
  const docURN = currentUrn.value;
  const docAnnos = allAnnotations.value[docURN] || {};
  
  return Object.values(docAnnos).filter(anno => 
    anno.type === 'range' && anno.uids.includes(uid)
  );
};

const openExistingRangeNote = (uid, event) => {
  const ranges = getRangesEndingAt(uid);
  if(ranges.length > 0) {
    //TODO: fix this, add support for showing multiple annotations
    rangeView.value = ranges[0];
  }
  else {console.log("huh??");}

  const rect = event.target.getBoundingClientRect();
  rangeViewPosition.value = {
    top: rect.bottom + window.scrollY + 2,
    left: rect.left + window.scrollX
  };

  console.log("idk man I tried ", rangeView)
};

const closeRangeNote = () => {
  rangeView.value = null;
}

const handleWordClick = (word) => {
  selectedWord.value = word;
};

const handleWordAnnotationDelete = (word) => {
  const urn = currentUrn.value;
  word.annotations = null;

  if(allAnnotations.value[urn]) {
    delete allAnnotations.value[urn][word.uid];
  }

  console.log("Removed annotations from:", word.form);
};

const handleRangeAnnotationDelete = (rangeAnnotation) => {
  const urn = currentUrn.value;
  if(allAnnotations.value[urn]) {
    delete allAnnotations.value[urn][rangeAnnotation.id];
  }
  console.log("Removed range annotation");
};

const handleMouseDown = (word) => {
  console.log("mouse down")
  isDragging.value = true;
  dragStart.value = word.uid;
  dragEnd.value = word.uid;
};

const handleMouseEnter = (word) => {
  if(isDragging.value) {
    dragEnd.value = word.uid;
  }
};

const handleMouseUp = (word) => {
  console.log("mouse up");
  if(isDragging.value && dragStart.value !== dragEnd.value) {
    saveRangeAnnotation(dragStart.value, dragEnd.value);
    console.log("saveannotation");
  }
  isDragging.value = false;
  dragStart.value = null;
  dragEnd.value = null;
};

const saveRangeAnnotation = (startUID, endUID) => {
  const section = passageData.value.text[currentSection.value];
  const startIndex = section.findIndex(w => w.uid === startUID);
  const endIndex = section.findIndex(w => w.uid === endUID);

  const realStartIndex = startIndex < endIndex ? startIndex : endIndex;
  const realEndIndex = startIndex < endIndex ? endIndex : startIndex;

  const selectedWords = section.slice(realStartIndex, realEndIndex).map(w => w.uid);

  const id = `range.${pendingAnnotation.value.startuid}.${pendingAnnotation.value.enduid}`

  openInput({
    id: id,
    uids: selectedWords,
    startuid: section[realStartIndex].uid,
    enduid: section[realEndIndex].uid,
    text: ""
  });
};

const handleToggleFeature = (featureName) => {
  features[featureName] = !features[featureName];
};

const getSyntaxPhraseForWord = (wordId) => {
  if (!features.syntax) return null;
  
  return passageData.value.passage.syntaxPhrases?.find(phrase => 
    phrase.wordIds.includes(wordId)
  ) || null;
};

const openInput = ({id, uids, startuid, enduid, text}) => {
  pendingAnnotation.value = {
    id, uids, startuid, enduid, text, type: 'range'
  };

  showRangeInput.value = true;
};

const cancelRangeInput = () => {
  showRangeInput.value = false;
  pendingAnnotation.value = null;
};

const saveRangeInput = () => {
  const docURN = currentUrn.value;
  if(!pendingAnnotation.value){return;}

  if(!allAnnotations.value[docURN]){
    allAnnotations.value[docURN] = {};
  }

  allAnnotations.value[docURN][pendingAnnotation.id] = {
    ...pendingAnnotation.value
  };

  showRangeInput.value = false;
  pendingAnnotation.value = null;
};

</script>

<style>
* {
  box-sizing: border-box;
}

.app-container {
  position: relative;
  min-height: 100vh;
  font-family: 'EB Garamond', 'Garamond', 'Georgia', 'Times New Roman', serif;
}

/* doc selector toggle */
.docselector-toggle {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1001;
  padding: 10px 16px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.docselector-toggle:hover {
  background-color: #2563eb;
  transform: translateY(-1px);
}

.docselector-toggle.docselector-open {
  background-color: #ef4444;
}

.docselector-toggle.docselector-open:hover {
  background-color: #dc2626;
}

.docselector {
  position: fixed;
  top: 0;
  left: -400px;
  width: 350px;
  height: 100vh;
  background-color: white;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  transition: left 0.3s ease;
  z-index: 1000;
  overflow-y: auto;
}

.docselector.open {
  left: 0;
}

.docselector-content {
  padding: 80px 20px 20px 20px;
}

.docselector-title {
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
  transition: all 0.2s;
}

.sidebar-toggle:hover {
  background-color: #2563eb;
  transform: translateY(-1px);
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

.next-button,
.prev-button {
  position: fixed;
  top: 80px;
  z-index: 1002;
  background-color: #19d3bd;
  color: black;
  padding: 5px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.next-button {
  left: 92px;
}

.prev-button {
  left: 20px;
}

.next-button:hover, 
.prev-button:hover {
  background-color: #13ac9a;
}

.prev-button.hidden,
.next-button.hidden {
  display: none !important;
}

.annotation-modal {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(255, 255, 255, 0.2); 
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  resize: both;
}

.modal-input {
  background: white;
  width: 100%;
  height: 80px; 
  padding: 0px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.9rem;
  resize: none; 
  outline: none;
}

.modal-input:focus {
  border-color: #3b82f6;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}

.btn-cancel {
  background: transparent;
  border: none;
  border-radius: 4px;
  color: #6b7280;
  font-size: 0.8rem;
  cursor: pointer;
}

.btn-cancel:hover {
  background: rgb(212, 212, 212);
}

.btn-save {
  background: #639efc;
  color: white;
  border: none;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-save:hover {
    background: #3b82f6;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.annotation-input-area {
  width: 100%;
  height: 120px;
  margin: 12px 0;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-family: inherit;
}

.line-note-icon {
  cursor: pointer;
  font-size: 9pt;
}

.line-note-icon:hover {
  font-size: 11pt;
}

.tooltip-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1999; /* Just below the tooltip */
  background: transparent;
}

.range-note-tooltip {
  position: absolute;
  z-index: 2000;
  max-width: 300px;
}

.tooltip-content {
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  position: relative;
}

.tooltip-close {
  position: absolute;
  top: 4px;
  right: 4px;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  line-height: 24px;
}

.tooltip-close:hover {
  color: #374151;
}

.tooltip-text {
  font-size: 0.9rem;
  line-height: 1.5;
  color: #374151;
  padding-right: 20px; /* Space for the close button */
}

.tooltip-delete {
  font-family: inherit;
  background-color: rgb(255, 167, 167);
  border: none;
  border-radius: 4px;
}

.tooltip-delete:hover {
  background-color: rgb(255, 100, 100);
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
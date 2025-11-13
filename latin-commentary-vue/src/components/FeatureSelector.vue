<template>
  <div class="feature-selector">
    <h3>Display Options:</h3>
    <div class="feature-toggles">
      <div class="feature-group">
        <h4> Morphology Annotations </h4>
        <input 
          type="checkbox" 
          id="annotations-toggle" 
          :checked="features.annotations"
          @change="handleToggle('annotations')"
        />
      </div>

      <div class="feature-group">
        <h4>Visual Highlighting</h4>
        <label 
          v-for="feature in visualFeatures"
          :key="feature.key"
          class="feature-toggle"
        >
          <input
            type="checkbox"
            :checked="features[feature.key]"
            @change="handleToggle(feature.key)"
          />
          <span class="feature-label">
            {{ feature.label }}
          </span>
          <span class="feature-description">{{ feature.description }}</span>
        </label>
      </div>
      
      <div class="feature-group">
        <h4>Annotation Content</h4>
        <label 
          v-for="feature in contentFeatures"
          :key="feature.key"
          class="feature-toggle"
        >
          <input
            type="checkbox"
            :checked="features[feature.key]"
            @change="handleToggle(feature.key)"
          />
          <span class="feature-label">
            {{ feature.label }}
          </span>
          <span class="feature-description">{{ feature.description }}</span>
        </label>
      </div>
    </div>
    
    <div class="preset-buttons">
      <button @click="setPreset('beginner')" class="preset-btn">
        📚 Beginner Preset
      </button>
      <button @click="setPreset('intermediate')" class="preset-btn">
        📖 Intermediate Preset
      </button>
      <button @click="setPreset('advanced')" class="preset-btn">
        🎓 Advanced Preset
      </button>
      <button @click="setPreset('all')" class="preset-btn">
        ⚡ Show All
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  features: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['toggle-feature']);

const visualFeatures = [
  { 
    key: 'caseHighlight', 
    label: 'Case Highlighting', 
    description: 'Color-coded underlines for grammatical cases'
  },
  { 
    key: 'posHighlight', 
    label: 'Part of Speech', 
    description: 'Different underline styles for nouns, verbs, etc.'
  },
  { 
    key: 'syntax', 
    label: 'Syntax Phrases', 
    description: 'Highlighted background for clauses and constructions'
  }
];

const contentFeatures = [
  { 
    key: 'vocab', 
    label: 'Vocabulary', 
    description: 'Word meanings and translations'
  },
  { 
    key: 'morphology', 
    label: 'Morphology', 
    description: 'Detailed grammatical analysis'
  },
  { 
    key: 'style', 
    label: 'Style', 
    description: 'Literary and stylistic notes'
  },
  { 
    key: 'rhetoric', 
    label: 'Rhetoric', 
    description: 'Rhetorical devices and techniques'
  }
];

const handleToggle = (featureName) => {
  emit('toggle-feature', featureName);
};

const setPreset = (presetName) => {
  const presets = {
    beginner: {
      caseHighlight: true,
      posHighlight: false,
      syntax: false,
      vocab: true,
      morphology: true,
      style: false,
      rhetoric: false,
      etymology: false
    },
    intermediate: {
      caseHighlight: true,
      posHighlight: false,
      syntax: true,
      vocab: true,
      morphology: true,
      style: true,
      rhetoric: false,
      etymology: false
    },
    advanced: {
      caseHighlight: false,
      posHighlight: false,
      syntax: true,
      vocab: false,
      morphology: true,
      style: true,
      rhetoric: true,
      etymology: true
    },
    all: {
      caseHighlight: true,
      posHighlight: true,
      syntax: true,
      vocab: true,
      morphology: true,
      style: true,
      rhetoric: true,
      etymology: true
    }
  };
  
  const preset = presets[presetName];
  Object.keys(preset).forEach(key => {
    if (props.features[key] !== preset[key]) {
      emit('toggle-feature', key);
    }
  });
};
</script>

<style scoped>
.feature-selector {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.feature-selector h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 16px;
  color: #374151;
}

.feature-toggles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.feature-group h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
}

.feature-toggle {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
  border: 1px solid #e5e7eb;
}

.feature-toggle:hover {
  background-color: #f9fafb;
}

.feature-toggle input[type="checkbox"] {
  margin-right: 8px;
  cursor: pointer;
  width: 18px;
  height: 18px;
}

.feature-label {
  display: flex;
  align-items: center;
  font-weight: 500;
  color: #374151;
  font-size: 0.95rem;
}

.feature-icon {
  margin-right: 6px;
  font-size: 1.1rem;
}

.feature-description {
  font-size: 0.8rem;
  color: #6b7280;
  margin-left: 26px;
}

.preset-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.preset-btn {
  padding: 8px 16px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  background-color: white;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.preset-btn:hover {
  background-color: #f3f4f6;
  border-color: #9ca3af;
}

.preset-btn:active {
  background-color: #e5e7eb;
}

@media (max-width: 768px) {
  .feature-toggles {
    grid-template-columns: 1fr;
  }
  
  .preset-buttons {
    flex-direction: column;
  }
  
  .preset-btn {
    width: 100%;
  }
}
</style>
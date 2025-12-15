<template>
  <div class="document-selector">
    <label for="doc-select">Select a text:</label>
    <select 
      id="doc-select"
      v-model="selectedURN"
      @change="loadDocument"
      class="doc-dropdown"
    >
      <optgroup 
        v-for="(docs, language) in documents" 
        :key="language"
        :label="language"
      >
        <option 
          v-for="doc in docs" 
          :key="doc.urn" 
          :value="doc.urn"
        >
          {{ doc.title }}
        </option>
      </optgroup>
    </select>
  </div>
</template>

<script setup>

import {ref, reactive} from 'vue';
import ciceroData from '../data/phi0474.phi013.perseus-lat1.json'
import homerData from '../data/tlg0012.tlg001.perseus-grc1.json'

const emit = defineEmits(['document-selected']);
const documents = {
    Latin: [
        {urn: 'phi0474.phi013', title: 'Cicero - In Catilinam', data: ciceroData}
    ],
    Greek: [
        {urn: 'tlg0012.tlg001', title: 'Homer - Iliad', data: homerData}
    ]
};

const selectedURN = ref('phi0474.phi013');
const selectedData = reactive(ciceroData);

const loadDocument = () => {
  // Find the selected document across all languages
  const allDocs = Object.values(documents).flat();
  const doc = allDocs.find(d => d.urn === selectedURN.value);
  
  console.log("loading document", doc.title)

  if (doc && doc.data) {
    // Replace passageData with new document
    selectedData.value = { ...doc.data };
    emit('document-selected', doc.data)
    console.log('Loaded:', doc.title);
  }
};

//emits the initial document
loadDocument();

</script>


<style scoped>
.document-selector {
  margin-bottom: 20px;
  padding: 16px;
  background-color: #f9fafb;
  border-radius: 8px;
}

.doc-dropdown {
  width: 100%;
  padding: 8px 12px;
  border: 2px solid #3b82f6;
  border-radius: 6px;
  font-size: 0.95rem;
  margin-top: 8px;
  cursor: pointer;
}

.doc-dropdown:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}
</style>
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

import {ref, onMounted} from 'vue';
import ciceroInCatilinam1 from '../data/phi0474.phi013.perseus-lat1.tb.json';
import homerIliad from '../data/tlg0012.tlg001.perseus-grc1.tb.json';
import herodotusHistories1 from '../data/tlg0016.tlg001.perseus-grc1.1.tb.json';
import xenophonMemorabilia from '../data/v1.0032-002.json';

const emit = defineEmits(['document-selected']);

const documents = {
  Latin: [
    {urn: 'phi0474.phi013', lang: 'lat', title: 'Cicero - In Catilinam', data: ciceroInCatilinam1}
  ],
  Greek: [
    {urn: 'tlg0012.tlg001', lang: 'grc', title: 'Homer - Iliad', data: homerIliad},    
    {urn: 'tlg0016.tlg001', lang: 'grc', title: 'Herodotus - Histories', data: herodotusHistories1},
    {urn: '0032.002', lang: 'grc', title: 'Xenophon - Memorabilia', data: xenophonMemorabilia}
  ]
};

const selectedURN = ref('phi0474.phi013');
const selectedData = ref(ciceroInCatilinam1);

onMounted(() => {
  loadDocument();
});

const loadDocument = () => {
  console.log('tring to load doc')
  // Find the selected document across all languages
  const allDocs = Object.values(documents).flat();
  const doc = allDocs.find(d => d.urn === selectedURN.value);
  
  console.log("loading document", doc.title)

  if (doc && doc.data) {
    selectedData.value = doc.data;
    emit('document-selected', {
      urn: doc.urn,
      lang: doc.lang,
      data: doc.data}
    )
    console.log('Loaded:', doc.title);
  }
};


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
<template>
  <div class="document-selector">
  <p><strong>Note:</strong> Please inspect the available sections carefully. Since Juno is built on treebanks, 
    not all sections will be available.</p>
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
    <label class="section-select-label" for="section-select">Select a section:</label>
    <select
      id="section-select"
      v-model="selectedSection"
      @change="changeSection"
      class="doc-dropdown"
    >
      <option
        v-for="section in availableSections"
        :key="section"
        :value="section"
      >
        {{ section }}
      </option>
    </select>
  </div>
</template>

<script setup>

import {ref, onMounted, computed} from 'vue';

//grc
import xenophonMemorabilia from '../data/0032-002.json';

import thucydidesPeloponnesianWar from '../data/Greek/tlg0003.tlg001.perseus-grc1.1.tb.json';
import plutarchLycurgus from '../data/Greek/tlg0007.tlg004.perseus-grc1.tb.json';
import plutarchAlcibiades from '../data/Greek/tlg0007.tlg015.perseus-grc1.tb.json';
import athenaeusDeipnosophistae12 from '../data/Greek/tlg0008.tlg001.perseus-grc1.12.tb.json';
import athenaeusDeipnosophistae13 from '../data/Greek/tlg0008.tlg001.perseus-grc1.13.tb.json';
import homerIliad from '../data/Greek/tlg0012.tlg001.perseus-grc1.tb.json';
import homerOdyssey from '../data/Greek/tlg0012.tlg002.perseus-grc1.tb.json';
import herodotusHistories from '../data/Greek/tlg0016.tlg001.perseus-grc1.1.tb.json';
import hesiodTheogony from '../data/Greek/tlg0020.tlg001.perseus-grc1.tb.json';
import hesiodShieldOfHeracles from '../data/Greek/tlg0020.tlg003.perseus-grc1.tb.json';
import platoEuthyphro from '../data/Greek/tlg0059.tlg001.perseus-grc1.tb.json';
import diodorusSiculusLibrary from '../data/Greek/tlg0060.tlg001.perseus-grc3.11.tb.json';
import origenesContraCelsum from '../data/Greek/tlg0096.tlg002.opp-grc2.1-53.tb.json';
import lysiasMurderOfEratosthenes from '../data/Greek/tlg0540.tlg001.perseus-grc1.tb.json';
import lysiasAgainstAlcibiadesDeserting from '../data/Greek/tlg0540.tlg014.perseus-grc1.tb.json';
import lysiasAgainstAlcibiadesRefusal from '../data/Greek/tlg0540.tlg015.perseus-grc1.tb.json';
import lysiasAgainstPancleon from '../data/Greek/tlg0540.tlg023.perseus-grc1.tb.json';
import polybiusHistories from '../data/Greek/tlg0543.tlg001.perseus-grc1.tb.json';
import apollodorusLibrary from '../data/Greek/tlg0548.tlg001.perseus-grc1.1.1.1-1.4.1.tb.json';

// TODO delete these ones that Not included due to processing issues
//import homericHymnsDemeter from '../data/Greek/tlg0013.tlg002.perseus-grc1.tb.json';
// import sophoclesTrachiniae from '../data/Greek/tlg0011.tlg001.perseus-grc2.tb.json';
// import sophoclesAntigone from '../data/Greek/tlg0011.tlg002.perseus-grc2.tb.json';
// import sophoclesAjax from '../data/Greek/tlg0011.tlg003.perseus-grc1.tb.json';
// import sophoclesOedipusTyrannus from '../data/Greek/tlg0011.tlg004.perseus-grc1.tb.json';
// import sophoclesElectra from '../data/Greek/tlg0011.tlg005.perseus-grc2.tb.json';
// import aeschylusSupplices from '../data/Greek/tlg0085.tlg001.perseus-grc2.tb.json';
// import aeschylusPersians from '../data/Greek/tlg0085.tlg002.perseus-grc2.tb.json';
// import aeschylusPrometheusBound from '../data/Greek/tlg0085.tlg003.perseus-grc2.tb.json';
// import aeschylusSevenAgainstThebes from '../data/Greek/tlg0085.tlg004.perseus-grc2.tb.json';
// import aeschylusAgamemnon from '../data/Greek/tlg0085.tlg005.perseus-grc1.tb.json';
// import aeschylusLibationBearers from '../data/Greek/tlg0085.tlg006.perseus-grc2.tb.json';
// import aeschylusEumenides from '../data/Greek/tlg0085.tlg007.perseus-grc1.tb.json';
//import hesiodWorksAndDays from '../data/Greek/tlg0020.tlg002.perseus-grc1.tb.json';

//lat
import caesarBelloGallico from '../data/Latin/phi0448.phi001.perseus-lat1.tb.json';
import ciceroInCatilinam from '../data/Latin/phi0474.phi013.perseus-lat1.tb.json';
import sallustBellumCatilinae from '../data/Latin/phi0631.phi001.perseus-lat1.tb.json';
import ovidMetamorphoses from '../data/Latin/phi0959.phi006.perseus-lat1.tb.json';
import petroniusSatyricon from '../data/Latin/phi0972.phi001.perseus-lat1.tb.json';
import suetoniusLifeOfAugustus from '../data/Latin/phi1348.abo012.perseus-lat1.tb.json';
import jeromeVulgata from '../data/Latin/tlg0031.tlg027.perseus-lat1.tb.json';
//import augustusResGestae from '../data/Latin/phi1221.phi007.perseus-lat1.tb.json';
//import tacitusHistoriae from '../data/Latin/phi1351.phi005.perseus-lat1.tb.json';

const emit = defineEmits(['document-selected', 'section-selected']);

const props = defineProps({
  availableSections: {
    type: Object,
    required: true
  }
});

const documents = {
Latin: [
    //{ urn: 'phi1221.phi007', lang: 'lat', title: 'Augustus - Res Gestae', data: augustusResGestae },
    //{ urn: 'phi1351.phi005', lang: 'lat', title: 'Tacitus - Historiae', data: tacitusHistoriae },
    { urn: 'phi0448.phi001', lang: 'lat', title: 'Caesar - Commentarii de Bello Gallico', data: caesarBelloGallico },
    { urn: 'phi0474.phi013', lang: 'lat', title: 'Cicero - In Catilinam', data: ciceroInCatilinam },
    { urn: 'tlg0031.tlg027', lang: 'lat', title: 'Jerome - Vulgata', data: jeromeVulgata },
    { urn: 'phi0959.phi006', lang: 'lat', title: 'Ovid - Metamorphoses', data: ovidMetamorphoses },
    { urn: 'phi0972.phi001', lang: 'lat', title: 'Petronius - Satyricon', data: petroniusSatyricon },
    { urn: 'phi0631.phi001', lang: 'lat', title: 'Sallust - Bellum Catilinae', data: sallustBellumCatilinae },
    { urn: 'phi1348.abo012', lang: 'lat', title: 'Suetonius - Life of Augustus', data: suetoniusLifeOfAugustus },
  ],
  Greek: [
    { urn: '0032.002', lang: 'grc', title: 'Xenophon - Memorabilia', data: xenophonMemorabilia },
    { urn: 'tlg0003.tlg001', lang: 'grc', title: 'Thucydides - History of the Peloponnesian War', data: thucydidesPeloponnesianWar },
    { urn: 'tlg0007.tlg004', lang: 'grc', title: 'Plutarch - Lycurgus', data: plutarchLycurgus },
    { urn: 'tlg0007.tlg015', lang: 'grc', title: 'Plutarch - Alcibiades', data: plutarchAlcibiades },
    { urn: 'tlg0008.tlg001', lang: 'grc', title: 'Athenaeus of Naucratis - Deipnosophistae 12', data: athenaeusDeipnosophistae12 },
    { urn: 'tlg0008.tlg001', lang: 'grc', title: 'Athenaeus of Naucratis - Deipnosophistae 13', data: athenaeusDeipnosophistae13 },
    { urn: 'tlg0012.tlg001', lang: 'grc', title: 'Homer - Iliad', data: homerIliad },
    { urn: 'tlg0012.tlg002', lang: 'grc', title: 'Homer - Odyssey', data: homerOdyssey },
    { urn: 'tlg0016.tlg001', lang: 'grc', title: 'Herodotus - Histories', data: herodotusHistories },
    { urn: 'tlg0020.tlg001', lang: 'grc', title: 'Hesiod - Theogony', data: hesiodTheogony },
    { urn: 'tlg0020.tlg003', lang: 'grc', title: 'Hesiod - Shield of Heracles', data: hesiodShieldOfHeracles },
    { urn: 'tlg0059.tlg001', lang: 'grc', title: 'Plato - Euthyphro', data: platoEuthyphro },
    { urn: 'tlg0060.tlg001', lang: 'grc', title: 'Diodorus Siculus - Historical Library', data: diodorusSiculusLibrary },
    { urn: 'tlg0096.tlg002', lang: 'grc', title: 'Origenes - Contra Celsum', data: origenesContraCelsum },
    { urn: 'tlg0540.tlg001', lang: 'grc', title: 'Lysias - On the Murder of Eratosthenes', data: lysiasMurderOfEratosthenes },
    { urn: 'tlg0540.tlg014', lang: 'grc', title: 'Lysias - Against Alcibiades: For Deserting the Ranks', data: lysiasAgainstAlcibiadesDeserting },
    { urn: 'tlg0540.tlg015', lang: 'grc', title: 'Lysias - Against Alcibiades: For Refusal of Military Service', data: lysiasAgainstAlcibiadesRefusal },
    { urn: 'tlg0540.tlg023', lang: 'grc', title: 'Lysias - Against Pancleon', data: lysiasAgainstPancleon },
    { urn: 'tlg0543.tlg001', lang: 'grc', title: 'Polybius - Histories', data: polybiusHistories },
    { urn: 'tlg0548.tlg001', lang: 'grc', title: 'Apollodorus - Library', data: apollodorusLibrary }

    //{ urn: 'tlg0013.tlg002', lang: 'grc', title: 'Homeric Hymns - Hymn 2 to Demeter', data: homericHymnsDemeter },
    //{ urn: 'tlg0020.tlg002', lang: 'grc', title: 'Hesiod - Works and Days', data: hesiodWorksAndDays },
    // { urn: 'tlg0085.tlg001', lang: 'grc', title: 'Aeschylus - Supplices', data: aeschylusSupplices },
    // { urn: 'tlg0085.tlg002', lang: 'grc', title: 'Aeschylus - Persians', data: aeschylusPersians },
    // { urn: 'tlg0085.tlg003', lang: 'grc', title: 'Aeschylus - Prometheus Bound', data: aeschylusPrometheusBound },
    // { urn: 'tlg0085.tlg004', lang: 'grc', title: 'Aeschylus - Seven Against Thebes', data: aeschylusSevenAgainstThebes },
    // { urn: 'tlg0085.tlg005', lang: 'grc', title: 'Aeschylus - Agamemnon', data: aeschylusAgamemnon },
    // { urn: 'tlg0085.tlg006', lang: 'grc', title: 'Aeschylus - Libation Bearers', data: aeschylusLibationBearers },
    // { urn: 'tlg0085.tlg007', lang: 'grc', title: 'Aeschylus - Eumenides', data: aeschylusEumenides },
    // { urn: 'tlg0011.tlg001', lang: 'grc', title: 'Sophocles - Trachiniae', data: sophoclesTrachiniae },
    // { urn: 'tlg0011.tlg002', lang: 'grc', title: 'Sophocles - Antigone', data: sophoclesAntigone },
    // { urn: 'tlg0011.tlg003', lang: 'grc', title: 'Sophocles - Ajax', data: sophoclesAjax },
    // { urn: 'tlg0011.tlg004', lang: 'grc', title: 'Sophocles - Oedipus Tyrannus', data: sophoclesOedipusTyrannus },
    // { urn: 'tlg0011.tlg005', lang: 'grc', title: 'Sophocles - Electra', data: sophoclesElectra },
  ]
};

const selectedURN = ref('phi0474.phi013');
const selectedSection = ref('1.1');
const selectedData = ref(ciceroInCatilinam);

const availableSections = computed(() => Object.keys(selectedData?.value.text));

onMounted(() => {
  loadDocument();
});

const loadDocument = () => {
  console.log('trying to load doc')
  // Find the selected document across all languages
  const allDocs = Object.values(documents).flat();
  const doc = allDocs.find(d => d.urn === selectedURN.value);
  
  console.log("loading document", doc.title)

  if (doc && doc.data) {
    selectedData.value = doc.data;
    emit('document-selected', {
      urn: doc.urn,
      lang: doc.lang,
      availableSections: availableSections.value,
      data: doc.data}
    )
    console.log('Loaded:', doc.title);
  }
};

const changeSection = () => {
  emit('section-selected', selectedSection.value);
}


</script>


<style scoped>
.document-selector {
  margin-bottom: 20px;
  padding: 16px;
  background-color: #f9fafb;
  border-radius: 8px;
}

.section-select-label{
  display:block;
  margin-top: 20px;
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

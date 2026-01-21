<template>
    <span>
        <div class="mistake-text">
            <li v-for="item in mistakeDisplay" :key="item">
                {{ item }}
            </li>
        </div>

        <button 
            class="clear-button" 
            @click="clearMistakes"
        >
            Reset Mistakes
        </button>
    </span>
</template>

<script setup>
import {computed} from 'vue';

const props = defineProps({
    mistakeTracker: {
        type: Object,
        required: true
    }
});

const emit = defineEmits(['clear-mistakes']);

const featureLabels = {
    pos: "Part of Speech",
    case: "Case",
    number: "Number",
    gender: "Gender",
    tense: "Tense",
    mood: "Mood",
    voice: "Voice",
    person: "Person",
};

const clearMistakes = () => {
  if (confirm('Are you sure you want to clear ALL mistakes? This cannot be undone.')) {
    emit('clear-mistakes');
  }
};

const mistakeDisplay = computed(() => {
    if (!props.mistakeTracker || Object.keys(props.mistakeTracker).length === 0) return ['No mistakes.'];

    const display=[];
    Object.entries(props.mistakeTracker).forEach(([feature, count]) => {
        display.push(`${featureLabels[feature]}: ${count} mistake(s)`);
    });
    return display;
});

</script>

<style scoped>
    .clear-button {
        position: relative;
        left: 50px;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        border: none;
        cursor: pointer;
    }

    .mistake-text {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
        font-size: 0.95rem;

    }
</style>
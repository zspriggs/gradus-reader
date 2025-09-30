<template>
  <div class="difficulty-selector">
    <h3>Reading Level:</h3>
    <div class="difficulty-buttons">
      <button
        v-for="lvl in levels"
        :key="lvl"
        :class="['difficulty-button', level === lvl ? 'active' : 'inactive']"
        @click="handleLevelChange(lvl)"
      >
        {{ lvl }}
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  level: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['level-change']);

const levels = ['beginner', 'intermediate', 'advanced'];

const handleLevelChange = (newLevel) => {
  emit('level-change', newLevel);
};
</script>

<style scoped>
.difficulty-selector {
  margin-bottom: 24px;
}

.difficulty-selector h3 {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #374151;
}

.difficulty-buttons {
  display: flex;
  gap: 8px;
}

.difficulty-button {
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  text-transform: capitalize;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.difficulty-button.active {
  background-color: #3b82f6;
  color: white;
}

.difficulty-button.inactive {
  background-color: #e5e7eb;
  color: #374151;
}

.difficulty-button.inactive:hover {
  background-color: #d1d5db;
}
</style>
<script lang="ts" setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  cityId: {
    type: Number,
    required: true,
  },
  cityName: {
    type: String,
    required: true,
  },
});


const emit = defineEmits(['viewCity', 'cityDeleted']);

const viewCity = () => {
  emit('viewCity', {id: props.cityId, name: props.cityName}); 
};

const deleteCity =  () => {
  emit('cityDeleted', props.cityId); 
};
</script>

<template>
  <div class="city-row">
    <div class="city-name">{{ cityName }}</div>
    <div class="actions">
      <button @click="viewCity" class="btn btn-view">
        <i class="el-icon-view"></i> View
      </button>
      <button @click="deleteCity" class="btn btn-delete">
        <i class="el-icon-delete"></i> Delete
      </button>
    </div>
  </div>
</template>

<style scoped>
.city-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #ccc;
}

.city-name {
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 0.3rem 0.5rem;
}

.btn-view {
  color: #007bff;
}

.btn-delete {
  color: #dc3545;
}
</style>

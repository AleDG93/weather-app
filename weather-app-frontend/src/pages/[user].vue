<script lang="ts" setup>
import axios from 'axios';
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import CityComponent from '../components/CityComponent.vue';
import { ElMessage } from 'element-plus';
import { OPEN_WEATHER_CITIES } from '../constants/cities';
import router from '../router/router';

const route = useRoute();  
const userName = route.params.user;

const cities = ref<{name: string, id: number,}[]>([]);
const userId = ref<number | null>(null);
const weatherData = ref<{
cityName: string,
weather: string,
temp: string,
feelsLike: string,
humidity: string,
lastCall: string,
} | null>();
const isModalVisible = ref(false);

const selectedCity = ref('');
const modalCityName = ref('')
const fetchData = async () => {
  if(!userName?.length){
    return
  }
  try {
    const userResponse = await axios.post('http://localhost:5000/users', { name: userName });
    const user = userResponse.data.user;
    userId.value = user.id;

    const citiesResponse = await axios.get(`http://localhost:5000/users/${userId.value}/cities`);
    cities.value = citiesResponse.data.cities;
  } catch (error) {
    console.error('Error fetching data:', error);
    ElMessage.error('Something went wrong while fetching data.');
  }
};

const handleViewCity = async (city: {id: number, name: string}) => {
  try {
    const response = await axios.get(`http://localhost:5000/cities/${city.id}`);
    modalCityName.value = city.name;
    weatherData.value = response.data;
    isModalVisible.value = true;
  } catch (error) {
    console.error('Error fetching weather data:', error);
    ElMessage.error('Something with weather data went wrong.');
  }
};
const handleCityDeleted = async (deletedCityId: number) => {
  try {
    await axios.delete(`http://localhost:5000/users/${userId.value}/cities/${deletedCityId}`);
    ElMessage.success('City deleted successfully.');
    cities.value = cities.value.filter((city) => city.id !== deletedCityId);
  } catch (error) {
    console.error(error);
    ElMessage.error('Failed to delete city.');
  }
};

const addCityToUser = async () => {
  if (selectedCity.value) {
    try {
      await axios.post(`http://localhost:5000/users/${userId.value}/cities`, {
        cityName: selectedCity.value,
      });
      ElMessage.success('City added successfully.');
      selectedCity.value = ''
      fetchData()
    } catch (error) {
      console.error('Error adding city:', error);
      ElMessage.error('Something went wrong while adding city.');
    }
  }
};

const closeModal = () => {
  isModalVisible.value = false;
  weatherData.value = null;
  modalCityName.value = ''
};


// Filter out cities that alredy belong to the user
const SELECT_CITIES_OPTIONS = computed(() => OPEN_WEATHER_CITIES.filter(c => 
    !cities.value.some(userCity => userCity.name === c.value)
  ))

const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? SELECT_CITIES_OPTIONS.value.filter(createFilter(queryString))
    : SELECT_CITIES_OPTIONS.value
  // call callback function to return suggestions
  cb(results)
}

const createFilter = (queryString: string) => {
  return (cities: {value: string, label: string}) => {
    return (
      cities.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    )
  }
}
onMounted(() => {
  fetchData();
});

</script>

<template>
 <div class="cities-page">
    <h1>Welcome {{ userName }}</h1>
    <h2>Here's the list of your favourite cities</h2>
    <p>
      You can add a city by selecting it from the dropdown.
    </p>    
    <el-autocomplete
        v-model="selectedCity"
        :fetch-suggestions="querySearch"
        clearable
        class="inline-input w-50"
        placeholder="Please Input"
        @select="addCityToUser"
      />
    <div v-if="cities.length > 0">
      <div>
      <div class="city-row">
        <div class="header-label">City Name</div>      
          <div class="header-label">Actions</div>              
      </div>
        <CityComponent
          v-for="city in cities"
          :key="city.id"
          :cityId="city.id"
          :userId="userId"
          :cityName="city.name"
          @viewCity="handleViewCity"
          @cityDeleted="handleCityDeleted"
        />
      </div>
    </div>
    <p v-else>No cities found.</p>
    
    <el-button style="margin-top: 20px;" type="secondary" @click="router.go(-1)">Go back</el-button>

  </div>

  <el-dialog
    v-model="isModalVisible"
    :title="modalCityName"
    width="500"
    :before-close="isModalVisible"
  >
  <div v-if="weatherData">
        <p><strong>Weather:</strong> {{ weatherData.weather }}</p>
        <p><strong>Temperature:</strong> {{ weatherData.temp }} °C</p>
        <p><strong>Feels Like:</strong> {{ weatherData.feelsLike }} °C</p>
        <p><strong>Humidity:</strong> {{ weatherData.humidity }} %</p>
        <p><strong>Data updated at:</strong> {{ weatherData.lastCall }}</p>
      </div>
      
      <template #footer>
      <div class="dialog-footer">
        <el-button @click="closeModal">Close</el-button>      
      </div>
    </template>
  </el-dialog>
</template>
<style>
.city-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #ccc;
}

.header-label {
  font-weight: bold;
  font-style: italic;
  color: steelblue;
}

</style>
<script lang="ts"  setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
const router = useRouter();

const name = ref('');
const submitName = async () => {
  if (!name.value.trim()) {
    return;
  }

  router.push({
    path: `/${name.value}`,
  });
};
</script>
<template>
  <div>
    <div>
      <h1>Welcome to Your Weather App!</h1>
      <p>
        Insert a username to get your weather information. If you have already used the app, please reuse the same username to access the weather info of your cities.
        If you're a new user, feel free to insert a random username and start exploring.
        Enjoy!
      </p>
    </div>
    <div>
<div>
  <el-input 
  v-model="name" 
  placeholder="What's your name?" 
  style="margin-bottom: 20px; max-width: 300px;"
  ></el-input>
</div>
<div>

  <el-button type="primary" @click="submitName">Bring me to my cities</el-button>
</div>
    </div>
  </div>
</template>

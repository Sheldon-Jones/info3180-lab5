<template>
  <div class="container mt-4">
    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
      <strong>Success!</strong> {{ successMessage }}
      <button type="button" class="btn-close" @click="successMessage = ''" aria-label="Close"></button>
    </div>

    <!-- Error Messages -->
    <div v-if="errorMessages.length > 0" class="alert alert-danger alert-dismissible fade show" role="alert">
      <strong>Errors:</strong>
      <ul class="mb-0">
        <li v-for="(error, index) in errorMessages" :key="index">{{ error }}</li>
      </ul>
      <button type="button" class="btn-close" @click="errorMessages = []" aria-label="Close"></button>
    </div>

    <!-- Movie Form -->
    <form @submit.prevent="saveMovie" id="movieForm">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" id="title" class="form-control" required />
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea name="description" id="description" class="form-control" rows="4" required></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input type="file" name="poster" id="poster" class="form-control" accept="image/*" required />
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const message = ref("");
const messageClass = ref("");
const displayMessage = ref (false);

onMounted(() => {
  getCsrfToken();
});

let csrf_token = ref('');
let successMessage = ref('');
let errorMessages = ref([]);

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
.then((response) => response.json())
.then((data) => { 
console.log(data);
csrf_token.value = data.csrf_token;
})
}

function saveMovie() {
  let movieForm = document.getElementById('movieForm');
  let form_data = new FormData(movieForm);
  
  fetch('/api/v1/movies', {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.message === "Movie Successfully added") {
        displayMessage.value = true;
        message.value = "Moovie added successfully!";
        successMessage.value = data.message + ' - Title: ' + data.title;
        errorMessages.value = [];
        movieForm.reset();
      } else if (data.errors) {
        errorMessages.value = data.errors;
        successMessage.value = '';
      }
      console.log(data);
    })
    .catch(function (error) {
      console.log(error);
      errorMessages.value = ['An error occurred while submitting the form'];
    });
}


</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>

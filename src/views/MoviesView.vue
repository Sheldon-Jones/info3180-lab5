<template>
  <div class="container mt-5">
    <h1 class="mb-4 text-start">Movies</h1>
    
    <div class="row">
      <div v-for="movie in movies" :key="movie.id" class="col-md-6 mb-4">
        
        <div class="card h-100 shadow-sm border">
          <div class="row g-0 h-100">
            
            <div class="col-5">
              <img :src="movie.poster" class="img-fluid rounded-start movie-poster" :alt="movie.title" />
            </div>

            <div class="col-7">
              <div class="card-body p-3 d-flex flex-column h-100">
                <h5 class="card-title fw-bold">{{ movie.title }}</h5>
                <p class="card-text text-muted small mt-2">
                  {{ movie.description }}
                </p>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>

    <div v-if="movies.length === 0" class="alert alert-info">
      No movies found. <router-link to="/movies/create">Add a movie</router-link>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';

let movies = ref([]);

function fetchMovies() {
  fetch('/api/v1/movies')
    .then((response) => response.json())
    .then((data) => {
      movies.value = data.movies;
    })
    .catch((error) => {
      console.log(error);
    });
}

onMounted(() => {
  fetchMovies();
});

</script>

<style scoped>
.movie-poster {
  width: 100%;
  height: 100%;
  min-height: 200px;
  object-fit: cover; 
}
.card {
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-3px);
}

.card-title {
  /* Prevents long titles from breaking the box layout */
  display: -webkit-box;
 
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-text {
  /* Truncates long descriptions so boxes stay even */
  display: -webkit-box;

  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
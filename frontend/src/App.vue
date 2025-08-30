<style scoped>
.loading-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #007bff, #00c6ff);
  animation: loading 1.5s infinite linear;
  z-index: 9999;
}

@keyframes loading {
  0% {
    left: -100%;
    width: 100%;
  }
  50% {
    left: 25%;
    width: 50%;
  }
  100% {
    left: 100%;
    width: 0%;
  }
}

/* Optional: additional padding if content still overlaps */
section {
  min-height: calc(100vh - 160px);
}
</style>

<template>
  <div>
    <!-- Bootstrap fixed navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand"><strong>Tester</strong></router-link>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarMenu"
          aria-controls="navbarMenu"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarMenu">
          <form class="d-flex ms-auto" method="get" action="/search">
            <input class="form-control me-2" type="search" placeholder="Search" name="query">
            <button class="btn btn-success" type="submit"><i class="fab fa-searchengin"></i></button>
          </form>
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/summer" class="nav-link">Summer</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/winter" class="nav-link">Winter</router-link>
            </li>
            <li class="nav-item">
              <template v-if="$store.state.isAuthenticated">
                <router-link to="/my-account" class="btn btn-outline-light me-2">My Account</router-link>
              </template>
              
              <template v-else>
                <router-link to="/log-in" class="btn btn-outline-light me-2">Log in</router-link>
              </template>
            </li>
            <li class="nav-item">
              <router-link to="/cart" class="btn btn-success">
                <i class="fas fa-shopping-cart me-1"></i>
                Cart ({{ cartTotalLength }})
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- 🔵 Loading Bar -->
    <div v-if="isLoading" class="loading-bar"></div>

    <!-- Main content section with padding to avoid being hidden behind fixed navbar -->
    <section>
      <router-view />
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-4 mt-auto">
      <div class="container">
        <p>&copy; 2025</p>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  beforeCreate() {
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if (token) {
      axios.defaults.headers.common['Authorization'] = "Bearer " + token
    }else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  },
  computed: {
    cart() {
      return this.$store.state.cart
    },
    cartTotalLength() {
      let totalLength = 0

      for (let item of this.cart.items) {
        totalLength += parseInt(item.quantity)
      }

      return totalLength
    },
    isLoading() {
      return this.$store.state.isLoading
    }
  }
}
</script>

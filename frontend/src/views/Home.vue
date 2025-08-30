<template>
  <div class="home">
    <div class="container mt-4">
      <h1>Home</h1>
      <p>Welcome to the School Management System</p>

      <div v-if="$store.state.isLoading" class="text-center mb-4">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div class="row">
        <ProductBox 
            v-for="product in latestProducts"
            v-bind:key="product.id"
            v-bind:product="product" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/axios'

import ProductBox from '@/components/ProductBox.vue'

export default {
  name: 'Home',
  components: {
    ProductBox
  },
  data() {
    return {
      latestProducts: []
    }
  },
  mounted() {
    this.getLatestProducts()

    document.title = 'Home | CodexZo Ecommerce'
  },
  methods: {
    async getLatestProducts() {
      this.$store.commit('setIsLoading', true)

      try {
        const response = await axios.get('/api/v1/latest-products/')
        this.latestProducts = response.data
      } catch (error) {
        console.error(error)
      }

      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>

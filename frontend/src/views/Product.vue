<style scoped>
    .product-image {
        transition: transform 0.3s ease;
    }
    .product-image:hover {
        transform: scale(1.05);
    }

    .quantity-input {
        width: 100px;
    }
</style>


<template>
  <div class="container my-5">
    <div class="row">
      <!-- Product Image -->
      <div class="col-md-6">
        <div class="main-img border rounded shadow-sm p-3 bg-white">
          <img
            class="img-fluid product-image rounded"
            v-bind:src="product.image"
            alt="Product"
          />
        </div>
      </div>

      <!-- Product Info -->
      <div class="col-md-6">
        <div class="main-description p-3 bg-light rounded shadow-sm">
          <h5 class="text-muted mb-2">
            Category:
            <span class="badge bg-secondary">{{ product.category }}</span>
          </h5>

          <h2 class="fw-bold">{{ product.name }}</h2>

          <div class="price-area my-4">
            <h3 class="text-danger fw-bold mb-0">${{ product.price }}</h3>
            <small class="text-muted">(Additional tax may apply on checkout)</small>
          </div>

          <!-- Buttons & Quantity -->
          <div class="buttons d-flex flex-wrap gap-3 align-items-center my-4">
            <button class="btn btn-outline-danger shadow-sm">
              <i class="fa fa-heart me-2"></i> Wishlist
            </button>

            <button class="btn btn-success shadow-sm" @click="addToCart">
              <i class="fa fa-cart-plus me-2"></i> Add to Cart
            </button>

            <input
              type="number"
              class="form-control quantity-input"
              v-model="quantity"
              min="1"
              max="10"
            />
          </div>

          <!-- Product Details -->
          <div class="product-details mt-5">
            <h5 class="text-primary mb-2">Product Details</h5>
            <p class="text-muted">{{ product.description }}</p>
          </div>

          <!-- Support Box -->
          <div class="row bg-white border rounded shadow-sm p-3 mt-4">
            <div class="col-auto">
              <i class="fa-brands fa-rocketchat fa-2x text-primary"></i>
            </div>
            <div class="col">
              <p class="mb-0">
                Have a question? Contact us via live chat or email.
              </p>
            </div>
          </div>

          <!-- Delivery Info -->
          <div class="delivery mt-4">
            <p class="mb-1">
              <i class="fa fa-truck text-success me-2"></i>
              <strong>Delivery in 3 days from purchase date</strong>
            </p>
            <small class="text-muted">Order now to receive it on time!</small>
          </div>

          <div class="delivery-options mt-3">
            <p class="mb-1">
              <i class="fa fa-box text-warning me-2"></i>
              <strong>Delivery Options</strong>
            </p>
            <small class="text-muted">View all available delivery methods.</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
    name: 'Product',
    data() {
        return {
            product: {},
            quantity: 1,
        }
    },
    mounted() {
        this.getProduct(),
        this.cart = this.$store.state.cart
    },
    methods: {
        async getProduct() {
            this.$store.commit('setIsLoading', true)

            const category_slug = this.$route.params.category_slug
            const product_slug = this.$route.params.product_slug

            try {
                const response = await axios.get(`/api/v1/products/${category_slug}/${product_slug}/`)
                this.product = response.data

                document.title = this.product.name + ' | CodexZo Ecommerce'
            } catch (error) {
                console.error(error)
            }

            this.$store.commit('setIsLoading', false)
        },
        addToCart() {
            const quantity = parseInt(this.quantity)

            if (isNaN(quantity) || quantity < 1) {
                this.quantity = 1
                return
            }

            const item = {
                product: this.product,
                quantity: quantity,
            }

            this.$store.commit('addToCart', item)

            Swal.fire({
                toast: true,
                position: 'bottom-end',
                icon: 'success',
                title: 'Added to cart!',
                showConfirmButton: false,
                timer: 2000,
                timerProgressBar: true,
            })
        }
    }
}
</script>
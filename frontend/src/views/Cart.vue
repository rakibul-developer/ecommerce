<template>
  <div class="page-cart container py-4">
    <div class="row">
      <div class="col-12">
        <h1 class="h2">Cart</h1>
      </div>

      <div class="col-12 mb-4">
        <div class="card p-3">
          <div v-if="cartTotalLength">
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Price</th>
                  <th>Quantity</th>
                  <th>Total</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <CartItem
                  v-for="item in cart.items"
                  :key="item.product.id"
                  :initialItem="item"
                  @removeFromCart="removeFromCart"
                />
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>You don't have any products in your cart...</p>
          </div>
        </div>
      </div>

      <div class="col-12">
        <div class="card p-3">
          <h2 class="h5">Summary</h2>

          <p><span class="fw-bold">${{ cartTotalPrice }},</span> {{ cartTotalLength }} items</p>

          <hr />

          <router-link to="/cart/checkout" class="btn btn-dark">
            Proceed to checkout
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from '@/axios'
import CartItem from '@/components/CartItem.vue'

export default {
    name: 'Cart',
    data() {
        return {
            cart: {
                items: []
            }
        }
    },
    components: {
        CartItem
    },
    methods: {
        removeFromCart(item) {
            this.cart.items = this.cart.items.filter(i => i.product.id !== item.product.id)
        }
    },
    mounted() {
        this.cart = this.$store.state.cart
    },
    computed: {
        cartTotalLength() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        },
        cartTotalPrice() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.product.price * curVal.quantity
            }, 0)
        },
    }
}
</script>
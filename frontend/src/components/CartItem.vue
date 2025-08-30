<template>
  <tr>
    <td>
      <router-link :to="item.product.get_absolute_url" class="text-black text-decoration-none">
        {{ item.product.name }}
      </router-link>
    </td>

    <td>${{ item.product.price }}</td>

    <td>
      {{ item.quantity }}
      <a
        @click="decrementQuantity(item)"
        role="button"
        class="btn btn-danger ms-2 px-2 py-1"
        title="Decrease quantity"
      >−</a>
      <a
        @click="incrementQuantity(item)"
        role="button"
        class="ms-2 btn btn-success px-2 py-1"
        title="Increase quantity"
      >+</a>
    </td>

    <td>${{ getItemTotal(item).toFixed(2) }}</td>

    <td>
      <button
        type="button"
        class="btn-close"
        aria-label="Remove"
        @click="removeFromCart(item)"
      ></button>
    </td>
  </tr>
</template>

<script>
export default {
    name: 'CartItem',
    props: {
        initialItem: Object,
    },
    data() {
        return {
            item: this.initialItem,
        }
    },
    methods: {
        getItemTotal(item) {
            return item.quantity * item.product.price
        },
        decrementQuantity(item) {
          item.quantity -= 1
          
          if (item.quantity === 0) {
            this.removeFromCart(item)
          }else {
            this.updateCart()
          }
        },
        incrementQuantity(item) {
          item.quantity += 1

          this.updateCart()
        },
        updateCart() {
          localStorage.setItem('cart', JSON.stringify(this.$store.state.cart))
        },
        removeFromCart(item) {
          this.$emit('removeFromCart', item)

          this.updateCart()
        }
    }
}
</script>
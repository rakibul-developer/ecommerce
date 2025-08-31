<template>
    <div class="page-checkout container py-4">
        <div class="row">
            <div class="col-12">
                <h1 class="display-4">Checkout</h1>
            </div>

            <div class="col-12 mb-4">
                <div class="card">
                    <div class="card-body">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th class="fw-bold">Product</th>
                                    <th class="fw-bold">Price</th>
                                    <th class="fw-bold">Quantity</th>
                                    <th class="fw-bold">Total</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr
                                    v-for="item in cart.items"
                                    :key="item.product.id"
                                >
                                    <td>{{ item.product.name }}</td>
                                    <td>${{ item.product.price }}</td>
                                    <td>{{ item.quantity }}</td>
                                    <td>${{ getItemTotal(item).toFixed(2) }}</td>
                                </tr>
                            </tbody>

                            <tfoot>
                                <tr>
                                    <td class="fw-bold" colspan="2">Total</td>
                                    <td class="fw-bold">{{ cartTotalLength }}</td>
                                    <td class="fw-bold">${{ cartTotalPrice.toFixed(2) }}</td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>
            </div>

            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <h2 class="h5">Shipping details</h2>

                        <p class="text-muted mb-4">* All fields are required</p>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">First name*</label>
                                    <input type="text" class="form-control" v-model="first_name">
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Last name*</label>
                                    <input type="text" class="form-control" v-model="last_name">
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">E-mail*</label>
                                    <input type="email" class="form-control" v-model="email">
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Phone*</label>
                                    <input type="text" class="form-control" v-model="phone">
                                </div>
                            </div>

                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">Address*</label>
                                    <input type="text" class="form-control" v-model="address">
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Zip code*</label>
                                    <input type="text" class="form-control" v-model="zipcode">
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Place*</label>
                                    <input type="text" class="form-control" v-model="place">
                                </div>
                            </div>
                        </div>

                        <div class="alert alert-danger mt-4" v-if="errors.length">
                            <p v-for="error in errors" :key="error">{{ error }}</p>
                        </div>

                        <hr>

                        <div id="card-element" class="mb-5"></div>

                        <template v-if="cartTotalLength">
                            <hr>
                            <button class="btn btn-dark" @click="submitForm">Pay with Stripe</button>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from '@/axios'

export default {
    name: 'Checkout',
    data() {
        return {
            cart: {
                items: []
            },
            stripe: {},
            card: {},
            first_name: '',
            last_name: '',
            email: '',
            phone: '',
            address: '',
            zipcode: '',
            place: '',
            errors: []
        }
    },
    mounted() {
        document.title = 'Checkout | Djackets'

        this.cart = this.$store.state.cart

        if (this.cartTotalLength > 0) {
            this.stripe = Stripe('pk_test_51S1KZs23lpb6u1Pgwqsq2VUmlJTSnc0F19tiEwyNRL3gfujXSlhjTgni15Ar4kRke8uSvZBJaoFAPgGHytyjzY5o00QViWaz7I')
            const elements = this.stripe.elements();
            this.card = elements.create('card', { hidePostalCode: true })

            this.card.mount('#card-element')
        }
    },
    methods: {
        getItemTotal(item) {
            return item.quantity * item.product.price
        },
        submitForm() {
            this.errors = []

            if (this.first_name === '') {
                this.errors.push('The first name field is missing!')
            }

            if (this.last_name === '') {
                this.errors.push('The last name field is missing!')
            }

            if (this.email === '') {
                this.errors.push('The email field is missing!')
            }

            if (this.phone === '') {
                this.errors.push('The phone field is missing!')
            }

            if (this.address === '') {
                this.errors.push('The address field is missing!')
            }

            if (this.zipcode === '') {
                this.errors.push('The zip code field is missing!')
            }

            if (this.place === '') {
                this.errors.push('The place field is missing!')
            }

            if (!this.errors.length) {
                this.$store.commit('setIsLoading', true)

                this.stripe.createToken(this.card).then(result => {                    
                    if (result.error) {
                        this.$store.commit('setIsLoading', false)

                        this.errors.push('Something went wrong with Stripe. Please try again')

                        console.log(result.error.message)
                    } else {
                        this.stripeTokenHandler(result.token)
                    }
                })
            }
        },
        async stripeTokenHandler(token) {
            const items = []

            for (let i = 0; i < this.cart.items.length; i++) {
                const item = this.cart.items[i]
                const obj = {
                    product: item.product.id,
                    quantity: item.quantity,
                    price: item.product.price * item.quantity
                }

                items.push(obj)
            }

            const data = {
                'first_name': this.first_name,
                'last_name': this.last_name,
                'email': this.email,
                'address': this.address,
                'zipcode': this.zipcode,
                'place': this.place,
                'phone': this.phone,
                'items': items,
                'stripe_token': token.id
            }

            await axios
                .post('/api/v1/checkout/', data, {
                    headers: {
                        'Authorization': `Bearer ${this.$store.state.token}`
                    }
                })
                .then(response => {
                    this.$store.commit('clearCart')
                    this.$router.push('/cart/success')
                })
                .catch(error => {
                    this.errors.push('Something went wrong. Please try again')

                    console.log(error)
                })

                this.$store.commit('setIsLoading', false)
        }
    },
    computed: {
        cartTotalPrice() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.product.price * curVal.quantity
            }, 0)
        },
        cartTotalLength() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        }
    }
}
</script>
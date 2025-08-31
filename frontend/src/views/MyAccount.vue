<template>
    <div class="container page-log-in mt-5">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <h1 class="mb-4">My Account</h1>

                <div v-if="userData">
                    <p><strong>Username:</strong> {{ userData.username }}</p>
                    <p><strong>Name:</strong> {{ userData.first_name + ' ' + userData.last_name }}</p>
                    <p><strong>Email:</strong> {{ userData.email }}</p>
                </div>

                <div class="mb-3">
                    <button @click="logout()" class="btn btn-danger w-100">logout</button>
                </div>
                <div class="alert alert-danger" v-if="errors.length">
                    <p v-for="error in errors" :key="error">{{ error }}</p>
                </div>
            </div>
        </div>
        <div class="row mt-4 justify-content-center" v-if="orders.length">
            <div class="col-md-12">
                <h2 class="text-center">My Orders</h2>
                <OrderSummary 
                    v-for="order in orders" 
                    :key="order.id" 
                    :order="order" 
                />
            </div>
        </div>
    </div>
</template>

<script>
import axios from '@/axios'
import OrderSummary from '@/components/OrderSummary.vue'

export default {
    name: "MyAccount",
    components: {
        OrderSummary
    },
    data() {
        return {
            errors: [],
            userData: JSON.parse(localStorage.getItem('userData')) || {},
            orders: []
        }
    },
    mounted() {
        document.title = 'My Account | CodexZo Ecommerce',
        this.getMyOrders()
    },
    methods: {
        logout() {
            axios.defaults.headers.common['Authorization'] = ''

            localStorage.removeItem('token')
            localStorage.removeItem('username')
            localStorage.removeItem('userid')

            this.$store.commit('removeToken')

            this.$router.push('/')
        },
        async getMyOrders() {
            this.$store.commit('setLoading', true)

            await axios.get(`/api/v1/my-orders/`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            .then(response => {
                this.orders = response.data
            })
            .catch(error => {
                console.error("There was an error fetching the orders:", error)
            })
        }
    }
}
</script>
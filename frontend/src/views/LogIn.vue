<template>
    <div class="container page-log-in mt-5">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <h1 class="mb-4">Log In</h1>

                <form @submit.prevent="submitForm">
                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input type="text" class="form-control" v-model="username">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="password">
                    </div>

                    <div class="alert alert-danger" v-if="errors.length">
                        <p v-for="error in errors" :key="error">{{ error }}</p>
                    </div>

                    <div class="mb-3">
                        <button type="submit" class="btn btn-dark w-100">Log In</button>
                    </div>

                    <hr>

                    <p class="text-center">
                        Or <router-link to="/sign-up">Click here</router-link> to create new account!
                    </p>
                </form>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
    name: "LogIn",
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    mounted() {
        document.title = 'Log In | CodexZo Ecommerce'
    },
    methods: {
        async submitForm() {
            axios.defaults.headers.common['Authorization'] = ""
            localStorage.removeItem('token')
            localStorage.removeItem('userData')  // নতুনভাবে ইউজারের ডাটা মুছে ফেলা হচ্ছে

            const formData = {
                username: this.username,
                password: this.password
            }

            await axios
                .post('api/v1/user/token/login/', formData)
                .then(response => {
                    console.log('Login response:', response) // লগিন রেসপন্স চেক করার জন্য
                    console.log(response.data)
                    const accessToken = response.data.access   // Access token
                    const refreshToken = response.data.refresh // Refresh token

                    // শুধু user সম্পর্কিত ডাটা আলাদা করো
                    const userData = {
                        id: response.data.id,
                        username: response.data.username,
                        email: response.data.email,
                        first_name: response.data.first_name,
                        last_name: response.data.last_name,
                    }

                    // Vuex store এ সেট করো
                    this.$store.commit('setToken', accessToken)
                    this.$store.commit('setUserData', userData)

                    // Axios default header সেট করো
                    axios.defaults.headers.common['Authorization'] = "Bearer " + accessToken

                    // LocalStorage এ সেভ করো
                    localStorage.setItem('token', accessToken)
                    localStorage.setItem('refresh_token', refreshToken) // চাইলে এটা future refresh এর জন্য
                    localStorage.setItem('userData', JSON.stringify(userData))

                    // Redirect
                    const toPath = this.$route.query.to || '/cart'
                    this.$router.push(toPath)
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else if (error.message) {
                        this.errors.push(error.message)
                    } else {
                        this.errors.push('Something went wrong. Please try again')
                    }
                })
        }
    }
}
</script>
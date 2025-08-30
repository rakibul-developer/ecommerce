<template>
    <div class="container page-sign-up mt-5">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <h1 class="mb-4">Sign up</h1>

                <form @submit.prevent="submitForm">
                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input type="text" class="form-control" v-model="username">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="password">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Repeat password</label>
                        <input type="password" class="form-control" v-model="password2">
                    </div>

                    <div class="alert alert-danger" v-if="errors.length">
                        <p v-for="error in errors" :key="error">{{ error }}</p>
                    </div>

                    <div class="mb-3">
                        <button type="submit" class="btn btn-dark w-100">Sign up</button>
                    </div>

                    <hr>

                    <p class="text-center">
                        Or <router-link to="/log-in">Click here</router-link> to log in!
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
    name: 'SignUp',
    data() {
        return {
            username: '',
            password: '',
            password2: '',
            errors: []
        }
    },
    mounted() {
        document.title = 'Sign up | CodexZo Ecommerce'
    },
    methods: {
        submitForm() {
             this.errors = []

             if (this.username === '') {
                 this.errors.push('The username is missing!')
             } else if (this.password === '') {
                 this.errors.push('The password is missing!')
             } else if (this.password2 === '') {
                 this.errors.push('The repeated password is missing!')
             } else if (this.password !== this.password2) {
                 this.errors.push('The passwords are not the same!')
             }

             if (!this.errors.length) {
                const formData = {
                    username: this.username,
                    password: this.password
                }

                axios
                    .post("api/v1/users/", formData)
                    .then(response => {
                        Swal.fire({
                            toast: true,
                            position: 'bottom-end',
                            icon: 'success',
                            title: 'You have successfully signed up!',
                            showConfirmButton: false,
                            timer: 2000,
                            timerProgressBar: true,
                        })

                        this.$router.push('/log-in')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                        } else if (error.message) {
                            this.errors.push(error.message)
                        } else {
                            this.errors.push('Something went wrong. Please try again!')
                        }
                    })
             }
        }
    }
}
</script>
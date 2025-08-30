<style scoped>

</style>


<template>
    <div class="container my-5">
        <div class="row">
            <!-- Product Image -->
            <div class="col-md-12">
                <h2 class="text-center">{{ category.name }}</h2>
            </div>
        </div>
        <div class="row">
            <ProductBox 
              v-for="product in category.products"
              v-bind:key="product.id"
              v-bind:product="product" />
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import Swal from 'sweetalert2'

import ProductBox from '@/components/ProductBox.vue'

export default {
    name: 'Category',
    components: {
        ProductBox
    },
    data() {
        return {
            category: {
                product: []
            }
        }
    },
    mounted() {
        this.getCategory()
    },
    watch: {
        $route(to, from) {
            if (to.name === 'Category') {
                this.getCategory()
            }
        }
    },
    methods: {
        async getCategory() {
            const category_slug = this.$route.params.category_slug

            this.$store.commit('setIsLoading', true)

            await axios.get(`/api/v1/category/${category_slug}/`)
                .then(response => {
                    this.category = response.data
                    document.title = this.category.name + ' | CodexZo Ecommerce'
                })
                .catch(error => {
                    console.log(error)
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Something went wrong!',
                        footer: '<a href="">Why do I have this issue?</a>'
                    })
                })
            
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>
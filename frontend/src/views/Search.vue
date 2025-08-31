<template>
    <div class="container py-4 page-search">
        <div class="row mb-4">
            <div class="col-12">
                <h1 class="display-4">Search</h1>
                <p class="text-muted h5">Search term: "{{ query }}"</p>
            </div>
        </div>

        <div class="row">
            <ProductBox
                v-for="product in products"
                :key="product.id"
                :product="product" />
        </div>
    </div>
</template>

<script>
import axios from '@/axios'
import ProductBox from '@/components/ProductBox.vue'

export default {
    name: 'Search',
    components: {
        ProductBox
    },
    data() {
        return {
            products: [],
            query: ''
        }
    },
    mounted() {
        document.title = 'Search | CodexZo Ecommerce';

        const uri = window.location.search.substring(1);
        const params = new URLSearchParams(uri);

        const searchQuery = params.get('query')
        if (searchQuery) {
            this.query = searchQuery;
            this.performSearch();
        }
    },
    methods: {
        async performSearch() {
            this.$store.commit('setIsLoading', true)

            try {
                const response = await axios.post('/api/v1/products/search/', {'query': this.query})
                this.products = response.data
            } catch (error) {
                console.error(error)
            }

            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>
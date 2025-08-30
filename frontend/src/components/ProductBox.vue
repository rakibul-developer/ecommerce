<template>
    <div class="col-lg-4 mb-4">
        <div class="card h-100">
            <img :src="product.thumbnail" class="card-img-top" width="200" height="200" alt="...">
            <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-text">{{ product.price }}</p>
                <router-link v-bind:to="product.get_absolute_url" class="btn btn-primary">View
                    Details</router-link>
            </div>
            <div class="card-footer">
                <small class="text-muted">Last updated 3 mins ago</small>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ProductBox',
    props: {
        product: Object
    }
}
</script>
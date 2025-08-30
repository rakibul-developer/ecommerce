<template>
    <div class="page-success container py-4 text-center">
        <div class="row">
            <div class="col-12">
                <h1 class="display-4 fw-bold">Thank you</h1>
                <p>Your order will be processed within 48 hours</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Success',
    mounted() {
        document.title = 'Success | Djackets';
    },
}
</script>

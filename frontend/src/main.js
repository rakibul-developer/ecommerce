// Import Bootstrap CSS and JS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Optional: Import Font Awesome (if you're using icons like the shopping cart)
import '@fortawesome/fontawesome-free/css/all.min.css'

// Your custom styles (keep this if you have custom CSS in main.css)
import './assets/main.css'

// Vue setup
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App)
app.use(store)
app.use(router)
app.mount('#app')

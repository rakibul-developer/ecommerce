import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Product from '@/views/Product.vue'
import Category from '@/views/Category.vue'
import Search from '@/views/Search.vue'
import Cart from '@/views/Cart.vue'
import SignUp from '@/views/SignUp.vue'
import LogIn from '@/views/LogIn.vue'
import MyAccount from '@/views/MyAccount.vue'
import store from '@/store'
import Checkout from '@/views/Checkout.vue'
import Success from '@/views/Success.vue'

const routes = [
  { path: '/',
    name: 'Home',
    component: Home
  },
  { path: '/search',
    name: 'Search',
    component: Search
  },
  { path: '/:category_slug/:product_slug/',
    name: 'Product',
    component: Product
  },
  { path: '/:category_slug/',
    name: 'Category',
    component: Category
  },
  { path: '/cart',
    name: 'Cart',
    component: Cart
  },
  { path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  { path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  { path: '/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta: { requireLogin: true }
  },
  { path: '/cart/checkout',
    name: 'Checkout',
    component: Checkout,
    meta: { requireLogin: true }
  },
  { path: '/cart/success',
    name: 'Success',
    component: Success
  },
  // { path: '/about', component: About },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'log-in', query: { to: to.path } })
  } else {
    next()
  }
})

export default router
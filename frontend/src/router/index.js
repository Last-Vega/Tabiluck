import Vue from 'vue'
import VueRouter from 'vue-router'
import Articles from '../views/Articles.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import PersonalPage from '../views/PersonalPage.vue'
import Detail from '../views/Detail.vue'

Vue.use(VueRouter)

const routes = [
  // sakuta
  {
    path: '/',
    name: 'Articles',
    component: Articles
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/personalpage',
    name: 'PesonalPage',
    component: PersonalPage
  },
  {
    path: '/detail/:id',
    name: 'Detail',
    component: Detail
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  // nakano
  {
    path: '/post',
    name: 'Post',
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/Post.vue'),
    props: true
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

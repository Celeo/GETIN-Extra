import Vue from 'vue'
import VueRouter from 'vue-router'

import store from '@/store'

import Landing from '@/pages/Landing'
import Login from '@/pages/Login'
import Logout from '@/pages/Logout'
import LoginCallback from '@/pages/LoginCallback'
import Admin from '@/pages/Admin'

import WikiIndex from '@/pages/wiki/Index'
import WikiViewPage from '@/pages/wiki/ViewPage'
import WikiEditPage from '@/pages/wiki/EditPage'
import WikiHistoryPage from '@/pages/wiki/HistoryPage'

import FitsEditor from '@/pages/fits/Editor'
import FitsFits from '@/pages/fits/Fits'


Vue.use(VueRouter)

const routes = [
  { path: '/', component: Landing, name: 'Landing' },
  { path: '/login', component: Login, name: 'Login' },
  { path: '/logout', component: Logout, name: 'Logout' },
  { path: '/eve/callback', component: LoginCallback, name: 'LoginCallback' },
  { path: '/admin', component: Admin, name: 'Admin' },
  { path: '/wiki/index', component: WikiIndex, name: 'WikiIndex' },
  { path: '/wiki/page/:category/:page', component: WikiViewPage, name: 'WikiViewPage' },
  { path: '/wiki/edit/:pageId', component: WikiEditPage, name: 'WikiEditPage' },
  { path: '/wiki/history/:pageId', component: WikiHistoryPage, name: 'WikiHistoryPage' },
  { path: '/fits/index', component: FitsFits, name: 'FitsFits' },
  { path: '/fits/editor', component: FitsEditor, name: 'FitsEditor' }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

/*
  State and permission-based routing
*/
router.beforeEach((to, from, next) => {
  /*
    If the user is not logged in and not in the process of doing so or just
    looking at the landing page, redirect them away from their detination
    to the Login page.
  */
  if (['Login', 'Logout', 'Landing', 'LoginCallback'].indexOf(to.name) === -1) {
    if (!store.getters.isLoggedIn) {
      next({ name: 'Login' })
      store.commit('SET_LOGIN_REDIRECT', to.path)
      return
    }
  }
  next()
})


// export created and configured router
export default router

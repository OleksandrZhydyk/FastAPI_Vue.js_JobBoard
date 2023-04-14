import { createRouter, createWebHistory } from 'vue-router'
import VacanciesView from '@/views/VacanciesView.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'main',
    component: VacanciesView
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/users/profile/:id',
    name: 'applicantProfile',
    component: () => import('@/views/ApplicantProfile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/me/vacancies',
    name: 'companyVacancies',
    component: () => import('@/views/CompanyVacancies.vue'),
    meta: { requiresAuth: true, isCompany: true },
  },
  {
    path: '/me',
    name: 'userProfile',
    component: () => import('@/views/UserProfile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/me/applied_vacancies',
    name: 'appliedVacancies',
    component: () => import('@/views/AppliedVacancies.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/me/vacancies/archive',
    name: 'archivedVacancies',
    component: () => import('@/views/ArchivedVacancies.vue'),
    meta: { requiresAuth: true, isCompany: true },
  },
  {
    path: '/vacancies/create',
    name: 'createVacancy',
    component: () => import('@/views/CreateVacancy.vue'),
    meta: { requiresAuth: true, isCompany: true },
  },
  {
    path: '/vacancies/:id',
    name: 'vacancies',
    component: () => import('@/views/VacancyDetailView.vue')
  },
  {
    path: '/vacancies/:id/update',
    name: 'vacanciesUpdate',
    component: () => import('@/views/VacancyUpdate.vue'),
    meta: { requiresAuth: true, isCompany: true },
  },
  {
    path: '/vacancies/:id/appliers',
    name: 'appliers',
    component: () => import('@/views/VacancyAppliers.vue'),
    meta: { requiresAuth: true, isCompany: true },
  },
  {
    path: '/forbidden',
    name: 'forbidden',
    component: () => import('@/views/Forbidden.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not_found',
    component: () => import('@/views/PageNotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, _, next) => {
  if (to.matched.some(record => record.meta.requiresAuth && record.meta.isCompany)) {
    if (store.getters['allUsers/isCompany']) {
      next();
      return;
    }
    next('/forbidden');
  }
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters['allUsers/isAuthenticated']) {
      next();
      return;
    }
    next('/login');
  } else {
    next();
  }
});

export default router

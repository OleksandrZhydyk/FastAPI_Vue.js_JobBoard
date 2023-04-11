import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import VacanciesView from '@/views/VacanciesView.vue'
import VacancyDetailView from '@/views/VacancyDetailView.vue'
import CompanyVacancies from '@/views/CompanyVacancies.vue'
import VacancyAppliers from '@/views/VacancyAppliers.vue'
import VacancyUpdate from '@/views/VacancyUpdate.vue'
import CreateVacancy from '@/views/CreateVacancy.vue'
import ArchivedVacancies from '@/views/ArchivedVacancies.vue'
import ApplicantProfile from '@/views/ApplicantProfile.vue'
import UserProfile from '@/views/UserProfile.vue'
import RegisterView from '@/views/RegisterView.vue'
import AppliedVacancies from '@/views/AppliedVacancies.vue'
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
    component: RegisterView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/users/profile/:id',
    name: 'applicantProfile',
    component: ApplicantProfile,
    meta: { requiresAuth: true },
  },
  {
    path: '/me/vacancies',
    name: 'companyVacancies',
    component: CompanyVacancies,
    meta: { requiresAuth: true },
  },
  {
    path: '/me',
    name: 'userProfile',
    component: UserProfile,
    meta: { requiresAuth: true },
  },
  {
    path: '/me/applied_vacancies',
    name: 'appliedVacancies',
    component: AppliedVacancies,
    meta: { requiresAuth: true },
  },
  {
    path: '/me/vacancies/archive',
    name: 'archivedVacancies',
    component: ArchivedVacancies,
    meta: { requiresAuth: true },
  },
  {
    path: '/vacancies/create',
    name: 'createVacancy',
    component: CreateVacancy,
    meta: { requiresAuth: true },
  },
  {
    path: '/vacancies/:id',
    name: 'vacancies',
    component: VacancyDetailView
  },
  {
    path: '/vacancies/:id/update',
    name: 'vacanciesUpdate',
    component: VacancyUpdate,
    meta: { requiresAuth: true },
  },
  {
    path: '/vacancies/:id/appliers',
    name: 'appliers',
    component: VacancyAppliers,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, _, next) => {
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

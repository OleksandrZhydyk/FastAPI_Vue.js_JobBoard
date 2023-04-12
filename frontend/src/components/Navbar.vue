<template>
 <header>
    <nav class="navbar navbar-expand-lg navbar-light bg-light" >
      <div class="container">
        <a class="navbar-brand" href="#" @click="$router.push('/')">Job Board</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <router-link class="nav-link active" aria-current="page" :to="{name: 'main'}">Vacancies</router-link>
            <router-link class="nav-link active" v-if="isCompany && isLoggedIn" :to="{name: 'companyVacancies'}">My vacancies</router-link>
            <router-link class="nav-link active" v-if="isCompany && isLoggedIn" :to="{name: 'archivedVacancies'}">Archived vacancies</router-link>
            <router-link class="nav-link active" v-if="isLoggedIn && !isCompany" :to="{name: 'appliedVacancies'}">Applied vacancies</router-link>
            <router-link class="nav-link active" v-if="isLoggedIn" :to="{name: 'userProfile'}">Profile</router-link>
          </div>
        </div>

        <router-link class="btn btn-outline-primary ms-2" v-if="isLoggedIn" @click="logOut" :to="{name: 'login'}">Logout</router-link>
        <router-link class="btn btn-outline-primary ms-2" :to="{name: 'login'}" v-if="!isLoggedIn" >Login</router-link>
        <router-link class="btn btn-outline-success ms-2" :to="{name: 'register'}" v-if="!isLoggedIn" >SignIn</router-link>
      </div>
    </nav>
 </header>
</template>

<script>
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex';

export default {
  name: 'NavBar',

  computed: {
    ...mapGetters({
        isLoggedIn: 'allUsers/isAuthenticated',
        isCompany: 'allUsers/isCompany',
    }),
    ...mapState({
        user: state => state.allUsers.user,
    }),
  },
  methods: {
    ...mapActions({
        logOut: 'allUsers/logOut'
    })
  },
}
</script>
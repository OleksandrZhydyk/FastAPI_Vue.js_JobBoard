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
            <a class="nav-link active" aria-current="page" href="#" @click="$router.push('/')">Vacancies</a>
            <a class="nav-link active" href="#" v-if="isCompany" @click="$router.push('/me/vacancies')">My vacancies</a>
          </div>
        </div>
        <form class="d-flex" role="search">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>

        <router-link class="btn btn-outline-primary ms-2" v-if="isLoggedIn" @click="logOut" to="/login">Logout</router-link>
        <router-link class="btn btn-outline-primary ms-2" to="/login" v-else >Login</router-link>
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
<template>
<div class="container d-flex align-items-center justify-content-center p-5">
  <div class="card p-5 bg-white col-md-6 ">
     <form @submit.prevent="submit" style="margin: auto;" class="text-center mt-2 mb-5">
     <h2 class="mb-5">Login</h2>
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" name="username" v-model="form.username" class="form-control" required="true"/>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" name="password" v-model="form.password" class="form-control" required="true"/>
      </div>
      <div v-if="errors" class="alert alert-danger" role="alert">
          <ul v-for="error, index in errors" :key="index">
            <li>{{error}}</li>
          </ul>
      </div>
      <button type="submit" class="btn btn-primary float-end">Login</button>
    </form>
    </div>
</div>
</template>

<script>
// @ is an alias to /src
import { mapActions, mapState, mapMutations } from 'vuex';

export default {
  name: 'LoginView',
  components: {},
  data() {
    return {
      error: false,
      form: {
        username: '',
        password:'',
      }
    }
  },
  computed: {
    ...mapState({
        errors: state => state.allUsers.errors,
    }),
  },
  methods: {
    ...mapActions({
        logIn: 'allUsers/logIn',
    }),
    ...mapMutations({
        setErrors: 'allUsers/setErrors',
    }),

      async submit() {
          const form_data = new FormData();
          form_data.append('username', this.form.username);
          form_data.append('password', this.form.password);
          const res = await this.logIn(form_data);
          if (res){
            this.setErrors(null)
            this.$router.push('/');
          } else {
            this.error = true
          }
      }
  },
}
</script>

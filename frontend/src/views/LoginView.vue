<template>
<div class="container d-flex align-items-center justify-content-center p-5">
  <div class="card p-5 bg-white col-md-8 mt-5">
     <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="username" class="form-label">Username:</label>
        <input type="text" name="username" v-model="form.username" class="form-control" required="true"/>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input type="password" name="password" v-model="form.password" class="form-control" required="true"/>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    </div>
</div>
</template>

<script>
// @ is an alias to /src
import { mapActions } from 'vuex';

export default {
  name: 'LoginView',
  components: {},
  data() {
    return {
      form: {
        username: '',
        password:'',
      }
    };
  },
  methods: {

    ...mapActions({
        logIn: 'allUsers/logIn',
    }),

  async submit() {
      const form_data = new FormData();
      form_data.append('username', this.form.username);
      form_data.append('password', this.form.password);
      await this.logIn(form_data);
      this.$router.push('/');
      }
    },
}
</script>

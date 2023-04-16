<template>
  <div class="container d-flex align-items-center justify-content-center p-5">
    <div class="card bg-white col-md-6">
      <form @submit.prevent="submit" style="margin: auto;" class="text-center mt-5 mb-5">
        <h2 class="mb-5">Registration</h2>
        <div class="mb-3">
          <label for="username" class="form-label">Email</label>
          <input type="text" name="username" v-model="email" class="form-control" required="true"/>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" name="password" v-model="password" class="form-control" required="true"/>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password confirmation</label>
          <input type="password" name="password-confirmation" v-model="passwordConfirmation" class="form-control" required="true"/>
        </div>
        <div class="mb-3">
          <input type="checkbox" class="me-2" name="password-confirmation" v-model="isCompany"/>
          <label for="password" class="form-label">Employer Y/N?</label>
        </div>
        <div v-if="errors" class="alert alert-danger" role="alert">
          <ul v-for="error, index in errors" :key="index">
            <li>{{error}}</li>
          </ul>
        </div>
        <button type="submit" class="btn btn-primary float-end">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex';

export default {
  name: 'RegisterView',
  data() {
    return {
      email: '',
      password:'',
      passwordConfirmation: '',
      isCompany: false
    }
  },
  computed: {
    ...mapState({
      errors: state => state.allUsers.errors,
    }),
  },
  methods: {
    ...mapMutations({
      setErrors: 'allUsers/setErrors',
    }),
    ...mapActions({
      createUser: 'allUsers/createUser',
    }),
    async submit() {
      const payload = {
        email: this.email,
        password: this.password,
        confirmed_password: this.passwordConfirmation,
        is_company: this.isCompany,
      };
      const res = await this.createUser(payload);
      if (res) {
        this.setErrors(null);
        this.$router.push('/login');
      }
    }
  }
}
</script>
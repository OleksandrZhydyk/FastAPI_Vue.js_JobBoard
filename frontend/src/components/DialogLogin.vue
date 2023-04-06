<template>
<button type="button" class="btn btn-primary mt-4" data-bs-toggle="modal" data-bs-target="#exampleModal">
  Apply
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Login required</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <form @submit.prevent="submit" style="margin: auto;" class="text-center mt-5 mb-5">
          <div class="modal-body">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" name="username" v-model="form.username" class="form-control" required="true"/>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" name="password" v-model="form.password" class="form-control" required="true"/>
              </div>
          </div>
          <div>
            <button type="submit" class="btn btn-primary" aria-label="Close" data-bs-dismiss="modal">Login</button>
          </div>
      </form>
    </div>
  </div>
</div>

</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'Dialog',

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

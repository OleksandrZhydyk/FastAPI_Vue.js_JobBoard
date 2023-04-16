<template>
  <div v-if="modal" class="modal" tabindex="-1" style="display:block; background-color: rgba(0, 0, 0, 0.77);"  aria-hidden="true" role="dialog">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-body">
          <p v-if="updated" class="text-center fs-3">Vacancy updated successfully</p>
          <p v-if="created" class="text-center fs-3">Vacancy created successfully</p>
          <div v-if="errors" class="alert alert-danger" role="alert">
            <ul v-for="error, index in errors" :key="index">
              <li>{{error}}</li>
            </ul>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" @click='$emit("modal")' class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
export default{
  props: {
    created: {
      type: Boolean,
        value: false,
      },
      updated: {
        type: Boolean,
        value: false
      },
      modal: {
        type: Boolean,
        value: false
      }
    },
    computed: {
    ...mapState({
      errors: state => state.allUsers.errors,
    }),
  }
}

</script>

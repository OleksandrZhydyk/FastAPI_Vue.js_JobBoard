<template>

<div v-if="modal" class="modal" tabindex="-1" style="display:block; background-color: rgba(0, 0, 0, 0.77);"  aria-hidden="true" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-body">
        <p v-if="updated" class="text-center fs-3">Vacancy updated successfully</p>
        <p v-if="created" class="text-center fs-3">Vacancy created successfully</p>
        <p v-if="error" class="text-center fs-3">Error occurred</p>
      </div>
      <div class="modal-footer">
        <button type="button" @click='$emit("modal")' class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

</template>

<script>
export default{
    props: {
        created: {
            type: Boolean,
            value: false,
        },
        updated: {
            type: Boolean,
            value: false,
        },
        error: {
            type: Boolean,
            value: false,
        },
        modal: {
            type: Boolean,
            value: false,
        }
    },
}

</script>

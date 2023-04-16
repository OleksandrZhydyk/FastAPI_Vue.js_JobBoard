<template>
  <div class="row mt-5">
    <div class="col text-center">
      <h2 class="text-center">403 Forbidden</h2>
      <router-link class="btn btn-success mt-2" style="text-align:center;" :to="{name: 'main'}">Back Home</router-link>
    </div>
  </div>
</template>

<script>

export default {
  name: "Forbidden"
}
</script>
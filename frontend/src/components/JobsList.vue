<template>

    <div v-for="job in jobs" :key="job.id">
        <div class="card mt-3">
          <div class="card-header">
            {{job.title}}
          </div>
          <div class="card-body">
            <h5 class="card-title">{{job.description}}</h5>
            <p class="card-text">{{job.created}}</p>
            <p class="card-text">{{job.category}}</p>
            <a href="#" class="btn btn-outline-primary" v-if="!isCompany" @click="$router.push(`/jobs/${job.id}`)">Go to</a>
            <a href="#" class="btn btn-outline-primary" v-if="isCompany" @click="$router.push(`/jobs/${job.id}/appliers`)">Get Appliers</a>
          </div>
        </div>
    </div>

</template>

<script>

export default{
    props: {
        jobs: {
            type: Array,
            required: true,
        },
        isCompany: {
            type: Boolean,
        },
    }
}
</script>
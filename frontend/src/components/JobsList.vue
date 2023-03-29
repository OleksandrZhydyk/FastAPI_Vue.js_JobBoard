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
            <a href="#" class="btn btn-outline-primary" v-if="!getAppliers" @click="$router.push(`/jobs/${job.id}`)">Go to</a>
            <div v-if="getAppliers">
            <a href="#" class="btn btn-outline-primary" @click="$router.push(`/jobs/${job.id}/appliers`)">Get Appliers</a>
            <router-link :to="{}" class="btn btn-warning">Edit</router-link>
            <a href="#" class="btn btn-outline-danger" @click="removeJob(job.id)">Delete Vacancy</a>
            </div>
          </div>
        </div>
    </div>

</template>

<script>
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex';

export default{
    props: {
        jobs: {
            type: Array,
            required: true,
        },
        getAppliers: {
            type: Boolean,
            value: false,
        },
    },

    methods: {
    ...mapActions({
        deleteJob: 'allJobs/deleteJob'
    }),

    async removeJob(id){
        try {
            let {data} = await this.deleteJob(id)
            if (data){
                this.removeJob(id);
                };
        } catch(e){
            console.log(e);
        }
    },

    removeJob(id){
        this.jobs = this.jobs.filter(item => item.id !== id )
        },
  },

}
</script>
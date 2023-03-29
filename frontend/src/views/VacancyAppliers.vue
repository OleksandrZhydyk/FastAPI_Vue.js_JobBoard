<template>
    <div v-if="jobAppliers">
        <div v-if="jobAppliers.appliers.length" v-for="applier in jobAppliers.appliers" :key="applier.id">
            <div class="card mt-3">
                <div class="card-header">
                    {{applier.email}}
                </div>
                <div class="card-body">
                    <h5 class="card-title">{{applier.name}}</h5>
                    <p class="card-text">{{applier.created_at}}</p>
                    <p class="card-text">{{applier.is_active}}</p>
                    <a href="#" class="btn btn-outline-primary" @click="$router.push(`/jobs/${job.id}`)">Go to</a>
                </div>
            </div>
        </div>
        <div v-else> No applicants </div>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {

    methods: {
        ...mapActions({
            getJobAppliers: 'allJobs/getJobAppliers',
        }),
    },

    computed: {
        ...mapState({
            jobAppliers: state => state.allJobs.jobAppliers,
        }),
    },
    created() {
        this.getJobAppliers(`${this.$route.params.id}`)
    },

}

</script>
<template>
<jobs-list v-if="loadingIndicator" :jobs="jobs.items" :isCompany="isCompany"/>
<div v-else> Loading ... </div>
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex';
import JobsList from '@/components/JobsList';

export default {
    name: "Jobs",
    components: {
        JobsList
    },
    data() {
        return{isCompany: false,}
    },
    methods: {
        ...mapActions({
            getJobs: 'allJobs/getJobs',
        }),
    },
    computed: {
        ...mapState({
            jobs: state => state.allJobs.jobs,
            loadingIndicator: state => state.allJobs.jobsLoadingIndicator,
            user: state => state.allUsers.user,
        }),
    },
    created() {
        this.getJobs()
    },


}
</script>
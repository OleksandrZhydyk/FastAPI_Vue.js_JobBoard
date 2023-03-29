<template>
    <div class="post">
        <div>
            <div><strong>title:</strong> {{job.title}} </div>
            <div><strong>description:</strong> {{job.description}} </div>
            <div><strong>salary from:</strong> {{job.salary_from}} </div>
            <div><strong>salary to:</strong> {{job.salary_to}} </div>
            <div><strong>create date:</strong> {{new Date(job.created_at)}} </div>
            <div><strong>update date:</strong> {{new Date(job.updated_at)}} </div>
            <a href="#" class="btn btn-outline-primary" >Apply to</a>
        </div>
    </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from 'vuex';

export default {
    name: "JobDetail",

    methods: {
        ...mapActions({
            getJob: 'allJobs/getJob',
        }),
    },
    computed: {
        ...mapState({
            job: state => state.allJobs.job,
        }),
    },
    mounted() {
        this.getJob(`${this.$route.params.id}`)
    },

}

</script>
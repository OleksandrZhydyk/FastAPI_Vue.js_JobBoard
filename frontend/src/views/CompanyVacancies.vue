<template>

<div v-if="loadingIndicator" v-for="vacancy in companyVacancies" :key="vacancy.id">
        <div class="card mt-3">
          <div class="card-header">
            {{vacancy.title}}
          </div>
          <div class="card-body">
            <h5 class="card-title">{{vacancy.description}}</h5>
            <p class="card-text">{{vacancy.created}}</p>
            <p class="card-text">{{vacancy.category}}</p>
            <a href="#" class="btn btn-outline-primary" @click="$router.push(`/jobs/${vacancy.id}/appliers`)">Get Appliers</a>
            <a href="#" class="btn btn-outline-warning" @click="$router.push(`/jobs/${vacancy.id}/update`)">Edit</a>
            <a href="#" class="btn btn-outline-danger" @click="removeJob(vacancy.id)">Delete Vacancy</a>
          </div>
        </div>
      </div>
    <div v-else> Loading ... </div>
</template>

<script>
import { mapActions, mapState, mapMutations } from 'vuex';

export default {
    name: "myAppliedJobs",

    methods: {
        ...mapActions({
            getMyCompanyVacancies: 'allUsers/getMyCompanyVacancies',
            deleteJob: 'allJobs/deleteJob'
        }),

        ...mapMutations({
            deleteMyVacancies: 'allUsers/deleteMyVacancies',
        }),

        async removeJob(id){
            try {
                await this.deleteJob(id)
                this.deleteMyVacancies(id);
            } catch(e){
                console.log(e);
            }
        },
    },
    computed: {
        ...mapState({
            companyVacancies: state => state.allUsers.companyVacancies,
            loadingIndicator: state => state.allUsers.myVacanciesLoadingIndicator,
        }),
    },
    created() {
        this.getMyCompanyVacancies()
    },

}

</script>
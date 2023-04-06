<template>
<div class="row">
<div class="col-8">
<h2 class="text-center mt-3">Your published vacancies</h2>
<div v-if="loadingIndicator" v-for="vacancy in companyVacancies" :key="vacancy.id">
        <div class="card mt-3">
          <div class="card-header">
            {{vacancy.title}}
          </div>
          <div class="card-body">
            <h5 class="card-title">{{vacancy.description}}</h5>
            <p class="card-text">{{vacancy.created}}</p>
            <p class="card-text">{{vacancy.category}}</p>
            <a href="#" class="btn btn-primary" @click="$router.push(`/vacancies/${vacancy.id}/appliers`)">Get Appliers</a>
            <a href="#" class="btn btn-danger float-end" @click="removeJob(vacancy.id)">Delete Vacancy</a>
            <router-link class="btn btn-warning float-end me-2" :to="{name: 'vacanciesUpdate', params: { id: vacancy.id }, query: { ...vacancy }}">Edit</router-link>
            <!-- <a href="#" class="btn btn-warning float-end me-2" @click="$router.push(`/vacancies/${vacancy.id}/update`, params: { vacancy })">Edit</a> -->
          </div>
        </div>
      </div>
    <div v-else> Loading ... </div>
    </div>
    </div>
</template>

<script>
import { mapActions, mapState, mapMutations } from 'vuex';

export default {
    name: "myAppliedVacancies",

    methods: {
        ...mapActions({
            getMyCompanyVacancies: 'allUsers/getMyCompanyVacancies',
            deleteVacancy: 'allVacancies/deleteVacancy'
        }),

        ...mapMutations({
            deleteMyVacancies: 'allUsers/deleteMyVacancies',
        }),

        async removeJob(id){
            try {
                await this.deleteVacancy(id)
                await this.deleteMyVacancies(id);
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
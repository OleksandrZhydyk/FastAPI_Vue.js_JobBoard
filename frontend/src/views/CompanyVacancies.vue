<template>
  <div class="row mt-2">
    <div class="col-8 mt-3">
      <h3 class="text-left">Published vacancies</h3>
    </div>
    <div class="col-4 mt-3">
      <router-link class="btn btn-success float-end" :to="{name: 'createVacancy'}">Create Vacancy</router-link>
    </div>
  </div>

  <div class="row">
    <div class="col">
      <div v-if="loadingIndicator" v-for="vacancy in activeVacancies" :key="vacancy.id">
        <div class="card mt-3">
          <div class="card-header">
            <span>{{vacancy.title}}</span>
            <span class="float-end">Updated: {{vacancy.updated_at.substring(0, 10)}}</span>
          </div>
          <div class="card-body">
            <p class="card-text">{{vacancy.category}}</p>
            <h5 class="card-title">{{vacancy.description}}</h5>
            <router-link class="btn btn-primary" :to="{name: 'appliers', params: { id: vacancy.id }}">Get Appliers</router-link>
            <a href="#" class="btn btn-danger float-end" @click="removeJob(vacancy.id)">Deactivate</a>
            <router-link class="btn btn-warning float-end me-2" :to="{name: 'vacanciesUpdate', params: { id: vacancy.id }, query: { ...vacancy }}">Edit</router-link>
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
        const res = await this.deleteVacancy(id);
          if (res){
            await this.deleteMyVacancies(id);
          }
      } catch(e){
        console.log(e);
      }
    },
  },
  computed: {
    ...mapState({
      companyVacancies: state => state.allUsers.companyVacancies,
      loadingIndicator: state => state.allUsers.myVacanciesLoadingIndicator,
      objOnPage: state => state.allVacancies.objOnPage
    }),
    activeVacancies(){
      return [...this.companyVacancies].filter((vacancy) => vacancy.is_active)
    }
  },
  created() {
    if (this.companyVacancies.length === 0){
      this.getMyCompanyVacancies()
    }
  },
}

</script>
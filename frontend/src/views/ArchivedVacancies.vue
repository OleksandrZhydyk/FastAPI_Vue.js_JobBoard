<template>
  <div class="row mt-2">
    <div class="col-8 mt-3">
      <h3 class="text-left">Archived vacancies</h3>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <div v-if="loadingIndicator" v-for="vacancy in this.archivedVacancies" :key="vacancy.id">
        <div class="card mt-3">
          <div class="card-header">
            <span>{{vacancy.title}}</span>
            <span class="float-end">Closed: {{vacancy.updated_at.substring(0, 10)}}</span>
          </div>
          <div class="card-body">
            <p class="card-text">{{vacancy.category}}</p>
            <h5 class="card-title">{{vacancy.description}}</h5>
            <router-link href="#" class="btn btn-primary" :to="{name: 'appliers', params: { id: vacancy.id }}">Get Appliers</router-link>
          </div>
        </div>
      </div>
      <div v-else> Loading ... </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: "archivedVacancies",
  methods: {
    ...mapActions({
      getMyCompanyVacancies: 'allUsers/getMyCompanyVacancies'
    }),
  },
  computed: {
    ...mapState({
      companyVacancies: state => state.allUsers.companyVacancies,
      loadingIndicator: state => state.allUsers.myVacanciesLoadingIndicator
    }),
    archivedVacancies(){
      return [...this.companyVacancies].filter((vacancy) => !vacancy.is_active)
    }
  },
  created() {
    if (this.companyVacancies.length === 0){
      this.getMyCompanyVacancies()
    }
  }
}
</script>
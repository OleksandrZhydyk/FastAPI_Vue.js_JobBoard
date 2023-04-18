<template>
  <div v-for="vacancy in vacancies" :key="vacancy.id">
    <div class="card mt-3">
      <div class="card-header">
        <span>{{vacancy.category}}</span>
        <span class="float-end">Published: {{vacancy.created_at.substring(0, 10)}}</span>
      </div>
      <div class="card-body">
        <h5 class="card-title">{{vacancy.title}}</h5>
        <p class="card-text">{{vacancy.description}}</p>
        <router-link class="btn btn-primary" :to="{name: 'vacancies', params: { id: vacancy.id }}">Go to</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default{
  name: 'JobsList',
  props: {
    vacancies: {
      type: Array,
      required: true
    },
    getAppliers: {
      type: Boolean,
      value: false
    }
  },

  methods: {
    ...mapActions({
      deleteVacancy: 'allVacancies/deleteVacancy'
    }),
    async removeJob(id){
      try {
        let {data} = await this.deleteVacancy(id)
          if (data){
            this.removeJob(id);
          };
      } catch(e){
        console.log(e);
      }
    },
    removeJob(id){
      this.vacancies = this.vacancies.filter(item => item.id !== id )
    }
  }
}
</script>

<template>

    <div v-for="vacancy in vacancies" :key="vacancy.id">
        <div class="card mt-3">
          <div class="card-header">
            {{vacancy.title}}
          </div>
          <div class="card-body">
            <h5 class="card-title">{{vacancy.description}}</h5>
            <p class="card-text">{{vacancy.created}}</p>
            <p class="card-text">{{vacancy.category}}</p>
            <a href="#" class="btn btn-primary" @click="$router.push(`/vacancies/${vacancy.id}`)">Go to</a>
          </div>
        </div>
    </div>

</template>

<script>
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex';

export default{
    props: {
        vacancies: {
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
        },
  },

}
</script>
<template>
<div class="row">
<div class="col-8">
<h2 class="text-center mt-3">Vacancies</h2>
<jobs-list v-if="loadingIndicator" :vacancies="vacancies.items" />
<div v-else> Loading ... </div>
</div>
</div>
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex';
import JobsList from '@/components/JobsList';

export default {
    name: "Vacancies",
    components: {
        JobsList
    },

    methods: {
        ...mapActions({
            getVacancies: 'allVacancies/getVacancies',
        }),
    },
    computed: {
        ...mapState({
            vacancies: state => state.allVacancies.vacancies,
            loadingIndicator: state => state.allVacancies.vacanciesLoadingIndicator,
            user: state => state.allUsers.user,
        }),
    },
    created() {
        this.getVacancies()
    },


}
</script>
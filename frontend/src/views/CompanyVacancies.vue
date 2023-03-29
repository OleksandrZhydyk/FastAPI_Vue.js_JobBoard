<template>
<jobs-list v-if="loadingIndicator" :jobs="companyVacancies" :isCompany="isCompany"/>
<div v-else> Loading ... </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import JobsList from '@/components/JobsList';

export default {
    name: "myAppliedJobs",
    components: {
        JobsList
    },

    data() {
        return{isCompany: true,}
    },

    methods: {
        ...mapActions({
            getMyCompanyVacancies: 'allUsers/getMyCompanyVacancies',
        }),
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
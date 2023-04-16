<template>
  <div class="row">
    <div class="col-8">
      <div class="row">
        <div class="col mt-3">
          <h3 class="text-left">Vacancies</h3>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <div v-if="user">
            <jobs-list :vacancies="user.vacancies" />
          </div>
          <div v-else> Loading ... </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import JobsList from '@/components/JobsList';

export default {
  name: "AppliedVacancies",
  components: {
    JobsList
  },
  methods: {
    ...mapActions({
      getVacancies: 'allVacancies/getVacancies'
    }),
  },
  computed: {
    ...mapState({
      vacancies: state => state.allVacancies.vacancies,
      loadingIndicator: state => state.allVacancies.vacanciesLoadingIndicator,
      user: state => state.allUsers.user
    }),
  }
}
</script>
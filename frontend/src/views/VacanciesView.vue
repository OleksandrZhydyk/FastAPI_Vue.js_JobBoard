<template>
  <div class="row">
    <div class="col-8">
      <div class="row">
        <div class="col mt-3">
          <h3 class="text-left">Vacancies</h3>
        </div>
        <div class="col mt-3">
          <select class="form-select float-end" aria-label="Sort by" style="width:auto;" v-model="selectedSort">
            <option disabled value="">Sort by</option>
            <option v-for="option in sortOptions" :key="option.value" :value="option.value">{{option.name}}</option>
          </select>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <div v-if="loadingIndicator">
            <jobs-list v-if="sortedVacancies.length" :vacancies="sortedVacancies"/>
            <div v-else class="fs-4 mt-5 mb-5 ms-3">No vacancies</div>
            <div class="row mt-2">
              <div class="col d-flex align-items-center">
                <button class="btn btn-primary me-2" @click='pageDecr' :disabled="currentPage === 1">&lt&lt; Previous</button>
                <span class="badge bg-secondary me-2 fs-4">{{currentPage}}</span>
                <button class="btn btn-primary me-2" @click='pageIncr' :disabled="currentPage === allPages">Next &gt&gt;</button>
              </div>
            </div>
          </div>
          <div v-else class="fs-4 mt-5 mb-5 ms-3"> Loading ... </div>
        </div>
      </div>
    </div>
    <div class="col-4">
    <h3 class="mt-3 ms-5 mb-4">Filters</h3>
      <div class="form-check form-switch mt-2 ms-5" v-for="(value, key) in categories" :key="key">
        <input class="form-check-input" type="checkbox" v-bind:value="value" v-model="filterCategories" role="switch">
        <label class="text-success fw-bold form-check-label">{{value}}</label>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import { isProxy, toRaw } from 'vue';
import JobsList from '@/components/JobsList';

export default {
  name: "Vacancies",
  components: {
    JobsList
  },
  data() {
    return {
      selectedSort: "",
      searchJobs: "",
      filterCategories: [],
      currentPage: 1,
      sortOptions: [
        {value: 'title', name: 'By title'},
        {value: 'created_at', name: 'By date'},
      ],
    }
  },
  methods: {
    ...mapActions({
      getVacancies: 'allVacancies/getVacancies',
    }),
    async pageIncr(){
      this.currentPage++
    },
    async pageDecr(){
      this.currentPage--
    },
  },
  computed: {
    ...mapState({
      vacancies: state => state.allVacancies.vacancies,
      loadingIndicator: state => state.allVacancies.vacanciesLoadingIndicator,
      user: state => state.allUsers.user,
      allPages: state => state.allVacancies.allPages,
      categories: state => state.allVacancies.categories,
      objOnPage: state => state.allVacancies.objOnPage,
    }),
    sortedVacancies(){
      if (this.vacancies){
        return [...this.vacancies.items].sort(
          (vacancy1, vacancy2) => vacancy1[this.selectedSort]?.localeCompare(vacancy2[this.selectedSort])
        )
      }
    }
  },
  mounted() {
    this.getVacancies({"size": this.objOnPage,
      "page": this.currentPage,
      "job_category": this.filterCategories,
      }
    )
  },
  watch: {
    currentPage(){
      let rawData = this.filterCategories
      if (isProxy(rawData)){
        rawData = toRaw(rawData)
      }
      this.getVacancies({"size": this.objOnPage,
        "page": this.currentPage,
        "job_categories": rawData,
        }
      );
    },
    filterCategories(){
      let rawData = this.filterCategories
      if (isProxy(rawData)){
        rawData = toRaw(rawData)
      }
      this.getVacancies({"size": this.objOnPage,
        "page": this.currentPage,
        "job_categories": rawData
        }
      )
    }
  }
}
</script>
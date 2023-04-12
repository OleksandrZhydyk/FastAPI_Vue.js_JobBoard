<template>

<div v-if="vacancyAppliers">
        <div class="row">
            <div class="col-md">
                <div class="p-3 py-5">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="text-right">Vacancy</h4>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-6">
                            <label class="labels" for="title">Title</label>
                            <input type="text" id="title" name="title" class="form-control" :value="vacancyAppliers.title" readonly/>
                        </div>
                        <div class="col-md-6">
                            <span class="float-end">Published: {{vacancyAppliers.created_at.substring(0, 10)}}</span>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-3">
                            <label class="labels" for="salary_from">Salary from</label>
                            <input type="number" :value="vacancyAppliers.salary_from" min="0" id="salary_from" name="salary_from" class="form-control" readonly/>
                        </div>
                        <div class="col-md-3">
                            <label class="labels" for="salary_up_to">Salary up to</label>
                            <input type="number" :value="vacancyAppliers.salary_to" min="0" id="salary_up_to" name="salary_to" class="form-control" readonly/>
                        </div>
                        <div class="col-md-3">
                            <label class="labels" for="category">Category</label>
                            <input type="text" :value="vacancyAppliers.category" min="0" id="category" name="category" class="form-control" readonly/>
                        </div>
                        <div class="col-md-3">
                            <label class="labels" for="email">Email</label>
                            <input type="text" :value="vacancyAppliers.email" min="0" id="email" name="email" class="form-control" readonly/>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-12">
                            <label class="labels" for="description">Description</label>
                            <textarea type="text" :value="vacancyAppliers.description" id="description" name="description" class="form-control" readonly rows="4"></textarea>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <div v-if="vacancyAppliers.appliers.length" v-for="applier in vacancyAppliers.appliers" :key="applier.id">
            <div class="card mt-3">
                <div class="card-header">
                    {{applier.email}}
                </div>
                <div class="card-body">
                    <h5 class="card-title">{{applier.name}}</h5>
                    <p class="card-text">{{applier.created_at}}</p>
                    <p class="card-text">{{applier.is_active}}</p>
                    <router-link
                        class="btn btn-outline-primary"
                        :to="{name:'applicantProfile', params: { id: applier.id }}">Profile
                    </router-link>
                </div>
            </div>
        </div>
        <div v-else> No applicants </div>
</div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {

    methods: {
        ...mapActions({
            getVacancyAppliers: 'allVacancies/getVacancyAppliers',
        }),
    },

    computed: {
        ...mapState({
            vacancyAppliers: state => state.allVacancies.vacancyAppliers,
        }),
    },
    created() {
        this.getVacancyAppliers(`${this.$route.params.id}`)
    },

}

</script>
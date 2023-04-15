<template>
    <form method="POST" style="overflow: hidden;">
        <div class="row">
            <div class="col-md">
                <div class="p-3 py-5">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="text-right">Vacancy</h4>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-6">
                            <label class="labels" for="title">Title</label>
                            <input type="text" id="title" name="title" class="form-control" v-model="vacancy.title" required="true"/>
                        </div>
                        <div class="col-md-6">
                            <div class="row mt-2">
                                <div class="col-md-8">
                                    <label class="labels float-end mt-2" for="category"> Category:  </label>
                                </div>
                                <div class="col-md-4">
                                    <select class="form-select float-end" id="category" aria-label="Select category" style="width:auto;" v-model="vacancy.category">
                                        <option v-for="(value, key) in this.categories" :key="key" :value="value">{{value}}</option>
                                    </select>
                                </div>
                             </div>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-3">
                            <label class="labels" for="salary_from">Salary from</label>
                            <input type="number" v-model="vacancy.salary_from"  min="0" id="salary_from" name="salary_from" class="form-control" required="true"/>
                        </div>
                        <div class="col-md-3">
                            <label class="labels" for="salary_up_to">Salary up to</label>
                            <input type="number" v-model="vacancy.salary_to"  min="0" id="salary_up_to" name="salary_to" class="form-control" required="true"/>
                        </div>
                        <div class="col-md-6">
                            <label class="labels" for="email">Contact email</label>
                            <input type="text" id="email" name="email" class="form-control" v-model="vacancy.email" required="true"/>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-12">
                            <label class="labels" for="description">Description</label>
                            <textarea type="text" v-model="vacancy.description" id="description" name="description" class="form-control" required="true" rows="4"></textarea>
                        </div>
                    </div>
                    <button type="button" @click="publishVacancy(vacancy)" class="btn btn-success mt-4">Create Vacancy</button>
                </div>
            </div>
        </div>
        <modal-error @modal="getModal" v-if="modal" :created="created" :modal="modal"/>
    </form>
</template>

<script>
import { mapActions, mapMutations, mapState, mapGetters } from 'vuex';
import ModalError from '@/components/ModalError';
import store from '@/store';

export default {
    name: "CreateVacancy",
    components: {
        ModalError
    },
    data(){
        return {
            vacancy: {
                title: '',
                email: '',
                description: '',
                salary_to: '',
                salary_from: '',
                category: 'Miscellaneous',
            },
            modal: false,
            created: false,
        }
    },
    methods: {
        ...mapActions({
            createVacancy: 'allVacancies/createVacancy',
        }),
        getModal(event){
            this.modal = false
            this.updated = false
            this.created = false
            if (this.errors === null) {
                this.$router.push('/me/vacancies');
            } else {
                store.commit('allUsers/setErrors', null);
            }
        },
        async publishVacancy(vacancy){
            try {
                const res = await this.createVacancy(vacancy)
                if (res){
                    this.modal = true
                    this.created = true
                } else {
                    this.modal = true
                }
            } catch(e){
                console.log(e);
            }
        },
    },
    computed: {
        ...mapState({
            categories: state => state.allVacancies.categories,
            errors: state => state.allUsers.errors
        }),
    },
}
</script>

<template>
    <form v-if="vacancy" method="POST" style="overflow: hidden;">
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
                            <span class="float-end">Updated: {{vacancy.updated_at.substring(0, 10)}}</span>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-6">
                            <label class="labels" for="salary_from">Salary from</label>
                            <input type="number" v-model="vacancy.salary_from"  min="0" id="salary_from" name="salary_from" class="form-control" required="true"/>
                        </div>
                        <div class="col-md-6">
                            <label class="labels" for="salary_up_to">Salary up to</label>
                            <input type="number" v-model="vacancy.salary_to"  min="0" id="salary_up_to" name="salary_to" class="form-control" required="true"/>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-12">
                            <label class="labels" for="description">Description</label>
                            <textarea type="text" v-model="vacancy.description" id="description" name="description" class="form-control" required="true" rows="4"></textarea>
                        </div>
                    </div>
                    <button type="button" @click="modifyVacancy(vacancy)" class="btn btn-warning mt-4">Update</button>
                </div>
            </div>
        </div>
        <modal-error @modal="getModal" v-if="modal" :updated="updated" :modal="modal"/>
    </form>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import ModalError from '@/components/ModalError';
import store from '@/store';

export default {
    data() {
        return {
            vacancy: null,
            modal: false,
            updated: false,
        }
    },
    components: {
        ModalError
    },
    computed: {
        ...mapState({
            errors: state => state.allUsers.errors
        }),
    },
    methods: {
        ...mapActions({
            updateVacancy: 'allVacancies/updateVacancy'
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
        async modifyVacancy(vacancy){
            try {
                let data = {
                  "id": vacancy.id,
                  "email": vacancy.email,
                  "title": vacancy.title,
                  "description": vacancy.description,
                  "salary_from": vacancy.salary_from.toString(),
                  "salary_to": vacancy.salary_to.toString()
                }
                let res = await this.updateVacancy(data)
                if (res){
                    this.modal = true
                    this.updated = true
                } else {
                    this.modal = true
                }
            } catch(e){
                console.log(e);
            }
        },
    },
    mounted() {
        this.vacancy = this.$route.query;
      }
  }
</script>

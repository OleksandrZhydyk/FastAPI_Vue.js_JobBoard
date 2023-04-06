<template>
<form method="GET" v-if="vacancy">
        <div class="row">
            <div class="col-md">
                <div class="p-3 py-5">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="text-right">Vacancy</h4>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-6">
                            <label class="labels" for="title">Title</label>
                            <input type="text" id="title" name="title" class="form-control" :value="vacancy.title" readonly/>
                        </div>
                        <div class="col-md-6">
                            <label class="labels" for="created_at">Published</label>
                            <input type="text" id="created_at" name="created_at" class="form-control" :value="vacancy.created_at.substring(0, 10)" readonly/>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-6">
                            <label class="labels" for="salary_from">Salary from</label>
                            <input type="number" :value="vacancy.salary_from" min="0" id="salary_from" name="salary_from" class="form-control" readonly/>
                        </div>
                        <div class="col-md-6">
                            <label class="labels" for="salary_up_to">Salary up to</label>
                            <input type="number" :value="vacancy.salary_to" min="0" id="salary_up_to" name="salary_to" class="form-control" readonly/>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-12">
                            <label class="labels" for="description">Description</label>
                            <textarea type="text" :value="vacancy.description" id="description" name="description" class="form-control" readonly rows="4"></textarea>
                        </div>
                    </div>

                   <button type="button" v-if="isLoggedIn && !applied" @click="applyJob(this.vacancy.id, this.user.id)"
                   class="btn btn-primary mt-4">Apply</button>
                   <button type="button" v-if="isLoggedIn && applied" class="btn btn-warning mt-4">Applied</button>
                   <DialogLogin v-if="!isLoggedIn" />

                    <ModalError ref="error" />
                </div>
            </div>
        </div>
    </form>
</template>

<script>
import { mapActions, mapMutations, mapState, mapGetters } from 'vuex';
import DialogLogin from '@/components/DialogLogin';
import ModalError from '@/components/ModalError';

export default {
    name: "JobDetail",
    components: {
        DialogLogin,
        ModalError
    },
    methods: {
        ...mapActions({
            getVacancy: 'allVacancies/getVacancy',
            applyToVacancy: 'allVacancies/applyToVacancy',
        }),
        ...mapMutations({
            addAppliedVacancy: 'allUsers/addAppliedVacancy',
        }),

        async applyJob(vacancyId, userId){
            try {
                const res = await this.applyToVacancy(vacancyId, userId)
                if (res === true){
                    await this.addAppliedVacancy(this.vacancy)
                } else {
                    this.$refs.error.click();
                }
            } catch(e){
                console.log(e);
            }
        },
    },
    computed: {
        ...mapState({
            vacancy: state => state.allVacancies.vacancy,
            user: state => state.allUsers.user,
        }),
        ...mapGetters({
            isLoggedIn: 'allUsers/isAuthenticated',
        }),
        applied(){
            if (this.user &&  this.vacancy){
                for (let i=0; i<this.user.vacancies.length; i++){
                    if (this.user.vacancies[i].id === this.vacancy.id){
                        return true
                    }
                }
            }
            return false
        },

    },
    mounted() {
        this.getVacancy(`${this.$route.params.id}`)
    },

}

</script>
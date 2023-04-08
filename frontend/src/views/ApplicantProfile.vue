<template>
    <div v-if="applicant">
        <div class="row">
            <div class="col-md">
                <div class="p-3 py-5">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="text-right">Profile</h4>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-6">
                            <label class="labels" for="title">Title</label>
                            <input type="text" id="title" name="title" class="form-control" :value="applicant.name" readonly/>
                        </div>
                        <div class="col-md-6">
                            <span class="float-end">Published: {{}}</span>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-3">
                            <label class="labels" for="salary_from">Salary from</label>
                            <input type="number" :value="applicant.email" min="0" id="salary_from" name="salary_from" class="form-control" readonly/>
                        </div>
                        <div class="col-md-3">
                            <label class="labels" for="salary_up_to">Salary up to</label>
                            <input type="number" min="0" id="salary_up_to" name="salary_to" class="form-control" readonly/>
                        </div>
                        <div class="col-md-3">
                            <label class="labels" for="category">Category</label>
                            <input type="text"  min="0" id="category" name="category" class="form-control" readonly/>
                        </div>
                        <div class="col-md-3">
                            <label class="labels" for="email">Email</label>
                            <input type="text"  min="0" id="email" name="email" class="form-control" readonly/>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-md-12">
                            <label class="labels" for="description">Description</label>
                            <textarea type="text" id="description" name="description" class="form-control" readonly rows="4"></textarea>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
    name: "ApplicantProfile",

    methods: {
        ...mapActions({
            getUser: 'allUsers/getUser',
        }),
    },
    computed: {
        ...mapState({
            applicant: state => state.allUsers.applicant,
        }),
    },
    created() {
        this.getUser(`${this.$route.params.id}`)
    },
}

</script>
<template>
    <div v-if="applicant">
        <div class="container rounded mt-5 mb-5">
            <div class="row">
                <div class="col-md-4">
                    <div v-if="applicant.avatar" class="d-flex flex-column align-items-center text-center p-3 py-5 mt-3"><img
                            class="rounded-circle"
                            :src="applicant.avatar"
                            alt="avatar">
                    </div>
                    <div v-else class="d-flex flex-column align-items-center text-center p-3 py-5 mt-3"><img
                            class="rounded-circle"
                            src="http://localhost:8000/static/default_imgs/empty_avatar.png"
                            alt="avatar">
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="p-3 py-5">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h4 class="text-right">Profile</h4>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-6"><label class="labels">First Name</label>
                                <input type="text" :value="applicant.name" id="name" name="name" class="form-control" readonly/>

                            </div>
                            <div class="col-md-6"><label class="labels">Resume:</label>
                            </div>
                        </div>
                        <div class="row ">
                            <div class="col-md-6 mt-3"><label class="labels">Email</label>
                                <input type="text" :value="applicant.email" id="email" name="email" class="form-control" readonly/>
                            </div>
                            <div v-if="applicant.resume" class="col-md-6">
                                <a :href="applicant.resume">
                                    <img src="http://localhost:8000/static/default_imgs/pdf_download.png" style="width:75px;height:75px;">
                                </a>
                            </div>
                            <div v-else class="col-md-6">
                               <img src="http://localhost:8000/static/default_imgs/gray_pdf.png" style="width:75px;height:75px;">
                            </div>
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
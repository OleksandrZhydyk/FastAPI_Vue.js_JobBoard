<template>
    <div v-if="user">
        <div class="container rounded mt-5 mb-5">
            <form @submit.prevent="submit" enctype="multipart/form-data">
                <div class="row">
                    <div class="col-md-4">
                        <div v-if="user.avatar" class="d-flex flex-column align-items-center text-center p-3 py-5 mt-3"><img
                            class="rounded-circle"
                            :src="user.avatar"
                            alt="avatar">

                            <input @change="handleAvatarUpload($event)" type="file" name="avatar" class="form-control mt-2" accept="image/*" id="id_avatar">
                            <input  v-model="clearAvatar" class="me-2" type="checkbox" name="photo-clear" id="photo-clear_id">
                            <label for="photo-clear_id">Delete photo</label>

                        </div>
                        <div v-else class="d-flex flex-column align-items-center text-center p-3 py-5 mt-4"><img
                                class="rounded-circle"
                                src="media/default_imgs/empty_avatar.png"
                                alt="avatar">
                                <input @change="handleAvatarUpload($event)" type="file" name="avatar" class="form-control mt-2" accept="image/*" id="id_avatar">
                        </div>

                    </div>
                    <div class="col-md-6">
                        <div class="p-3 py-5">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h4 class="text-right">Profile</h4>
                            </div>
                            <div class="row mt-3">
                                <div class="col-md-6"><label class="labels">First Name</label>
                                    <input type="text"
                                    :value="user.name" @input="handleNameUpload($event);"
                                    id="name" name="name" class="form-control"/>
                                </div>
                                <div class="col-md-6"><label class="labels">Email</label>
                                    <input type="text"
                                     :value="user.email" @input="handleEmailUpload($event);"
                                     id="email" name="email" class="form-control"/>
                                </div>
                            </div>
                            <div v-if="user.resume" class="row mt-3">
                                <div class="col-md-6">
                                    <a :href="user.resume">
                                        <img class="d-block float-end" src="media/default_imgs/pdf_download.png" style="width:75px;height:75px;">
                                    </a>
                                </div>
                                <div v-if="user.resume" class="col-md-6">
                                    <input @change="handleResumeUpload($event)" type="file" name="resume" class="form-control mt-3" accept="image/*" id="id_file">
                                    <input v-model="clearResume" class="me-2" type="checkbox" name="file-clear" id="file-clear_id">
                                            <label for="file-clear_id">Delete resume</label>
                                </div>
                            </div>
                            <div v-else class="row mt-3">
                                <div class="col-md-6">
                                   <img class="d-block float-end" src="media/default_imgs/gray_pdf.png" style="width:75px;height:75px;">
                                </div>
                                <div class="col-md-6">
                                    <input @change="handleResumeUpload($event)" type="file" name="resume" class="form-control mt-3" accept="image/*" id="id_file">
                                </div>
                            </div>
                            <button type="submit" class="btn btn-warning float-end mt-5">Update</button>
                        </div>
                    </div>
                </div>
                <modal-error @modal="getModal" v-if="modal" :updated="updated" :error="error" :modal="modal"/>
            </form>
        </div>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import ModalError from '@/components/ModalError';

export default {
    name: "UserProfile",
    components: {
        ModalError
    },
    data(){
        return {
            name: "",
            email: "",
            password: "",
            resume: null,
            clearResume: false,
            clearAvatar: false,
            avatar: null,
            modal: false,
            updated: false,
            error: false,
        }
    },

  methods: {
    ...mapActions({
        updateProfile: 'allUsers/updateProfile',
        logOut: 'allUsers/logOut',
        viewMe: 'allUsers/viewMe',
    }),
    getModal(event){
        this.modal = false,
        this.error = false,
        this.updated = false,
        this.created = false
    },
    handleResumeUpload(event){
        this.resume = event.target.files[0];
    },
    handleAvatarUpload(event){
        this.avatar = event.target.files[0];
    },
    handleNameUpload( event ){
        this.name = event.target.value;
    },
    handleEmailUpload( event ){
        console.log(event.target.value)
        this.email = event.target.value;
    },

    async submit() {
      const form_data = new FormData();
      form_data.append('name', this.name);
      form_data.append('email', this.email);
      form_data.append('password', this.password);
      form_data.append('clear_avatar', this.clearAvatar);
      form_data.append('clear_resume', this.clearResume);
      if (this.avatar){
        form_data.append('avatar', this.avatar);
      }
      if (this.resume){
        form_data.append('resume', this.resume);
      }
      let res = await this.updateProfile(form_data);
      if (res === true){
        this.modal = true,
        this.updated = true
      } else {
        this.modal = true,
        this.error = true
      }
      this.clearAvatar = false
      this.clearResume = false
      if (this.email || this.password){
        await this.logOut();
        this.$router.push('/login');
      } else {
        await this.viewMe();
        this.$router.push('/me');
      }
    }
  },
  computed: {
      ...mapState({
          user: state => state.allUsers.user,
      }),

  },
}

</script>
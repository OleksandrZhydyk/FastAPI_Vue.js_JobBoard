<template>
    <div class="row mt-2">
        <div class="col-8 mt-3">
            <h3 class="text-left">Archived vacancies</h3>
        </div>
    </div>
    <div class="row">
        <div class="col">
            <div v-for="vacancy in this.archivedVacancies" :key="vacancy.id">
                <div class="card mt-3">
                    <div class="card-header">
                        <span>{{vacancy.title}}</span>
                        <span class="float-end">Updated: {{vacancy.updated_at.substring(0, 10)}}</span>
                    </div>
                    <div class="card-body">
                        <p class="card-text">{{vacancy.category}}</p>
                        <h5 class="card-title">{{vacancy.description}}</h5>
                        <a href="#" class="btn btn-primary" @click="$router.push(`/vacancies/${vacancy.id}/appliers`)">Get Appliers</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
    name: "archivedVacancies",
    computed: {
        ...mapState({
            companyVacancies: state => state.allUsers.companyVacancies,
        }),
        archivedVacancies(){
            return [...this.companyVacancies].filter((vacancy) => !vacancy.is_active)
        }
    },
}
</script>
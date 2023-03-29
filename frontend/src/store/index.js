import { createStore } from "vuex";
import { usersModule } from "@/store/modules/users.js"
import { jobsModule } from "@/store/modules/jobs.js"


export default createStore({
  modules: {
    allUsers: usersModule,
    allJobs: jobsModule,
  }
});
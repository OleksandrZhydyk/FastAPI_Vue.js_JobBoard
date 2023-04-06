import { createStore } from "vuex";
import { usersModule } from "@/store/modules/users.js"
import { vacanciesModule } from "@/store/modules/vacancies.js"


export default createStore({
  modules: {
    allUsers: usersModule,
    allVacancies: vacanciesModule,
  }
});
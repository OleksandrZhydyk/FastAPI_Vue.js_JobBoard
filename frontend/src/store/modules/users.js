import axios from 'axios';

export const usersModule = {
  state: () => (
    { user: null,
      companyVacancies: [],
      myVacanciesLoadingIndicator: false,
      applicant: null,
      errors: null,
      refreshExpired: false
    }
  ),

  getters: {
    isAuthenticated: state => !!state.user,
    stateUser: state => state.user,
    isCompany: state => state.user ? state.user.is_company : false
  },

  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setCompanyVacancies(state, vacancies) {
      state.companyVacancies = vacancies;
    },
    setMyVacanciesLoadingIndicator(state, bool) {
      state.myVacanciesLoadingIndicator = bool;
    },
    deleteMyVacancies(state, id) {
      state.companyVacancies = state.companyVacancies.filter(item => item.id !== id )
    },
    addAppliedVacancy(state, vacancy){
      state.user.vacancies.push(vacancy)
    },
    setApplicant(state, applicant){
      state.applicant = applicant
    },
    setRefreshExpired(state, bool){
      state.refreshExpired = bool
    },
    setErrors(state, errors) {
      if (Array.isArray(errors)){
        let msg = []
        for (let i=0; i<errors.length; i++){
          msg.push(errors[i].loc[1] +": " + errors[i].msg)
        }
        state.errors = msg;
      } else if (errors === null){
        state.errors = null;
      } else {
        state.errors = [errors];
      }
    },
  },

    actions: {
      async logIn({dispatch}, form_data) {
        try {
          const res = await axios.post('/auth/login', form_data);
          if (res && res.status === 200){
            await dispatch('viewMe');
            return true
          } else {
            return false
          }
        } catch(e) {
          console.log(e)
        }
      },
      async viewMe({commit}) {
        const {data} = await axios.get('users/me');
        await commit('setUser', data);
      },
      async updateProfile({}, form_data) {
        try {
          const res = await axios.put('users/me', form_data,
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              },
            }
          );
          if (res && res.status === 200) {
            return true
          }
          return false
        } catch(e) {
          console.log(e)
        }
      },
      async getMyCompanyVacancies({commit}) {
        try {
          const res = await axios.get('vacancies/me');
          if (res && res.status === 200) {
            await commit('setCompanyVacancies', res.data);
          }
        } catch(e) {
          console.log(e)
        } finally {
          commit('setMyVacanciesLoadingIndicator', true);
        }
      },
      async getUser({commit}, id) {
        const {data} = await axios.get(`users/${id}`);
        await commit('setApplicant', data);
      },
      async createUser({}, payload) {
        try {
          const res = await axios.post("users/", payload);
          if (res && res.status === 200) {
            return true
          }
        } catch(e) {
          console.log(e)
        }
      },

      async logOut({commit}){
        try {
          const res = await axios.delete('/auth/logout');
          if (res && res.data.msg === "Successfully logout"){
            const user = null
            await commit('setUser', user);
          }
        } catch(e) {
          console.log(e)
        }
      }
    },
  namespaced: true,
};

import axios from 'axios';

export const usersModule = {
    state: () => (
        { user: null,
          companyVacancies: [],
          myVacanciesLoadingIndicator: false,
          applicant: null,
         }
    ),

    getters: {
      isAuthenticated: state => !!state.user,
      stateUser: state => state.user,
      isCompany: state => state.user ? state.user.is_company : false,
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
        }
    },

    actions: {
      async logIn({dispatch}, form_data) {
          try {
            const res = await axios.post('/auth/login', form_data);
            await dispatch('viewMe');
          } catch(e) {
            console.log(e)
          }
      },
      async viewMe({commit}) {
        let {data} = await axios.get('/users/me');
        await commit('setUser', data);
      },
      async updateProfile({}, form_data) {
          try {
            const res = await axios.put('/users/me', form_data,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                }
            );
            if (res.status !== 200) {
                return false
            }
            return true
          } catch(e) {
            console.log(e)
          }
      },
      async getMyCompanyVacancies({commit}) {
          try {
            let res = await axios.get('/vacancies/me');
            await commit('setCompanyVacancies', res.data);
          } catch(e) {
            console.log(e)
          } finally {
            commit('setMyVacanciesLoadingIndicator', true);
          }
      },
      async getUser({commit}, id) {
        let {data} = await axios.get(`/users/${id}`);
        await commit('setApplicant', data);
      },
      async createUser({}, payload) {
        let {data} = await axios.post("/users", payload);
      },

      async logOut({commit}){
        try {
            const res = await axios.delete('/auth/logout');
            if (res.data.msg === "Successfully logout"){
                let user = null
                await commit('setUser', user);
            } else {
                console.log(res)
            }
          } catch(e) {
            console.log(e)
          }
      }
    },
  namespaced: true,
};


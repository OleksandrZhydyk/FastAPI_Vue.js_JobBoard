import axios from 'axios';

export const vacanciesModule = {
    state: () => (
        { vacancies: {},
          vacanciesLoadingIndicator: false,
          vacancy: null,
          vacancyAppliers: null,
          allPages: 0,
          categories: null,
          objOnPage: 5,
         }
    ),

    getters: {
        isAuthenticated: state => !!state.user,
        stateVacancies: state => state.vacancies,
    },

    mutations: {
        setVacancies(state, vacancies){
            state.vacancies = vacancies;
        },
        setVacancy(state, vacancy){
            state.vacancy = vacancy;
        },
        setLoadingIndicator(state, bool){
            state.vacanciesLoadingIndicator = bool
        },
        setVacancyAppliers(state, appliers){
            state.vacancyAppliers = appliers
        },
        setAllPages(state, pages){
            state.allPages = pages;
        },
        setAllCategories(state, categories){
            state.categories = categories;
        },
    },

    actions: {
      async getVacancies({commit}, params) {
        try {
            const {data} = await axios.get('vacancies/',
                {
                    params: params,
                    paramsSerializer: {
                        indexes: null
                    },
                });
            if (data){
              commit('setVacancies', data);
              commit('setAllPages', data.pages);
              commit('setAllCategories', data.categories);
            }
        } catch(e) {
            console.log(e)
        } finally {
            commit('setLoadingIndicator', true);
        }
      },
      async getVacancy({commit}, id) {
        const {data} = await axios.get(`vacancies/${id}`);
        commit('setVacancy', data);
      },

      async getVacancyAppliers({commit}, id) {
        const {data} = await axios.get(`vacancies/${id}/apply`);
        commit('setVacancyAppliers', data);
      },
      async createVacancy({}, payload) {
        try{
          const res = await axios.post('vacancies/', payload);
          if (res && res.status === 200) {
            return true
          }
        } catch(e) {
          console.log(e)
        }
      },
      async updateVacancy({}, data) {
        try{
          const {id, ...params} = data
          const res = await axios.put(`vacancies/${id}`, params);
          if (res && res.status === 200) {
            return true
          }
        } catch(e) {
          console.log(e)
        }
      },
      async deleteVacancy({}, id) {
        try {
          const res = await axios.delete(`vacancies/${id}`);
          if (res && res.status === 200) {
            return true
          }
        } catch(e) {
          console.log(e)
        }
      },
      async applyToVacancy({}, vacancyId, userId) {
        try {
          const res = await axios.post(`vacancies/${vacancyId}/apply`, userId);
          if (res && res.status === 200) {
              return true
          }
        } catch(e) {
          console.log(e)
        }
      },
    },
  namespaced: true,
};
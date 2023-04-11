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
            let {data} = await axios.get('vacancies/',
                {
                    params: params,
                    paramsSerializer: {
                        indexes: null
                    },
                });
            commit('setVacancies', data);
            commit('setAllPages', data.pages);
            commit('setAllCategories', data.categories);
        } catch(e) {
            console.log(e)
        } finally {
            commit('setLoadingIndicator', true);
        }
      },
      async getVacancy({commit}, id) {
        let {data} = await axios.get(`vacancies/${id}`);
        commit('setVacancy', data);
      },

      async getVacancyAppliers({commit}, id) {
        let {data} = await axios.get(`vacancies/${id}/apply`);
        commit('setVacancyAppliers', data);
      },
      async createVacancy({}, payload) {
        let res = await axios.post('vacancies/', payload);
        if (res.status !== 200) {
            return false
        }
        return true
      },
      async updateVacancy({}, data) {
        const {id, ...params} = data
        let res = await axios.put(`vacancies/${id}`, params);
        if (res.status !== 200) {
            return false
        }
        return true
      },
      async deleteVacancy({}, id) {
        let res = await axios.delete(`vacancies/${id}`);
        if (res.status !== 200) {
            return false
        }
        return true
      },
      async applyToVacancy({}, vacancyId, userId) {
        let res = await axios.post(`vacancies/${vacancyId}/apply`, userId);
        if (res.status !== 200) {
            return false
        }
        return true
      },
    },
  namespaced: true,
};
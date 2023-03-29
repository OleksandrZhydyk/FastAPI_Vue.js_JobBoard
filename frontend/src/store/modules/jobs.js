import axios from 'axios';

export const jobsModule = {
    state: () => (
        { jobs: {},
          jobsLoadingIndicator: false,
          job: {},
          jobAppliers: null,
         }
    ),

    getters: {
      stateJobs: state => state.jobs,
    },

    mutations: {
        setJobs(state, jobs){
            state.jobs = jobs;
        },
        setJob(state, job){
            state.job = job;
        },
        setLoadingIndicator(state, bool){
            state.jobsLoadingIndicator = bool
        },
        setJobAppliers(state, appliers){
            state.jobAppliers = appliers
        }
    },

    actions: {
      async getJobs({commit}) {
        try {
            let {data} = await axios.get('jobs/');
            commit('setJobs', data);
        } catch(e) {
            console.log(e)
        } finally {
            commit('setLoadingIndicator', true);
        }
      },
      async getJob({commit}, id) {
        let {data} = await axios.get(`jobs/${id}`);
        commit('setJob', data);
      },

      async getJobAppliers({commit}, id) {
        let {data} = await axios.get(`jobs/${id}/apply`);
        commit('setJobAppliers', data);
      },
      async deleteJob({}, id) {
        await axios.delete(`jobs/${id}`);
      },
    },
  namespaced: true,
};
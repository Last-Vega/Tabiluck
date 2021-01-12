import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

// // sakuta↓
const initialState = {
  userName: '',
  searchResults: []
}

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: initialState,
  mutations: {
    changeResult (state, results) {
      state.searchResults = results
    },
    loginUser (state, name) {
      state.userName = name
    }
  },
  getters: {
    getSearchResults (state) {
      return state.searchResults
    },
    getUserName (state) {
      return state.userName
    }
  }
})

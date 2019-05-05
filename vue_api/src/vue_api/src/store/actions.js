import axios from 'axios'
import jwtDecode from 'jwt-decode'

export default {
  obtainToken: ({ commit, state }, payload) => {
    return axios.post(state.endpoints.obtainJwt, payload)
      .then((response) => {
        commit('setTokens', response.data)
      })
      .catch((error) => {
        let errorMsg = ''
        if (error.response) {
          if (error.response.status === 400) {
            errorMsg = 'Wrong username or password.'
          }
          // more specific messages can be added here
        } else {
          errorMsg = 'Something gone wrong.'
        }
        commit('updateLoginError', errorMsg)
      })
  },
  refreshToken: ({ state, commit }) => {
    const payload = {
      refresh: state.jwtRefresh
    }

    axios.post(state.endpoints.refreshJwt, payload)
      .then(response => {
        commit('updateAccessToken', response.data.access)
      })
      .catch(() => {
        commit('removeTokens')
      })
  },
  removeTokens: ({ commit }) => {
    commit('removeTokens')
  },
  inspectToken: ({ state, commit, dispatch }) => {
    const accessToken = state.jwtAccess
    const refreshToken = state.jwtRefresh

    if (accessToken) {
      const accessDecoded = jwtDecode(accessToken)
      const refreshDecoded = jwtDecode(refreshToken)
      const accessExp = accessDecoded.exp
      const refreshExp = refreshDecoded.exp
      const now = Date.now() / 1000

      if (accessExp < now && refreshExp > now) {
        dispatch('refreshToken')
      } else if (refreshExp < now) {
        commit('removeTokens')
      }
    }
  }
}

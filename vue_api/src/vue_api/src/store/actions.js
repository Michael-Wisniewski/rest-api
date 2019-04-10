import axios from 'axios'
import jwtDecode from 'jwt-decode'

export default {
  obtainToken: ({ commit, state }, payload) => {
    axios.post(state.endpoints.obtainJwt, payload)
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
      refresh: this.state.jwtRefresh
    }

    axios.post(this.state.endpoints.refreshJwt, payload)
      .then((response) => {
        this.commit('updateAccessToken', response.data.access)
      })
      .catch(() => {
        commit('removeTokens')
      })
  },
  removeTokens: ({ commit }) => {
    commit('removeTokens')
  },
  inspectToken: ({ state, commit }) => {
    const accessToken = state.jwtAccess
    const refreshToken = state.jwtRefresh

    if (accessToken) {
      const accessDecoded = jwtDecode(accessToken)
      const refreshDecoded = jwtDecode(refreshToken)
      const accessExp = accessDecoded.exp
      const refreshExp = refreshDecoded.exp

      if (accessExp - (Date.now() / 1000) < 1800 && (refreshExp - Date.now() / 1000) < 628200) {
        this.refreshToken()
      } else if (refreshExp < Date.now() / 1000) {
        commit('removeTokens')
      }
    }
  }
}

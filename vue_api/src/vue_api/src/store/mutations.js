export default {
  updateLoginError: (state, errorMsg) => {
    state.loginError = errorMsg
  },
  setTokens: (state, payload) => {
    state.jwtAccess = payload.access
    state.jwtRefresh = payload.refresh
    state.loginError = ''
    localStorage.setItem('jwtAccess', payload.access)
    localStorage.setItem('jwtRefresh', payload.refresh)
  },
  updateAccessToken: (state, newToken) => {
    localStorage.setItem('jwtAccess', newToken)
    state.jwtAccess = newToken
  },
  removeTokens: (state) => {
    localStorage.removeItem('jwtAccess')
    localStorage.removeItem('jwtRefresh')
    state.jwtAccess = null
    state.jwtRefresh = null
    state.loginError = ''
  }
}

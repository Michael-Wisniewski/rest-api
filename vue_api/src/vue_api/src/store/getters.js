export default {
  isAuthenticated: (state) => {
    if (state.jwtAccess) {
      return true
    } else {
      return false
    }
  },
  loginError: (state) => {
    return state.loginError
  },
  headers: (state) => {
    const config = {
      headers: {
        Authorization: 'Bearer ' + state.jwtAccess
      }
    }
    return config
  }
}

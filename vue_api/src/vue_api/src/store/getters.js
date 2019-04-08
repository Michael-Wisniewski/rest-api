export default {
  isAuthenticated: (state) => {
    if (state.jwtAccess) {
      return true
    } else {
      return false
    }
  }
}

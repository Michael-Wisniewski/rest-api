export default {
  jwtAccess: localStorage.getItem('jwtAccess'),
  jwtRefresh: localStorage.getItem('jwtRefresh'),
  loginError: '',
  endpoints: {
    obtainJwt: 'http://localhost:80/v1/api/token/',
    refreshJwt: 'http://localhost:80/v1/api/token/refresh/'
  }
}

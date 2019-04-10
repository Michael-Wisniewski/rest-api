import axios from 'axios'

export default {
  obtainToken: ({ commit, state }, payload) => {
    axios.post(state.endpoints.obtainJwt, payload)
      .then((response) => {
        console.log(response.data)
      })
  },
  inspectToken () {
    console.log('w inspect')
    return true
  }
}

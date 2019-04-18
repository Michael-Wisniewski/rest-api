<template>
  <div id="nav-bar" class="bottom-shadow">
    <b-navbar :variant="variant" type="dark">
      <b-navbar-brand>
        {{ user | capitalize }} Exam Panel
      </b-navbar-brand>
      <b-button v-show="isAuthenticated" @click="logOut" :variant="'outline-' + variant" class="ml-auto" size="lg">Log Out</b-button>
    </b-navbar>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'NavBar',
  props: [
    'user',
    'variant'
  ],
  computed: {
    ...mapGetters([
      'isAuthenticated'
    ])
  },
  filters: {
    capitalize (user) {
      return user.charAt(0).toUpperCase() + user.slice(1)
    }
  },
  methods: {
    ...mapActions([
      'removeTokens'
    ]),
    logOut () {
      this.removeTokens()
      this.$router.push({ path: '/' })
    }
  }
}
</script>

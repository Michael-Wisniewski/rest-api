<template>
  <b-modal
    v-model="show"
    centered
    class="text-center"
    header-text-variant="light"
    :title="'Login to ' + user +'\'s account'"
    :header-bg-variant="variant"
  >
    <p class="my-4">
      User name:
    </p>
    <p class="my-4">
      Password:
      <input />
    </p>
    <div slot="modal-footer" class="w-100" text-center>
      <b-button
        :variant="variant"
        size="xl"
        class="ml-auto"
        @click="show=false"
      >
        Log In
      </b-button>
    </div>
  </b-modal>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'AuthModel',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  props: [
    'user',
    'variant'
  ],
  computed: {
    ...mapGetters([
      'isAuthenticated'
    ]),
    show () {
      return !this.isAuthenticated
    }
  }
}
</script>

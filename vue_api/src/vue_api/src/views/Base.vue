<template>
  <div>
    <nav-bar
      :user="user"
      :variant="variant"
    />
    <b-container fluid>
      <transition name="bounce" mode="out-in">
      <router-view/>
      </transition>
      <auth-modal
        :user="user"
        :variant="variant"
      />
    </b-container>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import NavBar from '@/components/NavBar'
import AuthModal from '@/components/AuthModal'

export default {
  name: 'Base',
  data () {
    return {
      user: 'anonymous',
      variant: 'secondary'
    }
  },
  components: {
    NavBar,
    AuthModal
  },
  created () {
    if (this.$route.meta.user) {
      this.user = this.$route.meta.user
    }

    if (this.user === 'schoolboy') {
      this.variant = 'success'
    } else if (this.user === 'teacher') {
      this.variant = 'primary'
    }
  },
  methods: {
    ...mapActions([
      'inspectToken'
    ])
  },
  updated () {
    this.inspectToken()
  },
  mounted () {
    this.showModal = this.inspectToken()
  }
}
</script>

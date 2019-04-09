<template>
  <b-modal
    id="auth-modal"
    v-model="show"
    centered
    header-text-variant="light"
    no-close-on-backdrop
    :title="'Login to ' + user +'\'s account'"
    :header-bg-variant="variant"
  >
    <div slot="modal-header-close">
      <router-link to="/" class="close-btn">
        X
      </router-link>
    </div>

    <b-form-group
      label="Username :"
      class="mt-4"
      label-cols-sm="4"
      description="The minimum length is 4 characters."
      :invalid-feedback="usernameValidationText"
      :state="usernameValidation"
    >
      <b-form-input
        ref="username"
        v-model="username"
        :state="usernameValidation"
        required
        placeholder="Enter username"
        @keyup.enter="$refs.password.focus"
      ></b-form-input>
    </b-form-group>

    <b-form-group
      label="Password :"
      class="mt-3"
      label-cols-sm="4"
      description="The minimum length is 6 characters."
      :invalid-feedback="passwordValidationText"
      :state="passwordValidation"
    >
      <b-form-input
        ref="password"
        v-model="password"
        required
        placeholder="Enter password"
        :state="passwordValidation"
        :type="showPasssword ? 'text' : 'password'"
        @keyup.enter="login"
      ></b-form-input>
    </b-form-group>

    <b-form-checkbox
      v-model="showPasssword"
      class="text-center"
    >
      Show password
    </b-form-checkbox>

    <transition name="fade">
    <div id="connection" v-if="isChecking">
     <div class="loader">Loading...</div>
    </div>
    </transition>

    <div slot="modal-footer" class="w-100 text-center">
      <b-button
        :variant="variant"
        :disabled="isChecking"
        size="xl"
        @click="login"
      >
        Log In
      </b-button>
    </div>

  </b-modal>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'AuthModal',
  data () {
    return {
      username: '',
      password: '',
      showPasssword: false,
      usernameValidation: undefined,
      usernameValidationText: '',
      passwordValidation: undefined,
      passwordValidationText: '',
      isChecking: false
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
  },
  methods: {
    login () {
      if (this.validateData()) {
        this.isChecking = true
      }
    },
    validateData () {
      if (!this.usernameValidation || !this.passwordValidation) {
        if (!this.passwordValidation) {
          this.passwordValidation = false
          this.$nextTick(function () {
            this.$refs.password.focus()
          })
          this.checkPassword()
        }

        if (!this.usernameValidation) {
          this.usernameValidation = false
          this.$nextTick(function () {
            this.$refs.username.focus()
          })
          this.checkUsername()
        }
        return false
      } else {
        return true
      }
    },
    checkUsername () {
      if (this.username.length >= 4) {
        this.usernameValidation = true
      } else if (typeof this.usernameValidation !== 'undefined') {
        this.usernameValidation = false

        if (this.username.length === 0) {
          this.usernameValidationText = 'Please fill out this field.'
        } else {
          this.usernameValidationText = 'User\'s name is too short'
        }
      }
    },
    checkPassword () {
      if (this.password.length >= 6) {
        this.passwordValidation = true
      } else if (typeof this.passwordValidation !== 'undefined') {
        this.passwordValidation = false

        if (this.password.length === 0) {
          this.passwordValidationText = 'Please fill out this field.'
        } else {
          this.passwordValidationText = 'Password is too short'
        }
      }
    }
  },
  watch: {
    username () {
      this.checkUsername()
    },
    password () {
      this.checkPassword()
    }
  }
}
</script>

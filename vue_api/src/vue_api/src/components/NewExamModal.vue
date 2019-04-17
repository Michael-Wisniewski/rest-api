<template>
  <b-modal
    id="title-modal"
    v-model="showModal"
    @hide="closeModal"
    centered
    header-bg-variant="primary"
    header-text-variant="white"
    title="Add new examsheet"
  >
    <transition name="fade">
    <div v-if="!msg">
        <b-form-group
        label="Title :"
        class="mt-4"
        label-cols-sm="3"
        description="The minimum length is 6 characters."
        :invalid-feedback="titleValidationText"
        :state="titleValidation"
        >
        <b-form-input
            ref="title"
            v-model="title"
            :state="titleValidation"
            placeholder="Enter title"
            @keyup.enter="addExam()"
        ></b-form-input>
        </b-form-group>

        <transition name="fade">
        <div id="sending" v-if="isSending">
        <b-spinner
            :variant="variant"
        >
        </b-spinner>
        </div>
        </transition>
    </div>
    <div
      v-else
      class="container d-flex h-100"
    >
       <h4 class="align-self-center text-center w-100">
          {{ msg }}
       </h4>
    </div>
    </transition>

    <div slot="modal-footer" class="w-100 text-center">
      <b-button
        v-if="!msg"
        variant="info"
        size="xl"
        @click="addExam()"
        :disabled="isSending"
      >
        Add
      </b-button>
      <b-button
        v-else
        variant="info"
        size="xl"
        @click="closeModal()"
      >
        OK
      </b-button>
    </div>
  </b-modal>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'NewExamModal',
  data () {
    return {
      title: '',
      titleValidation: undefined,
      titleValidationText: '',
      msg: '',
      isSending: false
    }
  },
  props: {
    show: Boolean,
    refreshList: Function
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'headers'
    ]),
    showModal: {
      set () {
        return false
      },
      get () {
        return this.show
      }
    }
  },
  methods: {
    ...mapActions([
      'inspectToken'
    ]),
    checkTitle () {
      if (this.title.length >= 6) {
        this.titleValidation = true
      } else if (typeof this.titleValidation !== 'undefined') {
        this.titleValidation = false

        if (this.title.length === 0) {
          this.titleValidationText = 'Please fill out this field.'
        } else {
          this.titleValidationText = 'Title is too short'
        }
      }
    },
    addExam () {
      this.inspectToken()
      if (this.title.length >= 6 && this.isAuthenticated) {
        const headers = this.headers
        const url = 'http://localhost:80/v1/teacher/examsheet_list/'
        const data = {
          title: this.title
        }
        this.isSending = true
        axios.post(url, data, headers)
          .then((response) => {
            this.msg = response.data.message
          })
          .catch((error) => {
            if (error.response) {
              if (error.response.status === 406) {
                this.msg = error.response.data.title[0]
              } else {
                this.msg = 'Server error'
              }
            } else {
              this.msg = 'Something gone wrong'
            }
          })
        this.isSending = false
      } else {
        this.titleValidation = false
        this.checkTitle()
        this.$nextTick(function () {
          this.$refs.title.focus()
        })
      }
    },
    closeModal () {
      this.refreshList()
      this.resetData()
    },
    resetData () {
      this.title = ''
      this.titleValidation = undefined
      this.titleValidationText = ''
      this.msg = ''
      this.isSending = false
    }
  },
  watch: {
    title () {
      this.checkTitle()
    }
  }
}
</script>

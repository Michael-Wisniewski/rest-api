<template>
  <b-row id="teacher-exam"
         align-v="center"
         align-h="center"
         class="content-container">
    <b-col md="6">
      <b-spinner
      v-if="!exam && !msg"
        class="align-center"
      >
      </b-spinner>
      <div v-else>
        <transition name="bounce" mode="out-in">
        <b-card
          v-if="msg"
          border-variant="success"
          class="shadow text-center"
        >
          <b-card-text>
            <h4 class="result">
              {{ msg }}
            </h4>
            <hr class="my-4"/>
            <router-link to="/teacher/exam_list/">
              <b-button
                size="lg"
                variant="success"
              >
                OK
              </b-button>
            </router-link>
          </b-card-text>
        </b-card>
        <div
          v-if="exam"
        >
          <b-card
            id="title-card"
            header-bg-variant="primary"
            header-text-variant="white"
            class="shadow"
          >
            <span slot="header" class="badge badge-light">
            v. {{ version }}
            </span>
            <b-card-text>
              <b-form-group
                label="Title :"
                class="mt-4"
                label-cols-sm="2"
                description="The minimum length is 6 characters."
                :invalid-feedback="titleValidationText"
                :state="titleValidation"
                >
                <b-form-input
                    ref="title"
                    v-model="exam.title"
                    :state="titleValidation"
                    placeholder="Enter title"
                ></b-form-input>
                </b-form-group>
            </b-card-text>
          </b-card>
        </div>
        </transition>
      </div>
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'TeacherExam',
  data () {
    return {
      exam: null,
      msg: '',
      version: null,
      url: 'http://localhost:80/v1/teacher/exam_edit/',
      titleValidation: undefined,
      titleValidationText: ''
    }
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'headers'
    ])
  },
  methods: {
    ...mapActions([
      'inspectToken'
    ]),
    getExam () {
      this.inspectToken()
      if (this.isAuthenticated) {
        const headers = this.headers
        const url = this.url + this.$route.params.id + '/'
        const knownErrors = [404, 406, 410]

        axios.get(url, headers)
          .then((response) => {
            this.exam = response.data
            this.version = this.exam.version
            delete this.exam.version
          })
          .catch((error) => {
            if (error.response) {
              if (knownErrors.includes(error.response.status)) {
                this.msg = error.response.data.message
              } else {
                this.msg = 'Server error'
              }
            } else {
              this.msg = 'Something gone wrong'
            }
          })
      }
    },
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
    }
  },
  created () {
    this.getExam()
  },
  watch: {
    isAuthenticated () {
      this.getExam()
    },
    title () {
      this.checkTitle()
    }
  }
}
</script>

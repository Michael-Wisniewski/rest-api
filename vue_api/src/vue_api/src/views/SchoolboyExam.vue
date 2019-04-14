<template>
  <b-row id="schoolboy-exam-list"
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
            <h2 class="mt-3">
              Result
            </h2>
            <hr class="my-4"/>
            <h4 class="result">
              {{ msg }}
            </h4>
            <hr class="my-4"/>
            <router-link to="/schoolboy/exam_list/">
              <b-button
                size="lg"
                variant="success"
              >
                OK
              </b-button>
            </router-link>
          </b-card-text>
        </b-card>
        <question-box
          v-if="exam"
          :currentQuestion="exam.questions[index]"
          :percentCompleted="percentCompleted"
          :returnedAnswer="returnedAnswer"
        />
        </transition>
      </div>
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'
import QuestionBox from '../components/QuestionBox'

export default {
  name: 'SchoolboyExam',
  components: {
    QuestionBox
  },
  data () {
    return {
      exam: null,
      msg: '',
      index: 0,
      answers: [],
      url: 'http://localhost:80/v1/schoolboy/new_exam/'
    }
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'headers'
    ]),
    percentCompleted () {
      let result = (this.index / this.exam.questions.length) * 100
      return Math.round(result)
    }
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

        axios.get(url, headers)
          .then((response) => {
            this.exam = response.data
          })
          .catch((error) => {
            if (error.response) {
              if (error.response.status === 403) {
                this.msg = error.response.data.detail
              } else {
                this.msg = error.response.data.message
              }
            } else {
              this.msg = 'Something gone wrong'
            }
          })
      }
    },
    getResult () {
      this.inspectToken()
      if (this.isAuthenticated) {
        const answer = {
          id: this.exam.id,
          version: this.exam.version,
          answers: this.answers
        }
        const headers = this.headers
        const url = this.url + this.exam.id + '/'

        axios.post(url, answer, headers)
          .then((response) => {
            this.msg = response.data.message
          })
          .catch((error) => {
            if (error.response) {
              if (error.response.status === 403) {
                this.msg = error.response.data.detail
              } else {
                this.msg = error.response.data.message
              }
            } else {
              this.msg = 'Something gone wrong'
            }
          })
      }
    },
    returnedAnswer (id) {
      this.answers.push(id)
      this.index++
      if (this.index === this.exam.questions.length) {
        let self = this
        setTimeout(function () {
          self.getResult()
        }, 1500)
      }
    }
  },
  created () {
    this.getExam()
  },
  watch: {
    isAuthenticated () {
      this.getExam()
    }
  }
}
</script>

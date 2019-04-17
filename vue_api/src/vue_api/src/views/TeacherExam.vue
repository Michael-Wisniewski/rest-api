<template>
  <b-row id="teacher-exam"
         align-v="center"
         align-h="center"
         class="content-container">
    <b-col md="6" class="m-4">
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
        <b-form
          v-else-if="exam"
          @submit="saveExam"
        >
          <b-card
            id="title-card"
            header-bg-variant="primary"
            header-text-variant="white"
            class="shadow"
          >
            <div slot="header">
            Exam title
            <span class="badge badge-light version">
            v. {{ version }}
            </span>
            </div>
            <b-card-text>
              <b-form-group
                label="Title :"
                class="mt-4"
                label-cols-sm="2"
                description="The minimum length is 6 characters."
                >
                <b-form-input
                    v-model="exam.title"
                    placeholder="Enter title"
                    required
                    minlength=6
                >
                </b-form-input>
                </b-form-group>
                <b-row>
                    <b-col class="text-center">
                        <hr class="my-4"/>
                        <b-form-checkbox
                          v-model="exam.available"
                        >
                          Available
                        </b-form-checkbox>
                    </b-col>
                </b-row>
            </b-card-text>
          </b-card>
          <b-card
            v-for="(question, index) in exam.questions"
            v-if="doesDisplayQuestion(index)"
            :key="index"
            header-bg-variant="primary"
            header-text-variant="white"
            class="'shadow my-3"
          >
            <div slot="header" class="question-header">
              <span class="title">Question no. {{ index + 1 }}</span>
              <span
                v-if="minimumTwoQuestion"
                class="badge delete-question">
                <b-button @click="removeQuestion(index)" variant="danger">X</b-button>
              </span>
            </div>
            <b-card-text>
              <b-form-group
                label="Question :"
                class="mt-4"
                label-cols-sm="2"
                >
                <b-form-input
                  v-model="question.text"
                  placeholder="Enter question"
                  required
                >
                </b-form-input>
                </b-form-group>
              <hr class="my-4"/>
              <b-list-group>
                <b-list-group-item
                  v-for="(answer, ansIndex) in question.answers"
                  v-if="doesDisplayAnswer(index, ansIndex)"
                  :key="ansIndex"
                >
                  <b-row>
                    <b-col>
                        <b-form-checkbox
                          v-model="answer.is_correct"
                          :disabled="answer.is_correct"
                          @change="changeAnswer(index, ansIndex)"
                        >
                          correct
                        </b-form-checkbox>
                    </b-col>
                    <b-col cols="8">
                      <b-form-input
                        v-model="answer.text"
                        placeholder="Enter answer"
                        required
                      >
                      </b-form-input>
                    </b-col>
                    <b-col cols="2">
                      <b-button
                        v-if="minimumTwoAnswers(index)"
                        @click="removeAnswer(index, ansIndex)"
                        variant="danger">
                          X
                      </b-button>
                    </b-col>
                  </b-row>
                </b-list-group-item>
              </b-list-group>
              <b-row class="text-center">
                <b-col cols="12" class="mt-4">
                  Points :
                  <b-form-select
                    v-model="question.points"
                    :options="options"
                    class="select-points"
                  >
                  </b-form-select>
                </b-col>
                <b-col cols="12">
                  <hr class="my-4"/>
                  <b-button @click="addAnswer(index)" variant="info">Add Answer</b-button>
                </b-col>
              </b-row>
            </b-card-text>
          </b-card>
          <b-col class="text-center my-4">
            <b-button @click="deleteExam()" variant="danger">Delete Exam</b-button>
            <b-button @click="addQuestion()" variant="info">Add Question</b-button>
            <b-button type="submit" variant="success">Save</b-button>
          </b-col>
        </b-form>
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
      options: [1, 2, 3, 4, 5]
    }
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'headers'
    ]),
    minimumTwoQuestion () {
      if (this.exam.questions.length > 1) {
        return true
      } else {
        return false
      }
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
        const knownErrors = [404, 406, 410]

        axios.get(url, headers)
          .then((response) => {
            this.exam = response.data
            this.version = this.exam.version
            delete this.exam.version
            if (!this.exam.questions.length) {
              this.addQuestion()
            }
          })
          .catch((error) => {
            if (error.response) {
              if (knownErrors.includes(error.response.status)) {
                this.msg = error.response.data.message
              } else if (error.response.status === 403) {
                this.msg = error.response.data.detail
              } else {
                this.msg = 'Server error'
              }
            } else {
              this.msg = 'Something gone wrong'
            }
          })
      }
    },
    deleteExam () {
      this.inspectToken()
      if (this.isAuthenticated) {
        const headers = this.headers
        const url = this.url + this.$route.params.id + '/'
        const knownErrors = [404, 406, 410]

        axios.delete(url, headers)
          .then((response) => {
            this.msg = response.data.message
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
    saveExam (evt) {
      evt.preventDefault()
      this.inspectToken()
      if (this.isAuthenticated) {
        const headers = this.headers
        const url = this.url + this.$route.params.id + '/'
        const data = this.exam
        const knownErrors = [404, 406, 410]

        axios.post(url, data, headers)
          .then((response) => {
            this.msg = response.data.message
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
    addQuestion () {
      const question = {
        text: '',
        points: 1,
        answers: [
          {
            is_correct: true,
            text: ''
          },
          {
            is_correct: false,
            text: ''
          }
        ]
      }

      this.exam.questions.push(question)
    },
    removeQuestion (index) {
      const question = this.exam.questions[index]
      if (typeof question.id !== 'undefined') {
        question.delete = true
        this.$forceUpdate()
      } else {
        this.exam.questions.splice(index, 1)
      }
    },
    doesDisplayQuestion (index) {
      const question = this.exam.questions[index]
      if (typeof question.delete === 'undefined') {
        return true
      } else {
        return false
      }
    },
    addAnswer (index) {
      const answer = {
        is_correct: false,
        text: ''
      }
      this.exam.questions[index].answers.push(answer)
    },
    changeAnswer (index, ansIndex) {
      this.exam.questions[index].answers.forEach((answer, currentIndex) => {
        if (ansIndex !== currentIndex) {
          answer.is_correct = false
        }
      })
    },
    removeAnswer (index, ansIndex) {
      let question = this.exam.questions[index]
      let answer = question.answers[ansIndex]

      if (answer.is_correct) {
        answer.is_correct = false
        if (ansIndex === question.answers.length - 1) {
          question.answers[ansIndex - 1].is_correct = true
        } else {
          question.answers[ansIndex + 1].is_correct = true
        }
      }

      if (typeof answer.id !== 'undefined') {
        answer.delete = true
        this.$forceUpdate()
      } else {
        question.answers.splice(ansIndex, 1)
      }
    },
    minimumTwoAnswers (index) {
      let quantity = 0
      if (typeof this.exam.questions[index] !== 'undefined') {
        this.exam.questions[index].answers.forEach((answer) => {
          if (typeof answer.delete === 'undefined') {
            quantity++
          }
        })
      }
      return quantity > 2
    },
    doesDisplayAnswer (index, ansIndex) {
      const answer = this.exam.questions[index].answers[ansIndex]
      if (typeof answer.delete === 'undefined') {
        return true
      } else {
        return false
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

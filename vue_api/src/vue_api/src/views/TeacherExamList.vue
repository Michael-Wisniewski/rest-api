<template>
  <b-row id="teacher-exam-list"
         align-v="center"
         align-h="center"
         class="content-container">
    <b-col md="8">
      <b-spinner
        v-if="!exams && !errorMsg"
        class="align-center"
      >
      </b-spinner>
      <b-card
        v-else-if="errorMsg"
        class="text-center shadow"
      >
        <b-card-text>
          {{ errorMsg }}
        </b-card-text>
        <div
          v-if="firstExam"
          slot="footer"
          class="text-center"
        >
          <b-button
            @click="showNewExamModal = true"
            variant="info">
              Add first exam
          </b-button>
        </div>
      </b-card>
      <b-card
        v-else-if="exams"
        header="Exam list"
        header-bg-variant="primary"
        header-text-variant="white"
        border-variant="primary"
        class="shadow"
        footer-bg-variant="white"
      >
        <b-card-text>
          <b-table
            :items="exams"
            :fields="fields"
            striped
          >
          <template
            slot="available"
            slot-scope="data"
          >
            <h5>
              <span :class="'badge badge-' + getVariant(data.value)">
                {{ data.value }}
              </span>
            </h5>
          </template>
          <template
            slot="version"
            slot-scope="data"
          >
            <h5>
              <span class="badge badge-info">
                {{ data.value }}
              </span>
            </h5>
          </template>
          <template
            slot="filled"
            slot-scope="data"
          >
            <h5>
              <span class="badge badge-secondary">
                {{ data.value }}
              </span>
            </h5>
          </template>
          <template
            slot="passed"
            slot-scope="data"
          >
            <h5>
              <span class="badge badge-success">
                {{ data.value }}
              </span>
            </h5>
          </template>
          <template
            slot="url"
            slot-scope="data"
          >
            <router-link :to="getUrl(data.value)">
              <b-button variant="info">>></b-button>
            </router-link>
          </template>
          </b-table>
        </b-card-text>
        <div
          slot="footer"
          class="text-center"
        >
          <b-button
            @click="showNewExamModal = true"
            variant="info">
              New Exam
          </b-button>
        </div>
      </b-card>
    </b-col>
    <new-exam-modal
      :show="showNewExamModal"
      :refreshList="refreshList"
    >
    </new-exam-modal>
  </b-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'
import NewExamModal from '../components/NewExamModal'

export default {
  name: 'TeacherExamList',
  data () {
    return {
      exams: null,
      errorMsg: '',
      showNewExamModal: false,
      firstExam: false,
      fields: [
        {
          key: 'title',
          sortable: true
        },
        {
          key: 'available',
          sortable: true,
          class: 'text-center'
        },
        {
          key: 'version',
          sortable: false,
          class: 'text-center'
        },
        {
          key: 'updated',
          sortable: false
        },
        {
          key: 'filled',
          label: 'Times filled',
          sortable: false,
          class: 'text-center'
        },
        {
          key: 'passed',
          label: 'Times passed',
          sortable: false,
          class: 'text-center'
        },
        {
          key: 'url',
          label: 'Edit exam',
          sortable: false,
          class: 'text-center'
        }
      ]
    }
  },
  components: {
    NewExamModal
  },
  created () {
    this.getExams()
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
    getExams () {
      this.inspectToken()
      if (this.isAuthenticated) {
        const headers = this.headers

        axios.get('http://localhost:80/v1/teacher/examsheet_list/', headers)
          .then((response) => {
            if (response.status === 200) {
              if (response.data.message) {
                this.errorMsg = response.data.message
              } else {
                this.exams = response.data
              }
            } else if (response.status === 204) {
              this.firstExam = true
              this.errorMsg = 'You did not add any exam sheets.'
            }
          })
          .catch((error) => {
            if (error.response) {
              if (error.response.status === 403) {
                this.errorMsg = error.response.data.detail
              }
            } else {
              this.errorMsg = 'Something gone wrong.'
            }
          })
      }
    },
    getUrl (url) {
      const params = url.split('/')
      const id = params[params.length - 2]
      return '/teacher/exam/' + id + '/'
    },
    getVariant (available) {
      let badge = ''
      if (available) {
        badge = 'success'
      } else {
        badge = 'secondary'
      }
      return badge
    },
    refreshList () {
      this.showNewExamModal = false
      this.errorMsg = ''
      this.getExams()
    }
  },
  watch: {
    isAuthenticated () {
      this.getExams()
    }
  }
}
</script>

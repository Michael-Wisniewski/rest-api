<template>
  <b-row id="schoolboy-exam-list"
         align-v="center"
         align-h="center"
         class="content-container">
    <b-col md="6">
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
      </b-card>
      <b-card
        v-else-if="exams"
        header="Exam list"
        header-bg-variant="success"
        header-text-variant="white"
        border-variant="success"
        class="shadow"
      >
        <b-card-text>
          <b-table
            :items="exams"
            :fields="fields"
            striped
          >
            <template
              slot="difficulty"
              slot-scope="data"
            >
              <h5>
                <span :class="'badge badge-' + getVariant(data.value)">
                  {{ data.value }}
                </span>
              </h5>
            </template>
            <template
              slot="url"
              slot-scope="data"
            >
              <router-link :to="getUrl(data.value)">
                <b-button variant="success">>></b-button>
              </router-link>
            </template>
          </b-table>
        </b-card-text>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios'

export default {
  name: 'SchoolboyExamList',
  data () {
    return {
      exams: null,
      errorMsg: '',
      fields: [
        {
          key: 'title'
        },
        {
          key: 'author',
          sortable: true
        },
        {
          key: 'difficulty',
          sortable: true
        },
        {
          key: 'url',
          label: 'Take the exam',
          sortable: false,
          class: 'text-center'
        }
      ]
    }
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
    getExams () {
      if (this.isAuthenticated) {
        const headers = this.headers

        axios.get('http://localhost:80/v1/schoolboy/exam_list/', headers)
          .then((response) => {
            if (response.status === 200) {
              this.exams = response.data
            } else if (response.status === 202) {
              this.errorMsg = response.data.message
            }
          })
          .catch(() => {
            this.errorMsg = 'Something gone wrong.'
          })
      }
    },
    getUrl (url) {
      const params = url.split('/')
      const id = params[params.length - 2]
      return '/schoolboy/exam/' + id + '/'
    },
    getVariant (difficulty) {
      let variant = ''
      if (difficulty === 'Easy') {
        variant = 'success'
      } else if (difficulty === 'Medium') {
        variant = 'warning'
      } else {
        variant = 'danger'
      }
      return variant
    }
  },
  watch: {
    isAuthenticated () {
      this.getExams()
    }
  }
}
</script>

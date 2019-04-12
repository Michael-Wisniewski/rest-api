<template>
  <div id="question-box-container">
    <b-card
      border-variant="success"
      class="shadow text-center"
    >
      <div slot="header" class="progress">
        <div
          class="progress-bar bg-success"
          :style="'width: ' + percentCompleted + '%'"
        >
          {{ percentCompleted }}%
        </div>
      </div>
    <transition name="bounce" mode="out-in">
      <div :key="currentQuestion.text">
        <b-card-text
            v-if="percentCompleted !== 100"
        >
            <h3 class="mt-3">
            {{ currentQuestion.text }}
            </h3>
            <hr class="my-4"/>
            <b-list-group>
            <b-list-group-item
                v-for="(answer, index) in currentQuestion.answers"
                :key="index"
                @click.prevent="selectAnswer(index)"
                :class="[index === selectedIndex ? 'bg-success text-white' : '']"
            >
                {{ answer.text }}
            </b-list-group-item>
            </b-list-group>
        </b-card-text>
        <b-card-text
            v-else
            class="my-5"
        >
        <b-button size="lg" variant="success" disabled>
            <b-spinner type="grow"></b-spinner>
            Waiting for result...
            </b-button>
        </b-card-text>
      </div>
    </transition>
    </b-card>
  </div>
</template>

<script>
export default {
  name: 'QuestionBox',
  data () {
    return {
      selectedIndex: null
    }
  },
  props: {
    returnedAnswer: Function,
    currentQuestion: {
      type: Object,
      default () {
        return {
          text: '',
          answers: []
        }
      }
    },
    percentCompleted: Number
  },
  methods: {
    selectAnswer (index) {
      if (this.selectedIndex === null) {
        this.selectedIndex = index
        let self = this
        setTimeout(function () {
          self.returnedAnswer(self.currentQuestion.answers[index].id)
          self.selectedIndex = null
        }, 200)
      }
    }
  }
}
</script>

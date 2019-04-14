<template>
  <div id="landing_page">
    <b-row align-h="center" align-v="center">
      <b-col sm="4">
        <router-link to="/teacher/exam_list/">
          <b-card
            header="Teacher"
            header-tag="header"
            border-variant="primary"
            header-bg-variant="primary"
            header-text-variant="white"
            align="center"
            class="shadow"
          >
            <b-card-text>
            <img :src="require('../assets/images/teacher.jpg')" alt="Teacher panel">
            </b-card-text>
            <b-button href="#" variant="outline-primary" size="lg">Log In</b-button>
          </b-card>
        </router-link>
      </b-col>
      <b-col sm="4">
        <router-link to="/schoolboy/exam_list/">
          <b-card
            header="Schoolboy"
            header-tag="header"
            border-variant="success"
            header-bg-variant="success"
            header-text-variant="white"
            align="center"
            class="shadow"
          >
            <b-card-text>
            <img :src="require('../assets/images/schoolboy.jpg')" alt="Schoolboy panel">
            </b-card-text>
            <b-button variant="outline-success" size="lg">Log In</b-button>
          </b-card>
        </router-link>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: 'LandingPage'
}
</script>

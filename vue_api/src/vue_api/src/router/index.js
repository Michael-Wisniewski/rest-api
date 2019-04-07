import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/views/LandingPage'
import SchoolboyIndex from '@/views/SchoolboyIndex'
import SchoolboyExamList from '@/views/SchoolboyExamList'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'LandingPage',
      component: LandingPage
    },
    {
      path: '/schoolboy',
      component: SchoolboyIndex,
      children: [
        {
          path: 'exam_list/',
          name: 'SchoolboyExamList',
          component: SchoolboyExamList
        }
      ]
    }
  ]
})

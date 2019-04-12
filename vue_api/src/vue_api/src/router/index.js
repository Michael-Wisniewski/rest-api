import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/views/LandingPage'
import Base from '@/views/Base'
import SchoolboyExamList from '@/views/SchoolboyExamList'
import SchoolboyExam from '@/views/SchoolboyExam'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'LandingPage',
      component: LandingPage
    },
    {
      path: '/',
      component: Base,
      children: [
        {
          path: 'schoolboy/exam_list/',
          meta: { user: 'schoolboy' },
          component: SchoolboyExamList
        },
        {
          path: 'schoolboy/exam/:id/',
          meta: { user: 'schoolboy' },
          component: SchoolboyExam
        }
      ]
    }
  ]
})

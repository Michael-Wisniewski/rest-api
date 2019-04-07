<template>
  <div>
    w index
    <router-view/>
    <auth-modal/>
  </div>
</template>

<script>
import AuthModal from '@/components/AuthModal'

export default {
  name: 'SchoolboyIndex',
  components: {
    AuthModal
  }
}
</script>

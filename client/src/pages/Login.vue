<template lang="pug">
  section.section
    div.container
      article.message.is-warning(v-if="wasRedirected")
        div.message-body
          p You must log in to see that page.
      div(v-if="!error")
        h1.title Log in
        h2.subtitle Sign in with EVE's SSO
        a(:href="url")
          img(src="../assets/login.png")
      div(v-else)
        server-error
</template>

<script>
import Vue from 'vue'
import ServerError from '@/components/ServerError'


export default {
  components: {
    ServerError
  },
  data() {
    return {
      url: '',
      error: false
    }
  },
  computed: {
    wasRedirected() {
      return this.$store.getters.postLoginDestination !== null
    }
  },
  async created() {
    try {
      const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}eve/sso`)
      this.url = response.data.url
      this.error = false
    } catch (error) {
      this.error = true
    }
  }
}
</script>

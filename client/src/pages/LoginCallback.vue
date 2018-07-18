<template lang="pug">
  section.section
    div.container
      div.heading
        h1.title(v-if="!error && processing") Finishing login ...
        template
          div(v-if="error === 'other'")
            h1.title An error occurred with your login
              h2.subtitle
                router-link(to="{ name: 'Login' }") Please log in again
          div(v-else-if="error === 'alliance'")
            h1.title This app is for alliance-members only
            h2.subtitle If you've recently joined, it can take the EVE API a while to update. Check back later.
          div(v-if="!error && !processing")
            h1.title Login successful, redirecting you <strong>{{ name }}</strong>
</template>

<script>
import Vue from 'vue'
import decode from 'jwt-decode'


export default {
  data() {
    return {
      processing: true,
      error: null,
      name: ''
    }
  },
  async created() {
    try {
      const code = window.location.href.match(/code=([0-9a-zA-Z_-]*)/)[1]
      const response = await this.$store.getters.axios.post(`${Vue.config.SERVER_URL}eve/sso`, { code })

      const { sessionToken, localToken } = response.data
      const tokenData = decode(sessionToken)
      window.localStorage.setItem('token', localToken)
      const token = sessionToken
      this.$store.commit('LOG_IN', { token, tokenData })

      const loginRedirect = this.$store.getters.postLoginDestination
      if (loginRedirect !== null) {
        this.$router.push(loginRedirect)
        this.$store.commit('CLEAR_LOGIN_REDIRECT')
      } else {
        this.$router.push({ name: 'Landing' })
      }

      this.processing = false
      this.error = null
    } catch (err) {
      console.error(err)
      if (err.response && err.response.status === 403) {
        this.error = 'alliance'
      } else {
        this.error = 'other'
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.red
  color $red
</style>

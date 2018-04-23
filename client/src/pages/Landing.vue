<template lang="pug">
  div
    section.section.span
      div.container
        div.heading
          h1.title GETIN-Extra
        br
        p
          | This web app combines 2 features together: a wiki, where users can read, create, and edit articles, and
          | a place to read, create, and edit Pyfa-style fits.
          br
          |  To get started, click the <strong>Log in</strong> link in the top right to sign in
          |  with EVE's
          strong  SSO
          |  and then a
          strong  Index
          |  button will appear for the wiki and fits.
    section.section.footer
      div.container
        div.content.has-text-centered
          p
            strong GETIN-Extra
            |  by
            strong  Celeo
          p
            a.icon.is-link(href="https://github.com/Celeo/GETIN-Extra" target="_blank")
              b-icon(
                pack="fa"
                icon="github"
              )
</template>

<script>
export default {
  async created() {
    this.$store.commit('CLEAR_LOGIN_REDIRECT')
  }
}
</script>

<style lang="stylus" scoped>
section.span
  height 80vh
</style>

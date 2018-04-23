<template lang="pug">
  section.section
    div.container
      div(v-if="!error")
        nav.nav.has-deep-shadow
          div.nav-center
            category-tab(
              v-for="category in categories"
              v-bind:key='category'
              v-bind:data='category'
            )
        nav.nav.has-deep-shadow
          div.nav-center(
            v-for="category in categories"
            v-if="$store.getters.category === category.name"
          )
            ship-tab(
              v-for="fit in fitsInCategory"
              v-bind:name="fit.name"
              v-bind:key="fit.name"
            )
            div(v-if="fitsInCategory.length === 0")
              a.nav-item No fits in this category
        section.section
          div(v-html="markdown(fit.content)")
      div(v-else)
        server-error
</template>

<script>
import Vue from 'vue'
import marked from 'marked'
import { renderer } from '../util'
import CategoryTab from '../components/CategoryTab'
import ShipTab from '../components/ShipTab'
import ServerError from '../components/ServerError'


export default {
  components: {
    CategoryTab,
    ShipTab,
    ServerError
  },
  data() {
    return {
      categories: [],
      fits: [],
      error: false
    }
  },
  computed: {
    fit() {
      for (let fit of this.fits) {
        if (fit.category === this.$store.getters.category && fit.name === this.$store.getters.ship) {
          return fit
        }
      }
      return { content: '' }
    },
    fitsInCategory() {
      let ret = []
      for (let fit of this.fits) {
        if (fit.category === this.$store.getters.category) {
          ret.push(fit)
        }
      }
      return ret
    }
  },
  methods: {
    markdown(s) {
      return marked(s, { sanitize: true, renderer })
    },
    async loadData() {
      try {
        const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}fits`)
        this.categories = response.data.categories
        this.fits = response.data.fits
        this.error = false
      } catch (error) {
        this.error = true
        console.error(error)
      }
    }
  },
  async created() {
    await this.loadData()
  }
}
</script>

<template lang="pug">
  section.section
    div.container
      div.columns(v-if="$store.getters.editor")
        div.column.is-11
        div.column
          router-link.button.is-info(@click="newPageModalActive = true" :to="{ name: 'FitsEditor' }")
            span Editor
            b-icon(
              icon="arrow-right"
            )
      div(v-if="!error")
        div(v-if="categories.length > 0")
          div.columns
            div.column(
              v-for="category in categories"
              :key="category.id"
            )
              p.category.is-link(:class="{ 'is-selected': selectedCategory === category.id }" @click="setCategory(category.id)") {{ category.name }}
          div.columns(v-show="fitsInCategory.length > 0")
            div.column(
              v-for="fit in fitsInCategory"
              :key="fit.id"
            )
              p.fit.is-link(:class="{ 'is-selected': selectedFit === fit.id }" @click="setFit(fit.id)") {{ fit.name }}
          p(v-show="fitsInCategory.length === 0") No fits in this category
          p(v-html="fitData")
        div(v-else)
          p No fits have been created.
      div(v-else)
        server-error
</template>

<script>
import Vue from 'vue'
import marked from 'marked'
import { renderer } from '@/util'
import CategoryTab from '@/components/CategoryTab'
import ShipTab from '@/components/ShipTab'
import ServerError from '@/components/ServerError'


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
      selectedCategory: 0,
      selectedFit: 0,
      error: false
    }
  },
  computed: {
    fitsInCategory() {
      let ret = []
      for (let fit of this.fits) {
        if (fit.category_id === this.selectedCategory) {
          ret.push(fit)
        }
      }
      return ret
    },
    fitData() {
      if (this.selectedFit > 0) {
        let selected = null
        for (let fit of this.fits) {
          if (fit.id === this.selectedFit) {
            selected = fit
            break
          }
        }
        if (!selected) {
          return ''
        }
        return marked(selected.content, { sanitize: true, renderer })
      } else {
        return ''
      }
    }
  },
  methods: {
    markdown(s) {
      return marked(s, { sanitize: true, renderer })
    },
    async loadData() {
      try {
        const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}fits/fits`)
        this.categories = response.data.categories
        this.fits = response.data.fits
        this.selectedFit = 0
        this.selectedCategory = 0
        if (this.categories.length > 0) {
          this.selectedCategory = this.categories[0].id
        }
        this.error = false
      } catch (error) {
        this.error = true
        console.error(error)
      }
    },
    setCategory(id) {
      this.selectedCategory = id
      this.selectedFit = 0
    },
    setFit(id) {
      this.selectedFit = id
    }
  },
  async created() {
    await this.loadData()
  }
}
</script>

<style lang="stylus" scoped>
.category
  background-color white
  border 1px solid #dbdbdb
  color black
  border-radius 10px
  font-weight 600
  font-size 1.25rem
  position relative
  text-align center
  padding 1rem 0

.fit
  background-color white
  border 1px solid #dbdbdb
  color black
  border-radius 10px
  font-weight 600
  font-size 0.75rem
  position relative
  text-align center
  padding 0.75rem 0

.is-selected
  background-color hsl(204, 86%, 53%)
  color white
  border none
</style>

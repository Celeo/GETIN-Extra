<template lang="pug">
  section.section
    div.container(v-if="error")
      server-error
    div.container(v-if="error === false")
      nav.level
        div.level-left(v-if="fits !== null")
          div.level-item(v-if="!refreshing")
            b-field(label="Select a fit")
              b-select(placeholder="select" v-model="selectedId")
                b-option(
                  v-for="fit in fits"
                  v-bind:value="fit.id"
                  v-bind:key="fit.id"
                ) {{ fit.name }}
          div.level-item(v-if="!refreshing")
            b-field(label="Category")
              b-select(placeholder="select" v-model="categoryId" v-bind:disabled="selectedId === 0")
                b-option(
                  v-for="category in categories"
                  v-bind:value="category.id"
                  v-bind:key="category.id"
                ) {{ category.name }}
          div.level-item(v-if="!refreshing")
            b-field(label="Order")
              b-input(v-model="order" type="number" v-bind:disabled="selectedId === 0")
        div.level-right
          div.level-item
            div.block
              button.button.is-success(v-if="selectedId" @click="save")
                b-icon(icon="floppy-o")
                span Save changes
              button.button.is-danger(v-if="selectedId" @click="deleteFit")
                b-icon(icon="trash-o")
                span Delete fit
              button.button.is-info(@click="createNew")
                b-icon(icon="plus")
                span Create new fit
      div.columns(v-if="selectedId !== 0")
        div#panel-input.column.is-half
          p.control
            textarea#entry.textarea(v-model="fitContent")
        div.column.is-half
          div#panel-output(v-html="fitRendered")
</template>

<script>
import Vue from 'vue'
import marked from 'marked'
import { renderer } from '../util'
import ServerError from '../components/ServerError'


export default {
  components: {
    ServerError
  },
  data() {
    return {
      error: null,
      fits: null,
      categories: null,
      selectedId: 0,
      categoryId: 0,
      order: 0,
      fitContent: '',
      refreshing: false
    }
  },
  computed: {
    fitRendered() {
      return marked(this.fitContent, { sanitize: true, renderer })
    },
    selectedFit() {
      return this.fits.filter(e => e.id === this.selectedId)[0]
    },
    selectedCategory() {
      return this.categories.filter(e => e.id === this.categoryId)[0]
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}fits`)
        this.fits = response.data.fits
        this.categories = response.data.categories
        this.error = false
      } catch (error) {
        console.error(error)
        this.error = true
      }
    },
    async save() {
      try {
        const data = {
          content: this.fitContent,
          category_id: this.selectedCategory.id,
          order: this.order
        }
        await this.$store.getters.axios.put(`${Vue.config.SERVER_URL}fits/${this.selectedFit.id}`, data)
        await this.loadData()
        this.$toast.open({
          message: 'Fit saved',
          type: 'is-success'
        })
      } catch (error) {
        console.error(error)
        this.$dialog.alert({
          message: 'There was an error saving the data',
          type: 'is-danger',
          hasIcon: true
        })
      }
    },
    async deleteFit() {
      this.$dialog.confirm({
        title: 'Delete fit',
        message: 'Are you sure that you want to <strong>delete</strong> this fit? This cannot be undone.',
        confirmText: 'Delete',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: async () => {
          try {
            await this.$store.getters.axios.delete(`${Vue.config.SERVER_URL}fits/${this.selectedId}`)
            await this.loadData()
            this.selectedId = 0
            this.categoryId = 0
            this.order = 0
            this.refreshing = true
            Vue.nextTick(() => {
              this.refreshing = false
            })
            this.$toast.open({
              message: 'Fit deleted',
              type: 'is-success'
            })
          } catch (error) {
            this.$dialog.alert({
              message: 'There was an error deleting that fit',
              type: 'is-danger',
              hasIcon: true
            })
          }
        }
      })
    },
    async createNew() {
      this.$dialog.prompt({
        message: 'New fit creation',
        maxlength: 30,
        placeholder: 'name',
        onConfirm: async (value) => {
          try {
            await this.$store.getters.axios.post(`${Vue.config.SERVER_URL}fits`, { name: value })
            await this.loadData()
            this.$toast.open({
              message: 'New fit added',
              type: 'is-success'
            })
          } catch (error) {
            this.$dialog.alert({
              message: 'There was an error saving the new fit',
              type: 'is-danger',
              hasIcon: true
            })
          }
        }
      })
    }
  },
  async created() {
    await this.loadData()
  },
  watch: {
    selectedId(newId) {
      if (this.selectedFit) {
        this.fitContent = this.selectedFit.content
        this.categoryId = this.selectedFit.category_id
        this.order = this.selectedFit.order
      } else {
        this.fitContent = ''
        this.categoryId = -1
        this.order = ''
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
#panel-input
  border-right 1px solid rgba(0, 0, 0, .3)

#panel-output
  height 65vh
  overflow-y scroll

#entry
  height 70vh !important
</style>

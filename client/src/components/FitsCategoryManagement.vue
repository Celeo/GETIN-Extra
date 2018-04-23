<template lang="pug">
  section.section
    div.container
      h1.title Fits category management
      nav.level
        div.level-left(v-if="categories !== null")
          div.level-item(v-if="!refreshing")
            b-field(label="Select a category")
              b-select(placeholder="category" v-model="selectedId")
                option(
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
              button.button.is-danger(v-if="selectedId" @click="deleteCategory")
                b-icon(icon="trash-o")
                span Delete category
              button.button.is-info(@click="createNew")
                b-icon(icon="plus")
                span Create new category
</template>

<script>
import Vue from 'vue'


export default {
  data() {
    return {
      categories: [],
      selectedId: 0,
      order: 0,
      refreshing: false
    }
  },
  computed: {
    selected() {
      return this.categories.filter(e => e.id === this.selectedId)[0]
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}fits/categories`)
        this.categories = response.data
        this.error = false
      } catch (error) {
        console.error(error)
        this.error = true
      }
    },
    async save() {
      try {
        const data = {
          order: this.order
        }
        await this.$store.getters.axios.put(`${Vue.config.SERVER_URL}fits/categories/${this.selectedId}`, data)
        await this.loadData()
        this.$toast.open({
          message: 'Category saved',
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
    async deleteCategory() {
      if (this.selected.has_linked_fits) {
        this.$dialog.alert({
          message: 'You cannot delete this category has it has fits linked to it.',
          type: 'is-warning',
          hasIcon: true
        })
      } else {
        this.$dialog.confirm({
          title: 'Delete category',
          message: 'Are you sure that you want to <strong>delete</strong> this category? This cannot be undone.',
          confirmText: 'Delete',
          type: 'is-danger',
          hasIcon: true,
          onConfirm: async () => {
            try {
              await this.$store.getters.axios.delete(`${Vue.config.SERVER_URL}fits/categories/${this.selectedId}`)
              await this.loadData()
              this.selectedId = 0
              this.categoryId = 0
              this.order = 0
              this.refreshing = true
              Vue.nextTick(() => {
                this.refreshing = false
              })
              this.$toast.open({
                message: 'Category deleted',
                type: 'is-success'
              })
            } catch (error) {
              this.$dialog.alert({
                message: 'There was an error deleting that category',
                type: 'is-danger',
                hasIcon: true
              })
            }
          }
        })
      }
    },
    async createNew() {
      this.$dialog.prompt({
        message: 'New category creation',
        maxlength: 30,
        placeholder: 'name',
        onConfirm: async (value) => {
          try {
            await this.$store.getters.axios.post(`${Vue.config.SERVER_URL}fits/categories`, { name: value })
            await this.loadData()
            this.$toast.open({
              message: 'New category added',
              type: 'is-success'
            })
          } catch (error) {
            this.$dialog.alert({
              message: 'There was an error saving the new category',
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
      if (this.selected) {
        this.order = this.selected.order
      } else {
        this.order = ''
      }
    }
  }
}
</script>

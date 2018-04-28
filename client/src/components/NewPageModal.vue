<template lang="pug">
div.modal-card
  header.modal-card-head
    p.modal-card-title New page
  section.modal-card-body
    b-field(label="Page name")
      b-input(
        v-model="name"
        placeholder="name"
        required
      )
    b-field(label="Category")
      b-select(placeholder="category" v-model="categoryId")
        option(
          v-for="category in categories"
          v-bind:value="category.id"
          v-bind:key="category.id"
        ) {{ category.name }}
  footer.modal-card-foot
      button.button(@click.prevent="closeModal") Close
      button.button.is-success(@click="save" v-bind:disabled="name === '' || categoryId === 0") Create
</template>

<script>
import Vue from 'vue'


export default {
  data() {
    return {
      name: '',
      categoryId: 0,
      categories: []
    }
  },
  async created() {
    try {
      const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}wiki/category`)
      this.categories = response.data
    } catch (error) {
      console.error(error)
      this.$dialog.alert({
        message: 'There was an error creating the new page',
        type: 'is-danger',
        hasIcon: true
      })
      this.$emit('close')
      document.body.classList.toggle('is-noscroll', false)
    }
  },
  methods: {
    closeModal() {
      // https://github.com/buefy/buefy/issues/549
      this.$emit('close')
      document.body.classList.toggle('is-noscroll', false)
    },
    async save() {
      try {
        const data = {
          name: this.name,
          category_id: this.categoryId
        }
        const response = await this.$store.getters.axios.post(`${Vue.config.SERVER_URL}wiki/page`, data)
        this.$emit('close')
        document.body.classList.toggle('is-noscroll', false)
        Vue.nextTick(() => {
          this.$router.push({
            name: 'WikiViewPage',
            params: {
              category: response.data.category,
              page: response.data.page
            }
          })
        })
        this.$emit('close')
        document.body.classList.toggle('is-noscroll', false)
      } catch (error) {
        console.error(error)
        this.$dialog.alert({
          message: 'There was an error creating the new page',
          type: 'is-danger',
          hasIcon: true
        })
        this.$emit('close')
      }
    }
  }
}
</script>

<style scoped>
.modal-card {
    margin: 0 auto;
    width: auto;
}
</style>

<template lang="pug">
  a.navbar-item.is-tab.big(
      v-bind:class="{ 'is-active': $store.getters.category === data.name }"
      @click="setCategory"
    ) {{ data.name }}
</template>

<script>
export default {
  props: ['data'],
  methods: {
    setCategory() {
      this.$store.commit('SET_CATEGORY', this.data.name)
    }
  }
}
</script>

<style lang="stylus" scoped>
.big
  font-size 30px
  padding-left 100px
  padding-right 100px
</style>

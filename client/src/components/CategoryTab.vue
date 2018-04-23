<template lang="pug">
  a.nav-item.is-tab.big(
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

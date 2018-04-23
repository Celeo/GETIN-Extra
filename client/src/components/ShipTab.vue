<template lang="pug">
  a.nav-item.is-tab(
      v-bind:class="{ 'is-active': $store.getters.ship === name }"
      @click="setShip"
    ) {{ name }}
</template>

<script>
export default {
  props: ['name'],
  methods: {
    setShip() {
      this.$store.commit('SET_SHIP', this.name)
    }
  }
}
</script>

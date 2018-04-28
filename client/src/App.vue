<template lang="pug">
  div
    nav.navbar.has-shadow.is-spaced
      div.container
        div.navbar-brand
          router-link#brand.navbar-item(:to="'/'") GETIN-Extras
        div.navbar-end
          router-link.navbar-item.is-tab(
            :to="{ name: 'Landing' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'Landing' }"
          ) Home
          router-link.navbar-item.is-tab(
            :to="{ name: 'Login' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'Login' }"
            v-if="!loggedIn"
          ) Log in
          router-link.navbar-item.is-tab(
            :to="{ name: 'WikiIndex' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'WikiIndex' }"
            v-if="loggedIn"
          ) Wiki Index
          router-link.navbar-item.is-tab(
            :to="{ name: 'FitsFits' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'FitsFits' }"
            v-if="loggedIn"
          ) Fits Index
          router-link.navbar-item.is-tab(
            :to="{ name: 'Admin' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'Admin' }"
            v-if="$store.getters.admin"
          ) Admin
          router-link.navbar-item.is-tab(
            :to="{ name: 'Logout' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'Logout' }"
            v-if="loggedIn"
          ) Log out
    transition(name="fade" mode="out-in")
      router-view
</template>

<script>
export default {
  computed: {
    loggedIn() {
      return this.$store.getters.isLoggedIn
    },
    member() {
      return this.$store.getters.inAlliance
    }
  }
}
</script>

<style lang="scss">
@import "~bulma/sass/utilities/_all";

$primary: $blue;
$primary-invert: findColorInvert($primary);

$colors: (
    "white": ($white, $black),
    "black": ($black, $white),
    "light": ($light, $light-invert),
    "dark": ($dark, $dark-invert),
    "primary": ($primary, $primary-invert),
    "info": ($info, $info-invert),
    "success": ($success, $success-invert),
    "warning": ($warning, $warning-invert),
    "danger": ($danger, $danger-invert)
);

$link: $primary;
$link-invert: $primary-invert;
$link-focus-border: $primary;

@import "~bulma";
@import "~buefy/src/scss/buefy";

.button {
  margin-left: 5px;
}

#brand {
  font-weight: 600;
  font-size: 24px;
}

label.label {
  font-weight: 600 !important;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .2s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

.is-link {
  cursor: pointer;
}

.title-cat {
  font-size: 16px;
  font-weight: 400 !important;
}
</style>

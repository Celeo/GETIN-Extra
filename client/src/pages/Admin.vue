<template lang="pug">
  div
    role-management
    wiki-category-management
    deleted-pages-list
    fits-category-management
</template>

<script>
import RoleManagement from '@/components/RoleManagement'
import WikiCategoryManagement from '@/components/WikiCategoryManagement'
import FitsCategoryManagement from '@/components/FitsCategoryManagement'
import DeletedPagesList from '@/components/DeletedPagesList'


export default {
  components: {
    RoleManagement,
    WikiCategoryManagement,
    FitsCategoryManagement,
    DeletedPagesList
  }
}
</script>

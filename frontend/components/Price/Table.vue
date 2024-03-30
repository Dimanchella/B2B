<template>
  <v-data-table
      v-model:items-per-page="perPage"
      :headers="headers"
      :items="products"
      item-value="title"
      class="elevation-1 fill-height"
      hide-default-footer
      density="compact"
  >
    <template v-slot:item.actions="{ item }">
      <OrderCartSwitch :product="item"/>
    </template>

    <template v-slot:bottom>
    </template>

  </v-data-table>
</template>

<script setup>
import {usePriceStore} from "~/stores/price"
const priceStore = usePriceStore()
const { products, groups, perPage } = storeToRefs(priceStore)

const headers = [
  {
    title: 'Наименование',
    sortable: false,
    key: 'title',
    align: 'start'
  },
  {
    title: 'Характеристика',
    sortable: false,
    key: 'title_characteristic',
    align: 'start'
  },
  {
    title: 'Цена',
    sortable: false,
    key: 'price',
    align: 'end'
  },
  {
    title: 'Корзина',
    sortable: false,
    key: 'actions',
  },
]

</script>

<style scoped>

</style>

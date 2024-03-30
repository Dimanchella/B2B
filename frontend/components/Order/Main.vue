<script setup>
import {useOrderStore} from "~/stores/orders.js"
import {storeToRefs} from "pinia";

const orderStore = useOrderStore()
const {orders} = storeToRefs(orderStore)
</script>

<template>
  <div
      v-for="order in orders"
      :key="order.id"
  >
    {{ order.id }} - {{ order.title }}
  </div>
</template>

<style scoped>

</style>
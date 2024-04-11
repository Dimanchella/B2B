<-- Корзина -->

<script setup>
const props = defineProps({
  product: {
    type: Object,
    default: {}
  }
})

import {useCartStore} from "~/stores/cart.js";
const cartStore = useCartStore()
const {addToCart, changeFromCart, deleteFromCart, productCount} = cartStore

const numProducts = ref(0)

import {useMessageStore} from "~/stores/message";
const messageStore = useMessageStore();
const {error, message} = storeToRefs(messageStore);
const {clearMessage, setMessage, setError} = messageStore;

</script>

<template>
  <v-icon
      class="mr-2"
      @click="deleteFromCart(product)"
  >
    mdi-minus
  </v-icon>
    <input
        class="product-count"
        type="text"
        v-bind:value="productCount(product)"
        v-on:change="changeFromCart(product, $event.target.value)"
    />
  <v-icon
      class="ml-2"
      @click="addToCart(product)"
  >
    mdi-plus
  </v-icon>
</template>

<style scoped>
.product-count {
    text-align:center;
    border:1px solid white;
    padding:5px;
    width:40%;
}
</style>

<script setup>
import {useCartStore} from "~/stores/cart.js";

const cartStore = useCartStore()
const {cartCount} = cartStore
</script>

<template>
  <div :style="{'cursor':'pointer'}">
    <v-badge @click="navigateTo('/cart')" :content="cartCount()">
      <v-icon class="cart-icon">mdi-cart</v-icon>
    </v-badge>
  </div>
</template>

<style scoped>
.cart-icon {
  font-size: 24px;
}
</style>

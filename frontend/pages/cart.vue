<script setup>
import {Swiper, SwiperSlide} from "swiper/vue";
import {EffectCube, Pagination} from "swiper/modules";

import "swiper/css/effect-cube";
import "swiper/css/pagination";
import "swiper/css";

import {useCartStore} from "~/stores/cart.js";
import {useOrderStore} from "~/stores/orders"

const modules = [EffectCube, Pagination]

const cartStore = useCartStore()
const {cart, cartCount, uniProductsCount, deleteProductFromCart, cartSum, clearCart, emptyCart} = cartStore

const orderStore = useOrderStore()
const {createNewOrder} = orderStore

const performOrder = async () => {
  const id = await createNewOrder(cart)
  if (id) {
    clearCart()
    navigateTo('/order/' + id + '?cart=true')
  }
}
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="10">
        <h2>Всего {{ uniProductsCount() }} позиций товаров в количестве {{ cartCount() }} ед., на сумму {{ cartSum() }}
          руб.</h2>
      </v-col>
      <v-col cols="12" sm="2">
        <v-btn
            v-if="!emptyCart()"
            @click="performOrder()"
        >Оформить
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card
            class="mb-3"
            v-for="item in cart"
            :key="item.id"
        >
          <v-row align="center" class="ma-1">
            <v-col cols="12" sm="3">
              <swiper
                  v-if="item.images"
                  :modules="modules"
                  effect="cube"
                  :grab-cursor="true"
                  :loop="true"
                  :pagination="true"
              >
                <swiper-slide
                    v-for="(obj, idx) in item.images"
                    :key="idx"
                >
                  <img :src="getImgUrl(obj.image)" alt=""/>
                </swiper-slide>
              </swiper>
              <v-img
                  v-else
                  src="/nophoto.png"
                  class="cart-img"
              />
            </v-col>
            <v-col cols="12" sm="6">
              <h3>{{ item.title }}</h3>
              <h4>{{ item.title_characteristic }}</h4>
              <p>{{ item.price }} руб</p>
            </v-col>
            <v-col cols="2">
              <OrderCartSwitch :product="item"/>
            </v-col>
            <v-col cols="1">
              <v-icon
                  size="small"
                  @click="deleteProductFromCart(item)"
              >
                mdi-close
              </v-icon>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style>
.cart-img {
  min-width: 150px;
  height: 150px;
}

.swiper {
  width: 150px;
  height: 150px;
  overflow: visible;
}

.swiper-slide img {
  width: 100%;
  height: 100%;
}

.swiper-pagination-bullet {
  width: 10px;
  height: 10px;
  background-color: white;
  opacity: 0.8;
}

.swiper-pagination-bullet-active {
  background-color: darkolivegreen;
}
</style>

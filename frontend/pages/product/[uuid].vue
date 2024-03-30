<template>
  <v-container>
    <v-card>
      <v-row style="height: 80dvh">
        <v-col cols="6" align-self="center">
          <div>
            <swiper
                v-if="product.images.length"
                :modules="modules"
                effect="cube"
                :grab-cursor="true"
                :loop="true"
                :pagination="true"
            >
              <swiper-slide
                  v-for="(objimg, idx) in product.images"
                  :key="idx"
              >
                <img :src="getImgUrl(objimg.image)"/>
              </swiper-slide>
            </swiper>
            <v-img
                v-else
                src="/nophoto.png"
                class="cart-img"
            />
          </div>
        </v-col>
        <!-- <v-col cols="6" class="pt-5 pl-2">
          <h4>{{ product.title }}</h4>
          <h4>{{ product.characteristic }}</h4><br>
          <p v-html="product.description "></p><br>
          <p>Цена: {{ product.price }}</p><br>
          <OrderCartSwitch :product="product" />
        </v-col> -->
      </v-row>
    </v-card>
  </v-container>
</template>

<script setup>
import {usePriceStore} from "~/stores/price"

import {Swiper, SwiperSlide} from 'swiper/vue';
import {EffectCube, Pagination} from 'swiper/modules';

import 'swiper/css/effect-cube';
import 'swiper/css/pagination';
import 'swiper/css';

const modules = [EffectCube, Pagination]

const priceStore = usePriceStore()
const {getPriceDetail} = priceStore

const route = useRoute()
const id = route.params.uuid

const router = useRouter()

const product = await getPriceDetail(id)

// useSeoMeta({
//   title: `${product.title} - ИП Иванов - Продажа вентиляторов`,
//   ogTitle: `${product.title} - ИП Иванов - Продажа вентиляторов`,
//   description: product.description,
//   ogDescription: product.description,
//   ogImage: 'https://mysite.ru/image.png',
//   twitterCard: 'summary_large_image',
// })

// let url = ''
// if (product.images.length > 0) {
//   url = getImgUrl(product.images[0].image)
// }

// useSchemaOrg([
//   defineProduct({
//     name: product.title,
//     description: product.description,
//     image: [
//       url
//     ],
//     offers: [
//       { price: product.price },
//     ],
//   })
// ])

// const closeProduct = () => {
//   product.value = {}
//   router.back()
// }

</script>

<style scoped>
.swiper {
  width: 250px;
  height: 250px;
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
  background-color: #0d47a1;
}

.cart-img {
  min-width: 150px;
  height: 150px;
}
</style>

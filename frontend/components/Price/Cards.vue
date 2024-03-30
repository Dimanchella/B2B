<template>
  <v-row>
    <v-col
        v-for="product in products"
        :key="product.id"
        cols="12"
        sm="6"
        md="4"
        xl="2"
    >
      <v-card>
        <v-img
            :src="getProductImg(product)"
            class="cart-img"
            max-height="200"
            cover
            rel="preload"
        />
        <v-card-text>
          <div style="height: 100px">
            <h4>{{ product.title }}</h4>
            <p>{{ product.title_characteristic }}</p>
          </div>
          <div>
            {{ product.price }} руб.
          </div>
          <div class="d-flex justify-center align-center mt-2">
            <OrderCartSwitch :product="product" />
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="editProductLocal(product)">
            Подробнее
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>

const emit = defineEmits(['editProduct'])
const props = defineProps({
  products: {
    type: Array,
    required: true,
    default: []
  }
})

const getProductImg = (product) => {
  if (product.images.length === 0) {
    return '/nophoto.png'
  } else {
    return getImgUrl(product.images[0].image)
  }
}

const editProductLocal = (product) => {
  emit('editProduct', product)
}

</script>

<style scoped>
.cart-img {
 border: 1px solid white;
 background:black; 
 padding:10px;
}
</style>

<script setup>
import {usePriceStore} from "~/stores/price";
import {storeToRefs} from "pinia";

import {useTheme} from "vuetify"
const theme = useTheme()

const priceStore = usePriceStore()

const {
  products,
  groups,
  numPages,
  search,
  price_min,
  price_max,
  page,
  group,
} = storeToRefs(priceStore)
const {getPriceList, getGroupTree, resetPagination} = priceStore
const selectedGroupTitle = ref('')

await getPriceList()
await getGroupTree()

const pageChange = async () => {
  await getPriceList()
}

const searchItemPrice = async () => {
  resetPagination()
  await getPriceList()
}

const selectedGroupClick = async (selectedGroup) => {
  //alert('price.groupClick: '+ selectedGroup.title);
  selectedGroupTitle.value = selectedGroup.title
  group.value = selectedGroup.id
  resetPagination()
  await getPriceList()
}

const groupClick = async (selectedGroup) => {
  //alert('price.groupClick: '+ selectedGroup.title);
  selectedGroupTitle.value = selectedGroup.title;
  resetPagination();
  let obs = [selectedGroup];
  let is_root = 1;
  while (obs.length > 0) {
    const ob = obs.shift();
    if (ob.children.length > 0) {
      obs.push(... ob.children);
    }
    group.value = ob.id;
    await getPriceList(is_root);
    is_root = 0;
  }
}

const changeSelectedGroupTitle = async () => {
    selectedGroupTitle.value = '...';
}

const resetGroup = async () => {
  selectedGroupTitle.value = ''
  group.value = null
  resetPagination()
  await getPriceList()
}

const editProduct = (product) => {
  navigateTo({
    path: '/product/' + product.id,
  })
}

const priceSwitch = ref(true)
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6">
        <PriceSearchItem
            label="Поиск"
            v-model="search"
            @searchItem="searchItemPrice"
        />
      </v-col>
      <v-col cols="12" sm="2">
        <PriceSearchItem
            label="Цена минимум"
            v-model="price_min"
            @searchItem="searchItemPrice"
        />
      </v-col>
      <v-col cols="12" sm="2">
        <PriceSearchItem
            label="Цена максимум"
            v-model="price_max"
            @searchItem="searchItemPrice"
        />
      </v-col>
      <v-col cols="12" sm="2">
        <v-switch
            v-model="priceSwitch"
            label="Вид"
            inset
        ></v-switch>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="8">
        <div class="text-center pb-2">
          <v-pagination
              v-model="page"
              :length="numPages"
              :total-visible="5"
              @update:model-value="pageChange"
          ></v-pagination>
        </div>

        <PriceCards
            v-if="priceSwitch"
            :products="products"
            @editProduct="editProduct"
        />
        <PriceTable v-else/>

        <div class="text-center pt-2">
          <v-pagination
              v-model="page"
              :length="numPages"
              :total-visible="5"
              @update:model-value="pageChange"
          ></v-pagination>
        </div>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card
            density="compact"
            class="fill-height"
        >
          <template v-slot:text>
            <h3>Категории товаров</h3>
            <v-banner
                :text="selectedGroupTitle"
                density="compact"
            />
            <PriceTreeGroup
                v-for="group in groups"
                :key="group.id"
                :group="group"
                :group-title="group.title"
                :group-children="group.children"
                @groupClick="groupClick"
            />
          </template>
          <template v-slot:actions>
            <v-btn @click="resetGroup">
              Сброс
            </v-btn>
          </template>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>

</style>

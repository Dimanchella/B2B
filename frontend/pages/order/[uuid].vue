<template>
  <v-container>
    <v-row>
      <v-col>
        <v-btn class="mr-2" @click="closeOrder()">
          Закрыть
        </v-btn>
        <v-btn
            :disabled="disabled()"
            color="success"
            class="mr-2"
            @click="saveCurrentOrder()"
        >
          Записать
        </v-btn>
        <v-btn
            :disabled="disabled()"
            color="warning"
            class="mr-2"
            @click="updateCurrentOrder()">
          Оформить
        </v-btn>
        <v-chip :color="getStatusColor(order.site_status)">
          {{ formatStatus(order.site_status) }}
        </v-chip>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
            v-model="order.number"
            label="Номер"
            disabled
        ></v-text-field>
      </v-col>
      <v-col>
        <v-text-field
            v-model="orderDate"
            label="Дата"
            disabled
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-select
            v-model="order.organization"
            :items="organization"
            item-title="name"
            item-value="id"
            label="Организация"
            required
            single-line
            :disabled="disabled()"
        ></v-select>
        <v-select
            v-model="order.counterparty"
            :items="counterparty"
            item-title="name"
            item-value="id"
            label="Контрагент"
            required
            single-line
            :disabled="disabled()"
        ></v-select>
      </v-col>
      <v-col>
        <v-select
            v-model="order.agreement"
            :items="agreement"
            item-title="name"
            item-value="id"
            label="Соглашение"
            required
            single-line
            :disabled="disabled()"
        ></v-select>
        <v-select
            v-model="order.contract"
            :items="contract"
            item-title="name"
            item-value="id"
            label="Договор"
            required
            single-line
            :disabled="disabled()"
        ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-row class="pa-2">
          <v-col>Наименование</v-col>
          <v-col>Характеристика</v-col>
          <v-col cols="2">Количество</v-col>
          <v-col>Цена</v-col>
          <v-col>Сумма</v-col>
        </v-row>
        <v-card
            v-for="(item, idx) in order.order_orders_detail"
            :key="idx"
            class="pa-2 mb-1"
            :disabled="disabled()"
        >
          <v-row align="center">
            <v-col>
              {{ item.product_full_name }}
            </v-col>
            <v-col>
              {{ item.characteristic_name }}
            </v-col>
            <v-col cols="2">
              <v-icon
                  size="small"
                  class="me-2"
                  @click="dec(item)"
              >
                mdi-minus
              </v-icon>
                <input
                    class="product-count"
                    type="text"
                    v-bind:value="productCount(item.quantity)"
                    v-on:change="changeProductCount(item, $event.target.value)"
                    :disabled="disabled()"
                />
              <v-icon
                  size="small"
                  class="me-2"
                  @click="inc(item)"
              >
                mdi-plus
              </v-icon>
            </v-col>
            <v-col>
              {{ item.price }}
            </v-col>
            <v-col>
              {{ item.total }}
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-divider class="border-opacity-50 mb-6 mt-6"/>
    <v-row>
      <v-col>
        <p>Позиций: {{ uniProductsCount(order) }}</p>
      </v-col>
      <v-col>
        <p>Количество: {{ orderCount(order) }}</p>
      </v-col>
      <v-spacer/>
      <v-col>
        <p>Сумма: {{ orderSum(order) }}</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import {useOrderStore} from "~/stores/orders"
import {useCatalogsStore} from "~/stores/catalogs"

const route = useRoute()
const uuid = route.params.uuid

const router = useRouter()

const orderStore = useOrderStore()

const catalogsStore = useCatalogsStore()

const {getOrder, updateOrder, orderCount, orderSum, uniProductsCount} = orderStore

const {organization, counterparty, agreement, contract} = storeToRefs(catalogsStore)
const {getOrganization, getCounterparty, getAgreement, getContract} = catalogsStore

await getOrganization()
await getCounterparty()
await getAgreement()
await getContract()

const order = await getOrder(uuid)

const orderDate = computed({
  get() {
    return new Date(order.value.date_time).toLocaleString()
  },
  set(value) {
  }
})

const closeOrder = () => {
  order.value = {}
  if (route.query.cart) {
    router.push('/')
  } else {
    router.back()
  }
}

const saveCurrentOrder = async () => {
  // Сохранить изменения в заказе
  await updateOrder(order, false)
}

const updateCurrentOrder = async () => {
  // Оформить заказ
  await updateOrder(order, true)
  closeOrder()
}

const dec = (product) => {
  const products = order.value.order_orders_detail
  const index = products.findIndex(item => item.pk === product.pk)

  if (index < 0) return

  if (products[index].quantity > 0) {
    products[index].quantity--
    products[index].total = products[index].quantity * products[index].price
  }
}

const inc = (product) => {
  console.log(product)
  const products = order.value.order_orders_detail

  const index = products.findIndex(item => item.pk === product.pk)
  if (index >= 0) {
    products[index].quantity++
    products[index].total = products[index].quantity * products[index].price
  }
}

const changeProductCount = (product, value) => {
    console.log('changeProductCount: ', product, order)
    if (isNaN(value)) {
        const message = "ERROR!\nOrder product count value should be a number only\nPlease, repeat";
        alert(message);
        return false;
    }
    const count = Number(value);
    const products = order.value.order_orders_detail
    const index = products.findIndex(item => item.pk === product.pk)
    if (products[index] !== undefined) {
        products[index].quantity = count;
        products[index].total = products[index].quantity * products[index].price
    }
    //console.log('changeProductCount:', products[index], value);
}

const productCount = (value) => {
    return Math.floor(value)
}

const disabled = () => {
  if (order.value.site_status === 'PR' || order.value.site_status === 'CL') {
    return true
  } else {
    return false
  }
}

</script>

<style scoped>
.product-count {
    text-align:center;
    border:1px solid white;
    padding:5px;
    width:40%;
}
</style>

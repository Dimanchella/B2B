<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-data-table
            v-model:items-per-page="perPage"
            :headers="headers"
            :items="orders"
            class="elevation-1 fill-height"
        >
          <template v-slot:item.date_time="{item}">
            {{ formatDateRu(item.date_time, now) }}
          </template>

          <template v-slot:item.site_status="{item}">
            <v-chip :color="getStatusColor(item.site_status)">
              {{ formatStatus(item.site_status) }}
            </v-chip>
          </template>

          <template v-slot:item.actions="{item}">
            <v-icon
                v-if="canEdit(item.site_status)"
                size="small"
                class="me-2"
                @click="editItem(item)"
            >
              mdi-pencil
            </v-icon>
            <v-icon
                v-if="canDelete(item.site_status)"
                size="small"
                class="me-2"
                @click="deleteOrder(item)"
            >
              mdi-delete
            </v-icon>
            <v-icon
                v-if="canView(item.site_status)"
                size="small"
                class="me-2"
                @click="editItem(item)"
            >
              mdi-file-document-check-outline
            </v-icon>
          </template>

          <template v-slot:bottom>
            <div class="text-center pt-2">
              <v-pagination
                  v-model="page"
                  :length="numPages"
                  :total-visible="5"
                  @update:model-value="pageChange"
              />
            </div>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
definePageMeta({ middleware: 'auth' })

import {storeToRefs} from "pinia";
import {useOrderStore} from "~/stores/orders.js";

const orderStore = useOrderStore()

const {orders, page, perPage, numPages} = storeToRefs(orderStore)
const {getOrderList, deleteOrder} = orderStore

const headers = [
  {
    title: "Номер",
    sortable: false,
    key: "number",
    align: "start"
  },
  {
    title: "Дата",
    sortable: false,
    key: "date_time",
    align: "start"
  },
  {
    title: "Статус",
    sortable: false,
    key: "site_status",
    align: "start"
  },
  {
    title: "Партнер",
    sortable: false,
    key: "partner_full_name",
    align: "start"
  },
  {
    title: "Контрагент",
    sortable: false,
    key: "contractor_name",
    align: "start"
  },
  {
    title: "Организация",
    sortable: false,
    key: "organization_name",
    align: "start"
  },
  {
    title: "Действия",
    sortable: false,
    key: "actions"
  }
]

await getOrderList()

const now = new Date().toLocaleString("ru", {
  year: "numeric",
  month: "numeric",
  day: "numeric"
})

const editItem = (item) => {
  navigateTo('/order/' + item.id)
}

const pageChange = async () => {
  await getOrderList()
}
</script>

<style scoped>

</style>

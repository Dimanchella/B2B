<template>
    <div v-if="message">
      <v-snackbar
          :timeout="5000"
          :value="true"
          :color="snackbarColor()"
          @input="clearMessage()"
      >
        {{ message }}
        <template v-slot:activator="{ props }">
          <v-btn
              color="deep-purple-accent-4"
              v-bind="props"
              @click="clearMessage()"
          >
            Закрыть
          </v-btn>
        </template>
      </v-snackbar>
    </div>
</template>

<script setup>
import {useMessageStore} from "~/stores/message"
const messageStore = useMessageStore()

const {error, message} = storeToRefs(messageStore)
const {clearMessage} = messageStore

const snackbarColor = () => {
  return error ? 'red' : 'green'
}
</script>

<style scoped>

</style>

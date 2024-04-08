<script setup>
const emit = defineEmits(["searchItem", "update:modelValue"])
const props = defineProps({
  modelValue: {
    required: true
  },
  label: {
    type: String,
    default: ''
  }
})

const searchValue = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emit("update:modelValue", value)
  }
})

const searchItemIn = () => {
  emit("searchItem")
}
</script>

<template>
  <v-text-field
      :label="label"
      variant="underlined"
      density="compact"
      clearable
      v-model="searchValue"
      append-inner-icon="mdi-magnify"
      @click:append-inner="searchItemIn"
      @click:clear="searchItemIn"
      @keyup.prevent.enter="searchItemIn"
  />
</template>

<style scoped>

</style>
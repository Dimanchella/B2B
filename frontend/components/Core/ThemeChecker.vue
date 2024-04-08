<script setup>
import {useTheme} from "vuetify"

const theme = useTheme()
const darkMode = useCookie("darkMode")

const darkTheme = () => {
  return !!theme.global.current.value.dark
}

const toggleTheme = () => {
  let currentTheme = (darkTheme() ? "light" : "dark")
  theme.global.name.value = currentTheme
  darkMode.value = currentTheme
}
</script>

<template>
  <v-icon
    class="ml-2"
    @click="toggleTheme"
    icon="mdi-theme-light-dark"
  />
</template>

<style scoped>

</style>
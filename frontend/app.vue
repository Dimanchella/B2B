<template>
  <NuxtLayout>
    <NuxtPage/>
  </NuxtLayout>
</template>

<script setup>
import {useTheme} from "vuetify"

const theme = useTheme()
const darkMode = useCookie("darkMode")

if (darkMode.value !== undefined) {
  theme.global.name.value = darkMode.value
}
theme.global.IsDebug = 1; // XXX flag to project debug option
</script>

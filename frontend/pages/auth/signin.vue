<template>
  <v-container>
    <v-row
        justify="center"
        align-content="center"
        style="height: 100vh"
    >
      <v-col
          cols="12"
          lg="6" md="6" sm="6" xl="6"
      >
        <h2>Введите логин и пароль</h2>
        <form @submit.prevent="submit">
          <v-text-field
              v-model="username.value.value"
              :counter="10"
              :error-messages="username.errorMessage.value"
              label="ИНН"
          />

          <v-text-field
              v-model="password.value.value"
              :error-messages="password.errorMessage.value"
              label="Пароль"
              type="password"
          />

          <v-btn class="me-4" type="submit">
            Войти
          </v-btn>

          <v-btn @click="handleReset">
            Очистить
          </v-btn>

          <CoreThemeChecker class="ml-10"/>
        </form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
definePageMeta({
  layout: "custom",
  auth: {
    unauthenticatedOnly: true,
    navigateAuthenticatedTo: "/"
  }
})

import {useField, useForm} from "vee-validate";

const userValidationSchema = {
  username(value) {
    return /^[A-Z0-9-]{4,32}$/i.test(value)
    // if (value?.length === 10) return true
    // return 'ИНН должен состоять из 10 символов'
  },
  password(value) {
    return /^\S{6,}$/.test(value)
    // if (value?.value > 7 && /[0-9-]+/.test(value)) return true
    // return 'Пароль должен быть больше 7 символов'
  }
}

const {handleSubmit, handleReset} = useForm({
  validationSchema: userValidationSchema
})

const username = useField('username')
const password = useField('password')

const {signIn} = useAuth()

const submit = handleSubmit(values => {
  console.log('>>> Войти:', values)
  signIn('credentials', {
    username: values.username,
    password: values.password,
    callbackUrl: '/'
  })
}
/*
login() {
  this.$auth.loginWith('cookie', {
    data: {
    username: values.username,
    password: values.password,
    }
  })
    .then(() => this.$toast.success('Добро пожаловать'))
    .catch((e) => this.$toast.error(e.response.data.detail));
}
*/
)

</script>

<style scoped>

</style>

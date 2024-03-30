<template>
  <v-app-bar>
    <v-container class="fill-height">
      <v-app-bar-nav-icon
          class="hidden-md-and-up"
          variant="text"
          @click.stop="drawer = !drawer"
      />
      <v-avatar
          class="ms-4 me-10 hidden-sm-and-down"
          size="32"
          image="/favicon.ico"
      />
      <v-btn
          class="hidden-sm-and-down"
          v-for="link in links"
          :key="link.title"
          :to="link.to"
      >
        {{ link.title }}
      </v-btn>

      <v-spacer/>

      <div name="username" class="username">{{ data.user.username }}</div>

      <OrderCartIcon class="mr-2"/>

      <CoreThemeChecker class="mr-2"/>

      <v-divider class=" hidden-sm-and-down border-opacity-50 ml-6 mr-6" vertical/>
      <v-btn
          class="hidden-sm-and-down"
          v-if="status === 'authenticated'"
          key="logout"
          @click="signOut()"
      >
        Выйти
      </v-btn>
      <v-btn
          class="hidden-sm-and-down"
          v-if="status !== 'authenticated'"
          key="login"
          @click="signIn()"
      >
        Войти
      </v-btn>
    </v-container>
  </v-app-bar>

  <v-navigation-drawer
      v-model="drawer"
      temporary
      color="#385f73"
  >
    <v-list nav>
      <v-list-item
          v-for="link in links"
          :key="link.title"
          :to="link.to"
          :title="link.title"
      />
    </v-list>

    <template v-slot:append>
      <v-btn
          class="ma-2"
          v-if="status === 'authenticated'"
          key="logout"
          @click="signOut()"
      >
        Выйти
      </v-btn>
      <v-btn
          class="ma-2"
          v-if="status !== 'authenticated'"
          key="login"
          @click="signIn()"
      >
        Войти
      </v-btn>
    </template>
  </v-navigation-drawer>
</template>

<script setup>

import {ref} from "vue"

const drawer = ref(null)

const links = [
  {title: "Заказы", to: "/"},
  {title: "Прайс", to: "/price"},
]

//import {useField} from "vee-validate";
//const username = '...';

const {status, signOut} = useAuth()
const {data, token} = useAuthState()

</script>

<style scoped>

.username {
    padding:10px 20px;
}

</style>

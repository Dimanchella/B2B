// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, {transformAssetUrls} from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  devtools: {enabled: true},
  build: {
    transpile: ['vuetify'],
  },
  modules: [
    '@sidebase/nuxt-auth',
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({autoImport: true}))
      })
    },
    '@pinia/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
    'nuxt-schema-org',
  ],
  auth: {
    baseURL: process.env.AUTH_ORIGIN,
    provider: {
      type: 'authjs'
    },
    globalAppMiddleware: true,
  },
  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
  runtimeConfig: {
    authSecret: process.env.AUTH_SECRET,
    authOrigin: process.env.AUTH_ORIGIN,
    public: {
      djangoUrl: process.env.DJANGO_URL,
      imgUrl: process.env.IMG_URL,
    }
  },
  devServer: {
    host: '0.0.0.0',
    port: 3000,
  },
})

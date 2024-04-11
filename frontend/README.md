# Nuxt 3 Minimal Starter

Look at the [Nuxt 3 documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

Make sure to install the dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm run dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm run build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm run preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

------------

mkaro@mkaro-work:/storage/www/web/1c/frontend$ npx nuxi@latest module add sidebase-auth
Need to install the following packages:
nuxi@3.11.1
Ok to proceed? (y) y
ℹ Installing @sidebase/nuxt-auth@latest development dependency                                             4:00:12 PM

changed 1 package, and audited 941 packages in 8s

191 packages are looking for funding
  run `npm fund` for details

3 vulnerabilities (1 low, 2 moderate)

To address issues that do not require attention, run:
  npm audit fix

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
ℹ Updating nuxt.config.ts                                                                                  4:00:20 PM

 ERROR  Casting "BlockStatement" is not supported                                                           4:00:20 PM

  9 |   modules: [
 10 |     '@sidebase/nuxt-auth',
 11 |     (_options, nuxt) => {
                              ^
 12 |       nuxt.hooks.hook('vite:extendConfig', (config) => {
 13 |         // @ts-expect-error
 14 |         config.plugins.push(vuetify({autoImport: true}))


  
  9 |   modules: [
  10 |     '@sidebase/nuxt-auth',
  11 |     (_options, nuxt) => {
  ^
  12 |       nuxt.hooks.hook('vite:extendConfig', (config) => {
  13 |         // @ts-expect-error
  14 |         config.plugins.push(vuetify({autoImport: true}))
  
  at proxify (/home/mkaro/.npm/_npx/b95349761371180e/node_modules/nuxi/dist/chunks/add2.mjs:25905:13)
  at proxifyArrowFunctionExpression (/home/mkaro/.npm/_npx/b95349761371180e/node_modules/nuxi/dist/chunks/add2.mjs:25717:14)
  at proxify (/home/mkaro/.npm/_npx/b95349761371180e/node_modules/nuxi/dist/chunks/add2.mjs:25888:15)
  at /home/mkaro/.npm/_npx/b95349761371180e/node_modules/nuxi/dist/chunks/add2.mjs:25615:36
  at Array.map (<anonymous>)
  at Proxy.includes (/home/mkaro/.npm/_npx/b95349761371180e/node_modules/nuxi/dist/chunks/add2.mjs:25615:25)
  at /home/mkaro/.npm/_npx/b95349761371180e/node_modules/nuxi/dist/chunks/add2.mjs:26220:28
  at updateNuxtConfig (/home/mkaro/.npm/_npx/b95349761371180e/node_modules/nuxi/dist/chunks/add2.mjs:26250:5)
  at async Object.setup (/home/mkaro/.npm/_npx/b95349761371180e/node_modules/nuxi/dist/chunks/add2.mjs:26216:7)
  at async runCommand$1 (/home/mkaro/.npm/_npx/b95349761371180e/node_modules/nuxi/dist/shared/nuxi.9edf0930.mjs:1620:5)


 ERROR  Please manually add @sidebase/nuxt-auth to the modules in nuxt.config.ts                            4:00:20 PM




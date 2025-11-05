import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://v2ark.com',
  base: '/',
  output: 'static',
  build: {
    assets: '_astro'
  },
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp'
    }
  },
  vite: {
    build: {
      rollupOptions: {
        output: {
          assetFileNames: 'assets/[name].[hash][extname]'
        }
      }
    }
  }
});
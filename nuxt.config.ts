export default defineNuxtConfig({
  extends: ['docus'],

  devtools: {
    enabled: true,
  },

  app: {
    baseURL: '/',
    buildAssetsDir: '/_nuxt/',
    head: {
      link: [{ rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    },
  },

  site: {
    name: 'kostyl.dev',
  },

  nitro: {
    preset: 'github-pages',
    prerender: {
      routes: [],
    },
  },

  css: [
    '~/assets/css/content-images.css',
    '~/assets/css/code-line-numbers.css',
    '~/assets/css/content-width.css',
    '~/assets/css/zen-mode.css',
  ],

  content: {
    markdown: {
      tags: {
        'code-block': 'CodeBlock',
        callout: 'Callout',
        mermaid: 'Mermaid',
      },
    },
    build: {
      markdown: {
        highlight: {
          theme: {
            default: 'dark-plus',
            dark: 'dark-plus',
            light: 'light-plus',
          },
          langs: [
            // .NET Languages
            'csharp',
            'fsharp',
            'vb',
            // Web Languages
            'typescript',
            'javascript',
            'jsx',
            'tsx',
            'html',
            'css',
            'vue',
            'php',
            // Shell/Script Languages
            'bash',
            'shell',
            'powershell',
            'docker',
            'dockerfile',
            // Data/Config Languages
            'json',
            'jsonc',
            'yaml',
            'xml',
            'toml',
            'ini',
            // Other Programming Languages
            'cpp',
            'c',
            'java',
            'python',
            'rust',
            'go',
            'asm',
            // Markup/Documentation
            'markdown',
            'http',
            // Database
            'sql',
            // Utility
            'diff',
          ],
        },
      },
    },
  },

  compatibilityDate: '2025-01-26',

  icon: {
    serverBundle: 'auto',
    fetchTimeout: 5000,
  },

  vite: {
    server: {
      allowedHosts: ['865fb62d150c.ngrok-free.app'],
    },
    build: {
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules')) {
              if (id.includes('mermaid')) return 'vendor-mermaid'
              if (id.includes('docus') || id.includes('nuxt')) return 'vendor-nuxt'
              if (id.includes('shiki') || id.includes('highlight')) return 'vendor-code'
              return 'vendor'
            }
          },
        },
      },
    },
  },
})

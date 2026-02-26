import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#E50914',
        'primary-dark': '#B20710',
        dark: '#141414',
        'dark-secondary': '#221f1f',
      },
    },
  },
  plugins: [],
}
export default config

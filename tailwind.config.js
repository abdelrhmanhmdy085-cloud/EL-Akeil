/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#fdf2f2',
          100: '#fbe4e4',
          200: '#f7cdcd',
          300: '#f1abab',
          400: '#e77d7d',
          500: '#d95353',
          600: '#c43a3a',
          700: '#a52e2e',
          800: '#892929',
          900: '#722727',
          950: '#3e1111',
        },
      },
    },
  },
  plugins: [],
}

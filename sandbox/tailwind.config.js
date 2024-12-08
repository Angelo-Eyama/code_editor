/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      boxShadow: {
        /** offset-x | offset-y | blur-radius | spread-radius | color */
        'dark': '0 10px 77px 5px rgba(34, 159, 225, 0.7)',
      }
    },
  },
  plugins: [],
}


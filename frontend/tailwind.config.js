/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit', // Włącza Just-In-Time Compilation
  purge: ['./src/**/*.{html,ts}'], // Ścieżki do plików Angulara
  darkMode: false,
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
};

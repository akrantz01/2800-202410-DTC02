import forms from '@tailwindcss/forms';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./frontend/**/*.{html,js}'],
  theme: {
    extend: {
      fontFamily: {
        roboto: ['Roboto', 'sans-serif'],
      },
      colors: {
        primary: '#17da7c',
        secondary: '#00aef4',
        accent: '#00cbf4',
      },
    },
  },
  plugins: [forms],
};

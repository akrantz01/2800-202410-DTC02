import forms from '@tailwindcss/forms';
import flowbite from 'flowbite/plugin';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./frontend/**/*.{html,js}', './node_modules/flowbite/**/*.js'],
  theme: {
    extend: {
      fontFamily: {
        roboto: ['Roboto', 'sans-serif'],
        opensans: ['Open Sans', 'sans-serif'],
      },
      colors: {
        primary: '#17da7c',
        primary_highlight: '#15CB73',
        secondary: '#00aef4',
        accent: '#00cbf4',
      },
      fontSize: {
        xxs: '0.5rem',
      },
    },
  },
  plugins: [forms, flowbite],
};

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./frontend/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        roboto: ["Roboto", "sans-serif"],
      },
      colors: {
        primary: "#17da7c",
        secondary: "#00aef4",
        accent: "#00cbf4",
      },
    },
  },
  plugins: [],
};

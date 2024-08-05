/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "**/fastwindx/templates/**/*.html",
    "**/fastwindx/static/js/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
}


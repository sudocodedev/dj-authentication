/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/**/*.html',
    './templates/*.html',
    './static/js/*.js',
  ],
  theme: {
    extend: {
      fontSize: {
        'xs': '0.8rem',
        '2xs': '0.5rem',
      },
    },
  },
  plugins: [
    require('daisyui'),
    require('@tailwindcss/forms'),
  ],
  daisyui: {
    themes: ["emerald", "dim"],
  },
}


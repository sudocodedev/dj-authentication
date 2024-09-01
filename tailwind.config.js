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
      fontFamily: {
        'jost': ['Jost', 'sans-serif'],
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
  safelist: [
    'toast',
    'toast-top',
    'toast-end',
    'alert',
    'alert-info',
    'alert-success',
    'alert-warning',
    'alert-error',
    'text-xl',
  ],
}


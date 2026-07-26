/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "class",
  theme: {
    extend: {
      fontSize: {
        "display": ["2rem", { lineHeight: "1.2", fontWeight: "700" }],
      },
    },
  },
  plugins: [],
};

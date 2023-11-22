const Path = require("path");

const pySitePackages = Path.join(__dirname, '../venv/Lib/site-packages');
let pyPackagesPaths = [];

if (pySitePackages) {
  pyPackagesPaths = [
      Path.join(pySitePackages, "./crispy_tailwind/**/*.html"),
      Path.join(pySitePackages, "./crispy_tailwind/**/*.py"),
      Path.join(pySitePackages, "./crispy_tailwind/**/*.js")
  ];
}
// We can add current project paths here
const projectPaths = [
  Path.join(__dirname, "../templates/**/*.html"),
  // add js file paths if you need
];

const contentPaths = [...projectPaths, ...pyPackagesPaths];

module.exports = {
  content: contentPaths,
  theme: {
    extend: {},
  },
  plugins: [
      require("@tailwindcss/forms")
  ],
};
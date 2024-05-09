import globals from 'globals';
import js from '@eslint/js';
import prettier from 'eslint-plugin-prettier/recommended';

export default [
  prettier,
  {
    ignores: ['node_modules/'],
    languageOptions: { globals: { ...globals.browser, ...globals.node } },
  },
  {
    files: ['**/*.js'],
    rules: js.configs.recommended.rules,
  },
];

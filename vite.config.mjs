import fs from 'node:fs/promises';
import { resolve } from 'node:path';

import { defineConfig } from 'vite';

export default defineConfig(async () => {
  const root = resolve(import.meta.dirname, 'frontend');
  const files = await fs.readdir(root);
  const pages = files.filter((file) => file.endsWith('.html'));

  return {
    root: 'frontend',
    build: {
      target: 'es2022',
      rollupOptions: {
        input: Object.fromEntries(
          pages.map((file) => [file.replace(/\.html$/, ''), resolve(root, file)]),
        ),
      },
    },
  };
});

import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./assets/js/setupTests.js'],
    include: ['assets/js/**/*.test.{js,jsx}'],
    clearMocks: true,
    restoreMocks: true,
  },
});
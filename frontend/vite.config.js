// frontend/vite.config.js

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Add this section to solve the "Invalid hook call" error
  resolve: {
    dedupe: ['react', 'react-dom'],
  },
})
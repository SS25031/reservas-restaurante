import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		// En dev el navegador habla con :5173; Vite reenvía al backend para que
		// las cookies HTTPOnly de sesión funcionen en el mismo origen.
		proxy: {
			'/api': 'http://localhost:8000',
			'/health': 'http://localhost:8000'
		}
	}
});

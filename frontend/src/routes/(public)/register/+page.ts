import { redirect } from '@sveltejs/kit';
import { registroDisponible } from '$lib/api/auth';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const { disponible } = await registroDisponible(fetch);
	if (!disponible) {
		redirect(303, '/login');
	}
};

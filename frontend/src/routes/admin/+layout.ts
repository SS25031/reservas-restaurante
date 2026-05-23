import { redirect } from '@sveltejs/kit';
import { ApiError } from '$lib/api/client';
import { getMe } from '$lib/api/auth';
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ fetch }) => {
	try {
		const admin = await getMe(fetch);
		return { admin };
	} catch (e) {
		if (e instanceof ApiError && e.status === 401) {
			redirect(303, '/login');
		}
		throw e;
	}
};

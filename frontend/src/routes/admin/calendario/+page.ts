import { listReservas } from '$lib/api/admin';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const reservas = await listReservas(fetch);
	return { reservas };
};

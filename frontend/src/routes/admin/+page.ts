import { listReservas } from '$lib/api/admin';
import { getOnboardingEstado } from '$lib/api/onboarding';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const [reservas, onboarding] = await Promise.all([
		listReservas(fetch),
		getOnboardingEstado(fetch)
	]);
	return {
		reservasCount: reservas.length,
		onboarding
	};
};

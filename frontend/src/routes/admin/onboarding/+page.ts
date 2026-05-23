import {
	completarOnboarding,
	getCalendario,
	getMesas,
	getOnboardingEstado,
	getRestaurant,
	getTurnos
} from '$lib/api/onboarding';
import { normalizeMesas } from '$lib/onboarding/mesas';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const [estado, restaurant, mesas, turnos, calendario] = await Promise.all([
		getOnboardingEstado(fetch),
		getRestaurant(fetch),
		getMesas(fetch),
		getTurnos(fetch),
		getCalendario(fetch)
	]);

	return {
		estado,
		restaurant,
		mesas: normalizeMesas(mesas),
		turnos,
		calendario
	};
};

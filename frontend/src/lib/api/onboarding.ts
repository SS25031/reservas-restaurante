import { apiFetch } from './client';
import type {
	CalendarDayConfig,
	CompletarOnboardingResponse,
	MesaConfig,
	OnboardingEstado,
	RestaurantConfig,
	TurnoConfig
} from './types';

export function getOnboardingEstado(fetchFn: typeof fetch) {
	return apiFetch<OnboardingEstado>(fetchFn, '/api/v1/onboarding/estado');
}

export function getRestaurant(fetchFn: typeof fetch) {
	return apiFetch<RestaurantConfig>(fetchFn, '/api/v1/onboarding/restaurant');
}

export function updateRestaurant(
	fetchFn: typeof fetch,
	data: Partial<Pick<RestaurantConfig, 'nombre' | 'max_reservas_por_dia' | 'capacidad_maxima_grupo'>>
) {
	return apiFetch<RestaurantConfig>(fetchFn, '/api/v1/onboarding/restaurant', {
		method: 'PUT',
		body: JSON.stringify(data)
	});
}

export function getMesas(fetchFn: typeof fetch) {
	return apiFetch<MesaConfig[]>(fetchFn, '/api/v1/onboarding/mesas');
}

export function saveMesas(fetchFn: typeof fetch, mesas: MesaConfig[]) {
	return apiFetch<MesaConfig[]>(fetchFn, '/api/v1/onboarding/mesas', {
		method: 'PUT',
		body: JSON.stringify({ mesas })
	});
}

export function getTurnos(fetchFn: typeof fetch) {
	return apiFetch<TurnoConfig[]>(fetchFn, '/api/v1/onboarding/turnos');
}

export function saveTurnos(fetchFn: typeof fetch, turnos: TurnoConfig[]) {
	return apiFetch<TurnoConfig[]>(fetchFn, '/api/v1/onboarding/turnos', {
		method: 'PUT',
		body: JSON.stringify({ turnos })
	});
}

export function getCalendario(fetchFn: typeof fetch, desde?: string, hasta?: string) {
	const params = new URLSearchParams();
	if (desde) params.set('desde', desde);
	if (hasta) params.set('hasta', hasta);
	const query = params.toString();
	const path = query ? `/api/v1/onboarding/calendario?${query}` : '/api/v1/onboarding/calendario';
	return apiFetch<CalendarDayConfig[]>(fetchFn, path);
}

export function saveCalendario(fetchFn: typeof fetch, dias: CalendarDayConfig[]) {
	return apiFetch<CalendarDayConfig[]>(fetchFn, '/api/v1/onboarding/calendario', {
		method: 'PUT',
		body: JSON.stringify({ dias })
	});
}

export function completarOnboarding(fetchFn: typeof fetch) {
	return apiFetch<CompletarOnboardingResponse>(fetchFn, '/api/v1/onboarding/completar', {
		method: 'POST'
	});
}

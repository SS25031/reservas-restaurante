import { apiFetch } from './client';
import type { ReabrirOnboardingResponse, Reserva, ReservaCreate, ReservaUpdate } from './types';

export function listReservas(fetchFn: typeof fetch) {
	return apiFetch<Reserva[]>(fetchFn, '/api/v1/admin/reservas');
}

export function getReserva(fetchFn: typeof fetch, id: number) {
	return apiFetch<Reserva>(fetchFn, `/api/v1/admin/reservas/${id}`);
}

export function createReserva(fetchFn: typeof fetch, data: ReservaCreate) {
	return apiFetch<Reserva>(fetchFn, '/api/v1/admin/reservas', {
		method: 'POST',
		body: JSON.stringify(data)
	});
}

export function updateReserva(fetchFn: typeof fetch, id: number, data: ReservaUpdate) {
	return apiFetch<Reserva>(fetchFn, `/api/v1/admin/reservas/${id}`, {
		method: 'PATCH',
		body: JSON.stringify(data)
	});
}

export function cancelReserva(fetchFn: typeof fetch, id: number) {
	return apiFetch<void>(fetchFn, `/api/v1/admin/reservas/${id}/cancelar`, {
		method: 'POST'
	});
}

export function reabrirOnboarding(fetchFn: typeof fetch) {
	return apiFetch<ReabrirOnboardingResponse>(fetchFn, '/api/v1/admin/onboarding/reabrir', {
		method: 'POST'
	});
}

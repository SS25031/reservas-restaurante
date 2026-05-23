import { apiFetch } from './client';
import type { Disponibilidad, PublicRestaurant, Reserva, ReservaCreate } from './types';

export function getPublicRestaurant(fetchFn: typeof fetch) {
	return apiFetch<PublicRestaurant>(fetchFn, '/api/v1/public/restaurant');
}

export function getDisponibilidad(fetchFn: typeof fetch, fecha: string, personas: number) {
	const params = new URLSearchParams({ fecha, personas: String(personas) });
	return apiFetch<Disponibilidad>(fetchFn, `/api/v1/public/disponibilidad?${params}`);
}

export function createPublicReserva(fetchFn: typeof fetch, data: ReservaCreate) {
	return apiFetch<Reserva>(fetchFn, '/api/v1/public/reservas', {
		method: 'POST',
		body: JSON.stringify(data)
	});
}

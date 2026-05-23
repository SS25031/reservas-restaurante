import { apiFetch } from './client';
import type { AdminUser, RegistroDisponible } from './types';

export interface AuthCredentials {
	email: string;
	password: string;
}

export function registroDisponible(fetchFn: typeof fetch) {
	return apiFetch<RegistroDisponible>(fetchFn, '/api/v1/auth/registro-disponible');
}

export function getMe(fetchFn: typeof fetch) {
	return apiFetch<AdminUser>(fetchFn, '/api/v1/auth/me');
}

export function login(fetchFn: typeof fetch, credentials: AuthCredentials) {
	return apiFetch<AdminUser>(fetchFn, '/api/v1/auth/login', {
		method: 'POST',
		body: JSON.stringify(credentials)
	});
}

export function register(fetchFn: typeof fetch, credentials: AuthCredentials) {
	return apiFetch<AdminUser>(fetchFn, '/api/v1/auth/register', {
		method: 'POST',
		body: JSON.stringify(credentials)
	});
}

export function logout(fetchFn: typeof fetch) {
	return apiFetch<void>(fetchFn, '/api/v1/auth/logout', { method: 'POST' });
}

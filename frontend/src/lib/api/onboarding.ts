import { apiFetch } from './client';
import type { OnboardingEstado } from './types';

export function getOnboardingEstado(fetchFn: typeof fetch) {
	return apiFetch<OnboardingEstado>(fetchFn, '/api/v1/onboarding/estado');
}

/** Cliente HTTP hacia el backend (rutas relativas; proxy Vite en dev). */

export class ApiError extends Error {
	status: number;

	constructor(status: number, message: string) {
		super(message);
		this.name = 'ApiError';
		this.status = status;
	}
}

async function parseErrorMessage(res: Response): Promise<string> {
	try {
		const body = (await res.json()) as { detail?: string };
		if (typeof body.detail === 'string') return body.detail;
	} catch {
		// respuesta no JSON
	}
	return res.statusText || 'Error desconocido';
}

export async function apiFetch<T>(
	fetchFn: typeof fetch,
	path: string,
	options: RequestInit = {}
): Promise<T> {
	const headers = new Headers(options.headers);
	if (options.body && !headers.has('Content-Type')) {
		headers.set('Content-Type', 'application/json');
	}

	const res = await fetchFn(path, {
		credentials: 'include',
		...options,
		headers
	});

	if (!res.ok) {
		throw new ApiError(res.status, await parseErrorMessage(res));
	}

	if (res.status === 204) {
		return undefined as T;
	}

	return (await res.json()) as T;
}

export async function checkHealth(fetchFn: typeof fetch): Promise<boolean> {
	try {
		const res = await fetchFn('/health', { credentials: 'include' });
		if (!res.ok) return false;
		const body = (await res.json()) as { status?: string };
		return body.status === 'ok';
	} catch {
		return false;
	}
}

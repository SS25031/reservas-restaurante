<script lang="ts">
	import { goto } from '$app/navigation';
	import { ApiError } from '$lib/api/client';
	import { register } from '$lib/api/auth';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function onSubmit(event: SubmitEvent) {
		event.preventDefault();
		error = '';
		loading = true;
		try {
			await register(fetch, { email, password });
			await goto('/admin/onboarding');
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudo registrar';
		} finally {
			loading = false;
		}
	}
</script>

<h1>Registrar administrador</h1>
<p class="muted">
	Solo disponible mientras no exista un admin. Tras registrarte podrás configurar el
	restaurante (onboarding).
</p>

<form class="form card" style="margin-top: 1rem" onsubmit={onSubmit}>
	<label>
		Email
		<input type="email" bind:value={email} required autocomplete="email" />
	</label>
	<label>
		Contraseña (mín. 8 caracteres)
		<input type="password" bind:value={password} required minlength="8" autocomplete="new-password" />
	</label>
	{#if error}
		<p class="error">{error}</p>
	{/if}
	<button type="submit" disabled={loading}>{loading ? 'Registrando…' : 'Crear cuenta'}</button>
</form>

<p class="muted" style="margin-top: 1rem">
	¿Ya tienes cuenta?
	<a href="/login">Iniciar sesión</a>
</p>

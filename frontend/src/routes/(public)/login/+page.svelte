<script lang="ts">
	import { goto } from '$app/navigation';
	import { ApiError } from '$lib/api/client';
	import { login } from '$lib/api/auth';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function onSubmit(event: SubmitEvent) {
		event.preventDefault();
		error = '';
		loading = true;
		try {
			await login(fetch, { email, password });
			await goto('/admin');
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudo iniciar sesión';
		} finally {
			loading = false;
		}
	}
</script>

<h1>Iniciar sesión</h1>
<p class="muted">Acceso para administradores del restaurante.</p>

<form class="form card" style="margin-top: 1rem" onsubmit={onSubmit}>
	<label>
		Email
		<input type="email" bind:value={email} required autocomplete="email" />
	</label>
	<label>
		Contraseña
		<input type="password" bind:value={password} required minlength="8" autocomplete="current-password" />
	</label>
	{#if error}
		<p class="error">{error}</p>
	{/if}
	<button type="submit" disabled={loading}>{loading ? 'Entrando…' : 'Entrar'}</button>
</form>

<p class="muted" style="margin-top: 1rem">
	¿Primera vez?
	<a href="/register">Registrar administrador</a>
</p>

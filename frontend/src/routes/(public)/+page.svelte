<script lang="ts">
	import { onMount } from 'svelte';
	import { checkHealth } from '$lib/api/client';

	let backendOk = $state<boolean | null>(null);

	onMount(async () => {
		backendOk = await checkHealth(fetch);
	});
</script>

<h1>Reservas de restaurante</h1>
<p class="muted">
	Área pública para clientes (próximamente). Los administradores configuran el restaurante
	desde el panel privado.
</p>

<section class="card" style="margin-top: 1.5rem">
	<h2 style="margin-top: 0">Estado del backend</h2>
	{#if backendOk === null}
		<p class="muted">Comprobando…</p>
	{:else if backendOk}
		<p class="status-ok">Backend conectado (/health OK)</p>
	{:else}
		<p class="status-fail">
			No se pudo conectar al backend. ¿Está corriendo en <code>localhost:8000</code>?
		</p>
	{/if}
</section>

<p style="margin-top: 1.5rem">
	<a href="/login">Entrar como administrador</a>
	·
	<a href="/register">Registrar primer admin</a>
</p>

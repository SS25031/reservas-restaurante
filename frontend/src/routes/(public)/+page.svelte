<script lang="ts">
	import { onMount } from 'svelte';
	import { checkHealth } from '$lib/api/client';
	import { getPublicRestaurant } from '$lib/api/public';
	import type { PublicRestaurant } from '$lib/api/types';

	let backendOk = $state<boolean | null>(null);
	let restaurant = $state<PublicRestaurant | null>(null);

	onMount(async () => {
		backendOk = await checkHealth(fetch);
		try {
			restaurant = await getPublicRestaurant(fetch);
		} catch {
			restaurant = null;
		}
	});
</script>

<h1>Reservas de restaurante</h1>
{#if restaurant}
	<p class="muted">Bienvenido a {restaurant.nombre}.</p>
{:else}
	<p class="muted">Reserva tu mesa online de forma rápida y sencilla.</p>
{/if}

<section class="card hero-card">
	<h2 style="margin-top: 0">Reservar mesa</h2>
	<p class="muted">
		Elige fecha, turno y número de comensales. Recibirás confirmación al instante.
	</p>
	<a class="button-link" href="/reservar">Empezar reserva</a>
</section>

<section class="card" style="margin-top: 1.5rem">
	<h2 style="margin-top: 0">Estado del sistema</h2>
	{#if backendOk === null}
		<p class="muted">Comprobando…</p>
	{:else if backendOk}
		<p class="status-ok">Servicio disponible</p>
		{#if restaurant}
			<p class="muted">
				{restaurant.acepta_reservas
					? 'El restaurante acepta reservas en línea.'
					: 'El restaurante aún no acepta reservas en línea.'}
			</p>
		{/if}
	{:else}
		<p class="status-fail">
			No se pudo conectar al backend. ¿Está corriendo en <code>localhost:8000</code>?
		</p>
	{/if}
</section>

<p class="muted" style="margin-top: 1.5rem">
	<a href="/login">Entrar como administrador</a>
	·
	<a href="/register">Registrar primer admin</a>
</p>

<style>
	.hero-card {
		margin-top: 1.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		align-items: flex-start;
	}
</style>

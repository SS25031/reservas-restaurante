<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { ApiError } from '$lib/api/client';
	import { reabrirOnboarding } from '$lib/api/admin';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let reabriendo = $state(false);
	let mensaje = $state('');
	let error = $state('');

	async function onReabrirOnboarding() {
		if (!confirm('¿Reabrir el onboarding? Podrás volver a editar mesas, turnos y calendario.')) {
			return;
		}
		reabriendo = true;
		error = '';
		mensaje = '';
		try {
			await reabrirOnboarding(fetch);
			mensaje = 'Onboarding reabierto. La configuración inicial vuelve a estar editable.';
			await invalidateAll();
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudo reabrir el onboarding';
		} finally {
			reabriendo = false;
		}
	}
</script>

<h1>Panel de administración</h1>
<p class="muted">Bienvenido, {data.admin.email}.</p>

<section class="stats-grid">
	<article class="card stat-card">
		<p class="stat-label">Reservas activas</p>
		<p class="stat-value">{data.reservasCount}</p>
		<a href="/admin/reservas">Ver listado →</a>
	</article>
	<article class="card stat-card">
		<p class="stat-label">Onboarding</p>
		<p class="stat-value stat-value-sm">
			{data.onboarding.completado ? 'Completado' : 'Pendiente'}
		</p>
		<p class="muted">
			{data.onboarding.mesas_count} mesas · {data.onboarding.turnos_activos} turnos activos
		</p>
	</article>
</section>

<section class="card" style="margin-top: 1.5rem">
	<h2 style="margin-top: 0">Accesos rápidos</h2>
	<div class="actions-row">
		<a class="button-link" href="/admin/onboarding">Configurar restaurante</a>
		<a class="button-link secondary" href="/admin/reservas">Gestionar reservas</a>
		<a class="button-link secondary" href="/admin/calendario">Ver calendario</a>
	</div>
</section>

{#if data.onboarding.completado}
	<section class="card" style="margin-top: 1.5rem">
		<h2 style="margin-top: 0">Configuración inicial</h2>
		<p class="muted">
			Si necesitas cambiar mesas, turnos o calendario operativo, reabre el onboarding o edita
			la configuración directamente.
		</p>
		<div class="actions-row">
			<a class="button-link secondary" href="/admin/onboarding">Editar configuración</a>
			<button type="button" class="secondary" disabled={reabriendo} onclick={onReabrirOnboarding}>
				{reabriendo ? 'Reabriendo…' : 'Reabrir onboarding'}
			</button>
		</div>
		{#if mensaje}
			<p class="status-ok" style="margin-top: 0.75rem">{mensaje}</p>
		{/if}
		{#if error}
			<p class="error" style="margin-top: 0.75rem">{error}</p>
		{/if}
	</section>
{:else}
	<section class="card" style="margin-top: 1.5rem">
		<h2 style="margin-top: 0">Configuración pendiente</h2>
		<p class="muted">
			Completa el wizard de onboarding para definir mesas, turnos y calendario antes de abrir
			reservas públicas.
		</p>
		<a class="button-link" href="/admin/onboarding">Ir al onboarding</a>
	</section>
{/if}

<script lang="ts">
	import { ApiError } from '$lib/api/client';
	import { createPublicReserva, getDisponibilidad } from '$lib/api/public';
	import { formatFecha, isoDate } from '$lib/admin/format';
	import type { Disponibilidad, Reserva, TurnoApi } from '$lib/api/types';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	type Paso = 'busqueda' | 'datos' | 'exito';

	const hoy = isoDate(new Date());

	let paso = $state<Paso>('busqueda');
	let loading = $state(false);
	let error = $state('');

	let fecha = $state('');
	let personas = $state(2);
	let turno = $state<TurnoApi | ''>('');
	let disponibilidad = $state<Disponibilidad | null>(null);
	let reservaCreada = $state<Reserva | null>(null);

	let cliente = $state('');
	let telefono = $state('');
	let email = $state('');

	const turnosDisponibles = $derived(
		disponibilidad?.turnos.filter((item) => item.disponible) ?? []
	);

	async function onConsultar(event: SubmitEvent) {
		event.preventDefault();
		if (!data.restaurant.acepta_reservas) return;
		loading = true;
		error = '';
		turno = '';
		disponibilidad = null;
		try {
			const result = await getDisponibilidad(fetch, fecha, personas);
			disponibilidad = result;
			if (result.cerrado) {
				error = result.nota
					? `Este día está cerrado: ${result.nota}`
					: 'Este día está cerrado para reservas.';
				return;
			}
			const libres = result.turnos.filter((item) => item.disponible);
			if (!result.acepta_reservas || libres.length === 0) {
				error = 'No hay turnos disponibles para esa fecha y número de personas.';
				return;
			}
			turno = libres[0].turno;
			paso = 'datos';
		} catch (e) {
			error =
				e instanceof ApiError
					? e.message
					: 'No se pudo consultar la disponibilidad. Inténtelo más tarde.';
		} finally {
			loading = false;
		}
	}

	async function onReservar(event: SubmitEvent) {
		event.preventDefault();
		if (!turno || !fecha) return;
		loading = true;
		error = '';
		try {
			reservaCreada = await createPublicReserva(fetch, {
				cliente,
				telefono,
				email,
				personas,
				fecha,
				turno
			});
			paso = 'exito';
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudo completar la reserva';
		} finally {
			loading = false;
		}
	}

	function volverABusqueda() {
		paso = 'busqueda';
		error = '';
	}

	function nuevaReserva() {
		paso = 'busqueda';
		error = '';
		reservaCreada = null;
		disponibilidad = null;
		turno = '';
		cliente = '';
		telefono = '';
		email = '';
	}
</script>

<h1>Reservar mesa</h1>
<p class="muted">
	{#if data.restaurant.acepta_reservas}
		{data.restaurant.nombre} — grupos de hasta {data.restaurant.capacidad_maxima_grupo} personas.
	{:else}
		{data.restaurant.nombre} aún no acepta reservas en línea.
	{/if}
</p>

{#if !data.restaurant.acepta_reservas}
	<section class="card" style="margin-top: 1.5rem">
		<p class="muted">
			El restaurante está configurándose. Vuelve a intentarlo más tarde o contacta
			directamente con el local.
		</p>
	</section>
{:else}
	<ol class="steps" aria-label="Pasos de la reserva">
		<li class:active={paso === 'busqueda'}>1. Fecha y personas</li>
		<li class:active={paso === 'datos'}>2. Turno y datos</li>
		<li class:active={paso === 'exito'}>3. Confirmación</li>
	</ol>

	{#if paso === 'busqueda'}
		<form class="form card" style="margin-top: 1.5rem" onsubmit={onConsultar}>
			<h2 style="margin-top: 0">¿Cuándo venís?</h2>
			<div class="form-grid">
				<label>
					Fecha
					<input type="date" bind:value={fecha} min={hoy} required />
				</label>
				<label>
					Personas
					<input
						type="number"
						min="1"
						max={data.restaurant.capacidad_maxima_grupo}
						bind:value={personas}
						required
					/>
				</label>
			</div>
			{#if error}
				<p class="error">{error}</p>
			{/if}
			<button type="submit" disabled={loading}>
				{loading ? 'Consultando…' : 'Ver disponibilidad'}
			</button>
		</form>
	{:else if paso === 'datos' && disponibilidad}
		<section class="card summary-card">
			<p class="muted">Reserva para</p>
			<p><strong>{formatFecha(fecha)}</strong> · {personas} persona{personas === 1 ? '' : 's'}</p>
			<button type="button" class="secondary linkish" onclick={volverABusqueda}>Cambiar fecha</button>
		</section>

		<form class="form card" style="margin-top: 1rem" onsubmit={onReservar}>
			<h2 style="margin-top: 0">Elige turno y tus datos</h2>

			<fieldset class="turno-fieldset">
				<legend>Turno disponible</legend>
				<div class="turno-options">
					{#each turnosDisponibles as item (item.turno)}
						<label class="turno-option">
							<input type="radio" name="turno" value={item.turno} bind:group={turno} required />
							<span>
								<strong>{item.turno_label}</strong>
								<span class="muted">{item.mesas_libres} mesa{item.mesas_libres === 1 ? '' : 's'} libre{item.mesas_libres === 1 ? '' : 's'}</span>
							</span>
						</label>
					{/each}
				</div>
			</fieldset>

			<div class="form-grid">
				<label>
					Nombre
					<input bind:value={cliente} required autocomplete="name" />
				</label>
				<label>
					Teléfono
					<input bind:value={telefono} required autocomplete="tel" />
				</label>
				<label>
					Email
					<input type="email" bind:value={email} required autocomplete="email" />
				</label>
			</div>

			{#if error}
				<p class="error">{error}</p>
			{/if}

			<div class="actions-row">
				<button type="submit" disabled={loading}>
					{loading ? 'Reservando…' : 'Confirmar reserva'}
				</button>
				<button type="button" class="secondary" onclick={volverABusqueda}>Atrás</button>
			</div>
		</form>
	{:else if paso === 'exito' && reservaCreada}
		<section class="card success-card">
			<h2 style="margin-top: 0">¡Reserva confirmada!</h2>
			<p>Tu mesa quedó registrada con el número de reserva <strong>#{reservaCreada.id}</strong>.</p>
			<ul class="confirm-list">
				<li><strong>Fecha:</strong> {formatFecha(reservaCreada.fecha)}</li>
				<li><strong>Turno:</strong> {reservaCreada.turno_label}</li>
				<li><strong>Personas:</strong> {reservaCreada.personas}</li>
				<li><strong>Mesa:</strong> {reservaCreada.numero_mesa}</li>
				<li><strong>A nombre de:</strong> {reservaCreada.cliente}</li>
			</ul>
			<p class="muted">Te contactaremos al {reservaCreada.telefono} o {reservaCreada.email} si hace falta.</p>
			<div class="actions-row">
				<button type="button" onclick={nuevaReserva}>Hacer otra reserva</button>
				<a class="button-link secondary" href="/">Volver al inicio</a>
			</div>
		</section>
	{/if}
{/if}

<style>
	.steps {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem 1rem;
		margin: 1.25rem 0 0;
		padding: 0;
		list-style: none;
		font-size: 0.9rem;
		color: #6b7280;
	}

	.steps li.active {
		color: #2563eb;
		font-weight: 600;
	}

	.summary-card p {
		margin: 0.25rem 0;
	}

	.linkish {
		margin-top: 0.5rem;
		padding: 0;
		background: none;
		color: #2563eb;
		font-weight: 500;
	}

	.linkish:hover {
		background: none;
		text-decoration: underline;
	}

	.turno-fieldset {
		border: none;
		margin: 0;
		padding: 0;
	}

	.turno-fieldset legend {
		font-weight: 600;
		margin-bottom: 0.5rem;
	}

	.turno-options {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.turno-option {
		display: flex;
		align-items: flex-start;
		gap: 0.5rem;
		padding: 0.65rem 0.75rem;
		border: 1px solid #e5e7eb;
		border-radius: 0.375rem;
		cursor: pointer;
	}

	.turno-option:has(input:checked) {
		border-color: #2563eb;
		background: #eff6ff;
	}

	.turno-option span {
		display: flex;
		flex-direction: column;
		gap: 0.15rem;
	}

	.confirm-list {
		margin: 1rem 0;
		padding-left: 1.25rem;
	}

	.success-card {
		margin-top: 1.5rem;
	}
</style>

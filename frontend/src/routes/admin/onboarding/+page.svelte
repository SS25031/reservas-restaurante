<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import MesaCanvas from '$lib/components/onboarding/MesaCanvas.svelte';
	import { ApiError } from '$lib/api/client';
	import {
		completarOnboarding,
		saveCalendario,
		saveMesas,
		saveTurnos,
		updateRestaurant
	} from '$lib/api/onboarding';
	import { nextMesaNumero } from '$lib/onboarding/mesas';
	import type { CalendarDayConfig, MesaConfig, TurnoApi } from '$lib/api/types';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	type Paso = 'restaurant' | 'mesas' | 'turnos' | 'calendario' | 'completar';

	const pasos: { id: Paso; label: string }[] = [
		{ id: 'restaurant', label: 'Restaurante' },
		{ id: 'mesas', label: 'Mesas' },
		{ id: 'turnos', label: 'Turnos' },
		{ id: 'calendario', label: 'Calendario' },
		{ id: 'completar', label: 'Finalizar' }
	];

	const turnoLabels: Record<TurnoApi, string> = {
		MANANA: 'Mañana',
		TARDE: 'Tarde',
		NOCHE: 'Noche'
	};

	let paso = $state<Paso>('restaurant');
	let loading = $state(false);
	let error = $state('');
	let mensaje = $state('');

	let restaurantForm = $state({
		nombre: data.restaurant.nombre,
		max_reservas_por_dia: data.restaurant.max_reservas_por_dia,
		capacidad_maxima_grupo: data.restaurant.capacidad_maxima_grupo
	});

	let mesas = $state<MesaConfig[]>([...data.mesas]);
	let selectedMesa = $state<number | null>(mesas[0]?.numero ?? null);
	let turnos = $state([...data.turnos]);
	let calendario = $state<CalendarDayConfig[]>([...data.calendario]);

	let nuevoDia = $state({ fecha: '', cerrado: true, nota: '' });

	const mesaSeleccionada = $derived(mesas.find((mesa) => mesa.numero === selectedMesa) ?? null);
	const pasoIndex = $derived(pasos.findIndex((item) => item.id === paso));

	function irA(p: Paso) {
		paso = p;
		error = '';
		mensaje = '';
	}

	function anterior() {
		if (pasoIndex > 0) irA(pasos[pasoIndex - 1].id);
	}

	async function guardarRestaurant() {
		loading = true;
		error = '';
		try {
			const updated = await updateRestaurant(fetch, restaurantForm);
			restaurantForm = {
				nombre: updated.nombre,
				max_reservas_por_dia: updated.max_reservas_por_dia,
				capacidad_maxima_grupo: updated.capacidad_maxima_grupo
			};
			irA('mesas');
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudo guardar el restaurante';
		} finally {
			loading = false;
		}
	}

	async function guardarMesas() {
		if (mesas.length === 0) {
			error = 'Añade al menos una mesa.';
			return;
		}
		loading = true;
		error = '';
		try {
			mesas = await saveMesas(fetch, mesas);
			irA('turnos');
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudieron guardar las mesas';
		} finally {
			loading = false;
		}
	}

	function agregarMesa() {
		const numero = nextMesaNumero(mesas);
		const index = mesas.length;
		mesas = [
			...mesas,
			{
				numero,
				capacidad: 2,
				pos_x: 80 + (index % 5) * 120,
				pos_y: 70 + Math.floor(index / 5) * 90
			}
		];
		selectedMesa = numero;
	}

	function eliminarMesa() {
		if (selectedMesa === null) return;
		mesas = mesas.filter((mesa) => mesa.numero !== selectedMesa);
		selectedMesa = mesas[0]?.numero ?? null;
	}

	function actualizarCapacidad(event: Event) {
		if (selectedMesa === null) return;
		const value = Number((event.target as HTMLInputElement).value);
		mesas = mesas.map((mesa) =>
			mesa.numero === selectedMesa ? { ...mesa, capacidad: value } : mesa
		);
	}

	async function guardarTurnos() {
		if (!turnos.some((turno) => turno.activo)) {
			error = 'Activa al menos un turno.';
			return;
		}
		loading = true;
		error = '';
		try {
			turnos = await saveTurnos(fetch, turnos);
			irA('calendario');
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudieron guardar los turnos';
		} finally {
			loading = false;
		}
	}

	function agregarDiaCalendario() {
		if (!nuevoDia.fecha) {
			error = 'Indica una fecha.';
			return;
		}
		error = '';
		const resto = calendario.filter((dia) => dia.fecha !== nuevoDia.fecha);
		calendario = [
			...resto,
			{
				fecha: nuevoDia.fecha,
				cerrado: nuevoDia.cerrado,
				nota: nuevoDia.nota.trim() || null
			}
		].sort((a, b) => a.fecha.localeCompare(b.fecha));
		nuevoDia = { fecha: '', cerrado: true, nota: '' };
	}

	function quitarDia(fecha: string) {
		calendario = calendario.filter((dia) => dia.fecha !== fecha);
	}

	async function guardarCalendario() {
		loading = true;
		error = '';
		try {
			calendario = await saveCalendario(fetch, calendario);
			irA('completar');
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudo guardar el calendario';
		} finally {
			loading = false;
		}
	}

	async function onCompletar() {
		loading = true;
		error = '';
		mensaje = '';
		try {
			await completarOnboarding(fetch);
			mensaje = 'Onboarding completado. El restaurante ya acepta reservas públicas.';
			await invalidateAll();
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudo completar el onboarding';
		} finally {
			loading = false;
		}
	}
</script>

<h1>Configuración del restaurante</h1>
<p class="muted">
	Wizard de onboarding — define mesas, turnos y excepciones de calendario antes de abrir
	reservas públicas.
</p>

<ol class="steps">
	{#each pasos as item, index (item.id)}
		<li class:active={paso === item.id} class:done={index < pasoIndex}>
			<button type="button" class="step-button" onclick={() => irA(item.id)}>{item.label}</button>
		</li>
	{/each}
</ol>

{#if paso === 'restaurant'}
	<form
		class="form card"
		style="margin-top: 1.5rem"
		onsubmit={(event) => {
			event.preventDefault();
			guardarRestaurant();
		}}
	>
		<h2 style="margin-top: 0">Datos del restaurante</h2>
		<div class="form-grid">
			<label>
				Nombre
				<input bind:value={restaurantForm.nombre} required />
			</label>
			<label>
				Máx. reservas por día
				<input type="number" min="1" bind:value={restaurantForm.max_reservas_por_dia} required />
			</label>
			<label>
				Capacidad máxima por grupo
				<input type="number" min="1" bind:value={restaurantForm.capacidad_maxima_grupo} required />
			</label>
		</div>
		{#if error}<p class="error">{error}</p>{/if}
		<button type="submit" disabled={loading}>{loading ? 'Guardando…' : 'Siguiente'}</button>
	</form>
{:else if paso === 'mesas'}
	<section class="card" style="margin-top: 1.5rem">
		<h2 style="margin-top: 0">Layout de mesas</h2>
		<MesaCanvas bind:mesas bind:selectedNumero={selectedMesa} />
		<div class="actions-row" style="margin-top: 1rem">
			<button type="button" class="secondary" onclick={agregarMesa}>Añadir mesa</button>
			<button type="button" class="danger" disabled={selectedMesa === null} onclick={eliminarMesa}>
				Eliminar seleccionada
			</button>
		</div>
		{#if mesaSeleccionada}
			<label style="margin-top: 1rem; max-width: 12rem">
				Capacidad (M{mesaSeleccionada.numero})
				<input
					type="number"
					min="1"
					value={mesaSeleccionada.capacidad}
					oninput={actualizarCapacidad}
				/>
			</label>
		{/if}
		{#if error}<p class="error">{error}</p>{/if}
		<div class="actions-row" style="margin-top: 1rem">
			<button type="button" class="secondary" onclick={anterior}>Atrás</button>
			<button type="button" disabled={loading} onclick={guardarMesas}>
				{loading ? 'Guardando…' : 'Guardar y continuar'}
			</button>
		</div>
	</section>
{:else if paso === 'turnos'}
	<section class="card" style="margin-top: 1.5rem">
		<h2 style="margin-top: 0">Turnos de servicio</h2>
		<div class="turno-list">
			{#each turnos as turno, index (turno.turno)}
				<article class="turno-row">
					<label class="turno-toggle">
						<input type="checkbox" bind:checked={turnos[index].activo} />
						<strong>{turnoLabels[turno.turno]}</strong>
					</label>
					<label>
						Inicio
						<input
							type="time"
							value={turnos[index].hora_inicio ?? ''}
							oninput={(event) => {
								const value = (event.currentTarget as HTMLInputElement).value;
								turnos[index].hora_inicio = value || null;
							}}
						/>
					</label>
					<label>
						Fin
						<input
							type="time"
							value={turnos[index].hora_fin ?? ''}
							oninput={(event) => {
								const value = (event.currentTarget as HTMLInputElement).value;
								turnos[index].hora_fin = value || null;
							}}
						/>
					</label>
				</article>
			{/each}
		</div>
		{#if error}<p class="error">{error}</p>{/if}
		<div class="actions-row" style="margin-top: 1rem">
			<button type="button" class="secondary" onclick={anterior}>Atrás</button>
			<button type="button" disabled={loading} onclick={guardarTurnos}>
				{loading ? 'Guardando…' : 'Guardar y continuar'}
			</button>
		</div>
	</section>
{:else if paso === 'calendario'}
	<section class="card" style="margin-top: 1.5rem">
		<h2 style="margin-top: 0">Excepciones de calendario</h2>
		<p class="muted">Opcional: marca días cerrados o añade una nota operativa.</p>

		<form
			class="form-grid"
			style="margin-top: 1rem"
			onsubmit={(event) => {
				event.preventDefault();
				agregarDiaCalendario();
			}}
		>
			<label>
				Fecha
				<input type="date" bind:value={nuevoDia.fecha} required />
			</label>
			<label class="inline-check">
				<input type="checkbox" bind:checked={nuevoDia.cerrado} />
				Día cerrado
			</label>
			<label>
				Nota
				<input bind:value={nuevoDia.nota} placeholder="Opcional" />
			</label>
			<button type="submit" class="secondary">Añadir</button>
		</form>

		{#if calendario.length > 0}
			<ul class="calendar-list">
				{#each calendario as dia (dia.fecha)}
					<li>
						<strong>{dia.fecha}</strong>
						— {dia.cerrado ? 'Cerrado' : 'Abierto'}
						{#if dia.nota}
							· {dia.nota}
						{/if}
						<button type="button" class="linkish" onclick={() => quitarDia(dia.fecha)}>Quitar</button>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="muted">Sin excepciones — todos los días usan los turnos configurados.</p>
		{/if}

		{#if error}<p class="error">{error}</p>{/if}
		<div class="actions-row" style="margin-top: 1rem">
			<button type="button" class="secondary" onclick={anterior}>Atrás</button>
			<button type="button" disabled={loading} onclick={guardarCalendario}>
				{loading ? 'Guardando…' : 'Guardar y continuar'}
			</button>
		</div>
	</section>
{:else}
	<section class="card" style="margin-top: 1.5rem">
		<h2 style="margin-top: 0">Resumen</h2>
		<ul class="summary-list">
			<li><strong>Restaurante:</strong> {restaurantForm.nombre}</li>
			<li><strong>Mesas:</strong> {mesas.length}</li>
			<li><strong>Turnos activos:</strong> {turnos.filter((t) => t.activo).length}</li>
			<li><strong>Excepciones calendario:</strong> {calendario.length}</li>
			<li>
				<strong>Estado:</strong>
				{data.estado.completado ? 'Completado' : 'Pendiente de finalizar'}
			</li>
		</ul>

		{#if data.estado.completado}
			<p class="status-ok">El onboarding ya está completado. Puedes editar pasos anteriores o ir al panel.</p>
		{:else}
			<p class="muted">Al completar, el restaurante empezará a aceptar reservas en `/reservar`.</p>
		{/if}

		{#if mensaje}<p class="status-ok">{mensaje}</p>{/if}
		{#if error}<p class="error">{error}</p>{/if}

		<div class="actions-row" style="margin-top: 1rem">
			<button type="button" class="secondary" onclick={anterior}>Atrás</button>
			{#if !data.estado.completado}
				<button type="button" disabled={loading} onclick={onCompletar}>
					{loading ? 'Completando…' : 'Completar onboarding'}
				</button>
			{/if}
			<a class="button-link secondary" href="/admin">Ir al panel</a>
		</div>
	</section>
{/if}

<style>
	.steps {
		display: flex;
		flex-wrap: wrap;
		gap: 0.35rem;
		margin: 1.25rem 0 0;
		padding: 0;
		list-style: none;
	}

	.step-button {
		border: 1px solid #e5e7eb;
		background: #fff;
		color: #374151;
		padding: 0.35rem 0.75rem;
		border-radius: 999px;
		font-size: 0.85rem;
		cursor: pointer;
	}

	.steps li.active .step-button {
		background: #2563eb;
		border-color: #2563eb;
		color: #fff;
		font-weight: 600;
	}

	.steps li.done .step-button {
		border-color: #93c5fd;
		color: #1d4ed8;
	}

	.turno-list {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.turno-row {
		display: grid;
		grid-template-columns: 1fr repeat(2, minmax(8rem, 1fr));
		gap: 0.75rem;
		align-items: end;
		padding: 0.75rem;
		border: 1px solid #e5e7eb;
		border-radius: 0.375rem;
	}

	.turno-toggle {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.inline-check {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding-top: 1.5rem;
	}

	.calendar-list,
	.summary-list {
		margin: 1rem 0 0;
		padding-left: 1.25rem;
	}

	.linkish {
		margin-left: 0.5rem;
		padding: 0;
		background: none;
		color: #2563eb;
		font-size: 0.85rem;
	}

	.linkish:hover {
		background: none;
		text-decoration: underline;
	}

	@media (max-width: 640px) {
		.turno-row {
			grid-template-columns: 1fr;
		}

		.inline-check {
			padding-top: 0;
		}
	}
</style>

<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { ApiError } from '$lib/api/client';
	import { cancelReserva, createReserva, updateReserva } from '$lib/api/admin';
	import { formatFecha, TURNOS } from '$lib/admin/format';
	import type { Reserva, TurnoApi } from '$lib/api/types';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let showCreate = $state(false);
	let editingId = $state<number | null>(null);
	let loading = $state(false);
	let error = $state('');

	let createForm = $state({
		cliente: '',
		telefono: '',
		email: '',
		personas: 2,
		fecha: '',
		turno: 'NOCHE' as TurnoApi
	});

	let editForm = $state({
		fecha: '',
		turno: 'NOCHE' as TurnoApi
	});

	function startEdit(reserva: Reserva) {
		editingId = reserva.id;
		editForm = { fecha: reserva.fecha, turno: reserva.turno };
		error = '';
	}

	function cancelEdit() {
		editingId = null;
		error = '';
	}

	async function onCreate(event: SubmitEvent) {
		event.preventDefault();
		loading = true;
		error = '';
		try {
			await createReserva(fetch, createForm);
			showCreate = false;
			createForm = {
				cliente: '',
				telefono: '',
				email: '',
				personas: 2,
				fecha: '',
				turno: 'NOCHE'
			};
			await invalidateAll();
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudo crear la reserva';
		} finally {
			loading = false;
		}
	}

	async function onUpdate(event: SubmitEvent) {
		event.preventDefault();
		if (editingId === null) return;
		loading = true;
		error = '';
		try {
			await updateReserva(fetch, editingId, editForm);
			editingId = null;
			await invalidateAll();
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudo actualizar la reserva';
		} finally {
			loading = false;
		}
	}

	async function onCancelReserva(reserva: Reserva) {
		if (!confirm(`¿Cancelar la reserva de ${reserva.cliente} (${formatFecha(reserva.fecha)})?`)) {
			return;
		}
		loading = true;
		error = '';
		try {
			await cancelReserva(fetch, reserva.id);
			if (editingId === reserva.id) editingId = null;
			await invalidateAll();
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'No se pudo cancelar la reserva';
		} finally {
			loading = false;
		}
	}
</script>

<h1>Reservas</h1>
<p class="muted">Listado de reservas activas. Crea, edita fecha/turno o cancela.</p>

<div class="actions-row" style="margin: 1rem 0">
	<button type="button" onclick={() => (showCreate = !showCreate)}>
		{showCreate ? 'Ocultar formulario' : 'Nueva reserva'}
	</button>
</div>

{#if showCreate}
	<form class="form card" style="margin-bottom: 1.5rem" onsubmit={onCreate}>
		<h2 style="margin-top: 0">Nueva reserva</h2>
		<div class="form-grid">
			<label>
				Cliente
				<input bind:value={createForm.cliente} required />
			</label>
			<label>
				Teléfono
				<input bind:value={createForm.telefono} required />
			</label>
			<label>
				Email
				<input type="email" bind:value={createForm.email} required />
			</label>
			<label>
				Personas
				<input type="number" min="1" bind:value={createForm.personas} required />
			</label>
			<label>
				Fecha
				<input type="date" bind:value={createForm.fecha} required />
			</label>
			<label>
				Turno
				<select bind:value={createForm.turno}>
					{#each TURNOS as turno (turno.value)}
						<option value={turno.value}>{turno.label}</option>
					{/each}
				</select>
			</label>
		</div>
		<button type="submit" disabled={loading}>{loading ? 'Guardando…' : 'Crear reserva'}</button>
	</form>
{/if}

{#if editingId !== null}
	<form class="form card" style="margin-bottom: 1.5rem" onsubmit={onUpdate}>
		<h2 style="margin-top: 0">Editar reserva #{editingId}</h2>
		<div class="form-grid">
			<label>
				Fecha
				<input type="date" bind:value={editForm.fecha} required />
			</label>
			<label>
				Turno
				<select bind:value={editForm.turno}>
					{#each TURNOS as turno (turno.value)}
						<option value={turno.value}>{turno.label}</option>
					{/each}
				</select>
			</label>
		</div>
		<div class="actions-row">
			<button type="submit" disabled={loading}>{loading ? 'Guardando…' : 'Guardar cambios'}</button>
			<button type="button" class="secondary" onclick={cancelEdit}>Cancelar edición</button>
		</div>
	</form>
{/if}

{#if error}
	<p class="error">{error}</p>
{/if}

{#if data.reservas.length === 0}
	<section class="card">
		<p class="muted">No hay reservas activas. Crea la primera con el botón de arriba.</p>
	</section>
{:else}
	<div class="table-wrap card">
		<table class="data-table">
			<thead>
				<tr>
					<th>Fecha</th>
					<th>Turno</th>
					<th>Cliente</th>
					<th>Personas</th>
					<th>Mesa</th>
					<th>Contacto</th>
					<th></th>
				</tr>
			</thead>
			<tbody>
				{#each data.reservas as reserva (reserva.id)}
					<tr>
						<td>{formatFecha(reserva.fecha)}</td>
						<td>{reserva.turno_label}</td>
						<td>{reserva.cliente}</td>
						<td>{reserva.personas}</td>
						<td>{reserva.numero_mesa}</td>
						<td>
							<span class="muted">{reserva.telefono}</span><br />
							<span class="muted">{reserva.email}</span>
						</td>
						<td class="table-actions">
							<button type="button" class="secondary" disabled={loading} onclick={() => startEdit(reserva)}>
								Editar
							</button>
							<button
								type="button"
								class="danger"
								disabled={loading}
								onclick={() => onCancelReserva(reserva)}
							>
								Cancelar
							</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}

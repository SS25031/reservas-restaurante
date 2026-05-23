<script lang="ts">
	import { goto } from '$app/navigation';
	import {
		buildMonthGrid,
		DIAS_SEMANA,
		formatMesAnio,
		groupReservasByDate,
		isoDate
	} from '$lib/admin/format';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const today = new Date();
	let year = $state(today.getFullYear());
	let month = $state(today.getMonth());
	let selectedDate = $state<string | null>(null);

	const byDate = $derived(groupReservasByDate(data.reservas));
	const grid = $derived(buildMonthGrid(year, month));
	const selectedReservas = $derived(
		selectedDate ? (byDate.get(selectedDate) ?? []) : []
	);

	function prevMonth() {
		if (month === 0) {
			month = 11;
			year -= 1;
		} else {
			month -= 1;
		}
		selectedDate = null;
	}

	function nextMonth() {
		if (month === 11) {
			month = 0;
			year += 1;
		} else {
			month += 1;
		}
		selectedDate = null;
	}

	function selectDay(date: Date) {
		selectedDate = isoDate(date);
	}

	function goToReservas() {
		goto('/admin/reservas');
	}
</script>

<h1>Calendario</h1>
<p class="muted">Vista mensual de reservas activas. Haz clic en un día para ver el detalle.</p>

<section class="card calendar-shell">
	<div class="calendar-toolbar">
		<button type="button" class="secondary" onclick={prevMonth} aria-label="Mes anterior">←</button>
		<h2 style="margin: 0; text-transform: capitalize">{formatMesAnio(year, month)}</h2>
		<button type="button" class="secondary" onclick={nextMonth} aria-label="Mes siguiente">→</button>
	</div>

	<div class="calendar-grid" role="grid" aria-label="Calendario de reservas">
		{#each DIAS_SEMANA as dia (dia)}
			<div class="calendar-weekday" role="columnheader">{dia}</div>
		{/each}
		{#each grid as cell, index (index)}
			{#if cell}
				{@const key = isoDate(cell)}
				{@const count = byDate.get(key)?.length ?? 0}
				{@const isToday = key === isoDate(today)}
				{@const isSelected = selectedDate === key}
				<button
					type="button"
					class="calendar-day"
					class:today={isToday}
					class:selected={isSelected}
					class:has-reservas={count > 0}
					onclick={() => selectDay(cell)}
				>
					<span class="day-number">{cell.getDate()}</span>
					{#if count > 0}
						<span class="day-badge">{count} reserva{count === 1 ? '' : 's'}</span>
					{/if}
				</button>
			{:else}
				<div class="calendar-day empty" aria-hidden="true"></div>
			{/if}
		{/each}
	</div>
</section>

<section class="card" style="margin-top: 1.5rem">
	{#if selectedDate}
		<h2 style="margin-top: 0">
			{selectedReservas.length} reserva{selectedReservas.length === 1 ? '' : 's'} — {selectedDate}
		</h2>
		{#if selectedReservas.length === 0}
			<p class="muted">Sin reservas este día.</p>
		{:else}
			<ul class="reserva-list">
				{#each selectedReservas as reserva (reserva.id)}
					<li>
						<strong>{reserva.turno_label}</strong> — {reserva.cliente} ({reserva.personas} p.)
						· Mesa {reserva.numero_mesa}
					</li>
				{/each}
			</ul>
		{/if}
	{:else}
		<p class="muted">Selecciona un día del calendario para ver las reservas.</p>
	{/if}
	<div class="actions-row" style="margin-top: 1rem">
		<button type="button" class="secondary" onclick={goToReservas}>Ir al listado</button>
	</div>
</section>

<style>
	.calendar-shell {
		padding: 1rem;
	}

	.calendar-toolbar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.calendar-grid {
		display: grid;
		grid-template-columns: repeat(7, minmax(0, 1fr));
		gap: 0.35rem;
	}

	.calendar-weekday {
		font-size: 0.75rem;
		font-weight: 600;
		color: #6b7280;
		text-align: center;
		padding: 0.25rem;
	}

	.calendar-day {
		min-height: 4.5rem;
		border: 1px solid #e5e7eb;
		border-radius: 0.375rem;
		background: #fff;
		padding: 0.35rem;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.25rem;
		cursor: pointer;
		text-align: left;
	}

	.calendar-day.empty {
		border: none;
		background: transparent;
		cursor: default;
		min-height: 0;
	}

	.calendar-day.today {
		border-color: #2563eb;
	}

	.calendar-day.selected {
		background: #eff6ff;
		border-color: #2563eb;
	}

	.calendar-day.has-reservas .day-badge {
		color: #1d4ed8;
		font-weight: 600;
	}

	.day-number {
		font-weight: 600;
	}

	.day-badge {
		font-size: 0.75rem;
		color: #6b7280;
	}

	.reserva-list {
		margin: 0;
		padding-left: 1.25rem;
	}
</style>

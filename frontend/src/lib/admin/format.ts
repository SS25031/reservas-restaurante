import type { Reserva, TurnoApi } from '$lib/api/types';

export const TURNOS: { value: TurnoApi; label: string }[] = [
	{ value: 'MANANA', label: 'Mañana' },
	{ value: 'TARDE', label: 'Tarde' },
	{ value: 'NOCHE', label: 'Noche' }
];

const fechaLarga = new Intl.DateTimeFormat('es-ES', {
	weekday: 'long',
	day: 'numeric',
	month: 'long',
	year: 'numeric'
});

const mesAnio = new Intl.DateTimeFormat('es-ES', { month: 'long', year: 'numeric' });

export function formatFecha(iso: string): string {
	return fechaLarga.format(new Date(iso + 'T12:00:00'));
}

export function formatMesAnio(year: number, month: number): string {
	return mesAnio.format(new Date(year, month, 1));
}

export function isoDate(d: Date): string {
	const y = d.getFullYear();
	const m = String(d.getMonth() + 1).padStart(2, '0');
	const day = String(d.getDate()).padStart(2, '0');
	return `${y}-${m}-${day}`;
}

export function groupReservasByDate(reservas: Reserva[]): Map<string, Reserva[]> {
	const map = new Map<string, Reserva[]>();
	for (const reserva of reservas) {
		const list = map.get(reserva.fecha) ?? [];
		list.push(reserva);
		map.set(reserva.fecha, list);
	}
	for (const list of map.values()) {
		list.sort((a, b) => a.turno.localeCompare(b.turno) || a.numero_mesa - b.numero_mesa);
	}
	return map;
}

/** Cuadrícula de un mes: null = celda vacía antes del día 1. */
export function buildMonthGrid(year: number, month: number): (Date | null)[] {
	const first = new Date(year, month, 1);
	const startOffset = (first.getDay() + 6) % 7; // lunes = 0
	const daysInMonth = new Date(year, month + 1, 0).getDate();
	const cells: (Date | null)[] = Array.from({ length: startOffset }, () => null);
	for (let day = 1; day <= daysInMonth; day++) {
		cells.push(new Date(year, month, day));
	}
	while (cells.length % 7 !== 0) {
		cells.push(null);
	}
	return cells;
}

export const DIAS_SEMANA = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];

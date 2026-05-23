import type { MesaConfig } from '$lib/api/types';

const TABLE_RADIUS = 34;
const CANVAS_WIDTH = 720;
const CANVAS_HEIGHT = 420;

export function defaultPosition(index: number): { x: number; y: number } {
	const col = index % 5;
	const row = Math.floor(index / 5);
	return { x: 80 + col * 120, y: 70 + row * 90 };
}

export function normalizeMesas(mesas: MesaConfig[]): MesaConfig[] {
	return mesas.map((mesa, index) => {
		const pos = defaultPosition(index);
		return {
			...mesa,
			pos_x: mesa.pos_x ?? pos.x,
			pos_y: mesa.pos_y ?? pos.y
		};
	});
}

export function nextMesaNumero(mesas: MesaConfig[]): number {
	if (mesas.length === 0) return 1;
	return Math.max(...mesas.map((mesa) => mesa.numero)) + 1;
}

export { CANVAS_HEIGHT, CANVAS_WIDTH, TABLE_RADIUS };

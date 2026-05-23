<script lang="ts">
	import { browser } from '$app/environment';
	import type { MesaConfig } from '$lib/api/types';
	import {
		CANVAS_HEIGHT,
		CANVAS_WIDTH,
		TABLE_RADIUS,
		defaultPosition
	} from '$lib/onboarding/mesas';
	import { onDestroy, onMount } from 'svelte';
	import type Konva from 'konva';

	let {
		mesas = $bindable([]),
		selectedNumero = $bindable<number | null>(null)
	} = $props<{ mesas: MesaConfig[]; selectedNumero?: number | null }>();

	let container: HTMLDivElement | undefined = $state();
	let stage: Konva.Stage | null = null;
	let layer: Konva.Layer | null = null;
	let KonvaLib: typeof Konva | null = null;

	function syncShapes() {
		if (!layer || !KonvaLib) return;
		layer.destroyChildren();

		for (const mesa of mesas) {
			const x = mesa.pos_x ?? defaultPosition(mesa.numero - 1).x;
			const y = mesa.pos_y ?? defaultPosition(mesa.numero - 1).y;
			const selected = selectedNumero === mesa.numero;

			const group = new KonvaLib.Group({
				x,
				y,
				draggable: true,
				name: `mesa-${mesa.numero}`
			});

			const circle = new KonvaLib.Circle({
				radius: TABLE_RADIUS,
				fill: selected ? '#dbeafe' : '#f3f4f6',
				stroke: selected ? '#2563eb' : '#9ca3af',
				strokeWidth: selected ? 3 : 1.5
			});

			const label = new KonvaLib.Text({
				text: `M${mesa.numero}\n${mesa.capacidad}p`,
				fontSize: 13,
				fontStyle: 'bold',
				fill: '#111827',
				align: 'center',
				width: TABLE_RADIUS * 2,
				offsetX: TABLE_RADIUS,
				offsetY: 14
			});

			group.on('click tap', () => {
				selectedNumero = mesa.numero;
				syncShapes();
			});

			group.on('dragend', () => {
				const pos = group.position();
				mesas = mesas.map((item: MesaConfig) =>
					item.numero === mesa.numero
						? {
								...item,
								pos_x: Math.round(pos.x),
								pos_y: Math.round(pos.y)
							}
						: item
				);
			});

			group.add(circle);
			group.add(label);
			layer.add(group);
		}

		layer.batchDraw();
	}

	onMount(async () => {
		if (!browser || !container) return;
		const mod = await import('konva');
		KonvaLib = mod.default;
		stage = new KonvaLib.Stage({
			container,
			width: CANVAS_WIDTH,
			height: CANVAS_HEIGHT
		});
		layer = new KonvaLib.Layer();
		stage.add(layer);

		const background = new KonvaLib.Rect({
			x: 0,
			y: 0,
			width: CANVAS_WIDTH,
			height: CANVAS_HEIGHT,
			fill: '#fafafa',
			stroke: '#e5e7eb',
			strokeWidth: 1,
			listening: false
		});
		layer.add(background);
		syncShapes();

		stage.on('click tap', (event) => {
			if (event.target === stage || event.target === background) {
				selectedNumero = null;
				syncShapes();
			}
		});
	});

	$effect(() => {
		mesas;
		selectedNumero;
		syncShapes();
	});

	onDestroy(() => {
		stage?.destroy();
		stage = null;
		layer = null;
	});
</script>

<div class="canvas-wrap">
	<div bind:this={container} class="konva-host" role="img" aria-label="Plano de mesas del restaurante"></div>
	<p class="muted canvas-hint">Arrastra las mesas para colocarlas. Haz clic para seleccionar.</p>
</div>

<style>
	.canvas-wrap {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.konva-host {
		width: 100%;
		max-width: 720px;
		border: 1px solid #e5e7eb;
		border-radius: 0.5rem;
		overflow: hidden;
		background: #fafafa;
	}

	.canvas-hint {
		margin: 0;
		font-size: 0.85rem;
	}
</style>

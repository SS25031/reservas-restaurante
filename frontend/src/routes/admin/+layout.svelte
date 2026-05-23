<script lang="ts">
	import { goto } from '$app/navigation';
	import { logout } from '$lib/api/auth';
	import type { LayoutData } from './$types';

	let { data, children } = $props<{ data: LayoutData; children: import('svelte').Snippet }>();

	async function onLogout() {
		await logout(fetch);
		await goto('/login');
	}
</script>

<header class="site-header">
	<a class="brand" href="/admin">Panel admin</a>
	<nav>
		<span class="muted">{data.admin.email}</span>
		<a href="/admin">Inicio</a>
		<button type="button" class="secondary" onclick={onLogout}>Salir</button>
	</nav>
</header>

<main>
	{@render children()}
</main>

<style>
	header button.secondary {
		padding: 0.35rem 0.75rem;
		font-size: 0.875rem;
	}
</style>

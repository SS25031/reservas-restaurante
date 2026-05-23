<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { logout } from '$lib/api/auth';
	import type { LayoutData } from './$types';

	let { data, children } = $props<{ data: LayoutData; children: import('svelte').Snippet }>();

	async function onLogout() {
		await logout(fetch);
		await goto('/login');
	}

	function isActive(href: string): boolean {
		const path = page.url.pathname;
		if (href === '/admin') return path === '/admin';
		return path === href || path.startsWith(`${href}/`);
	}
</script>

<header class="site-header">
	<a class="brand" href="/admin">Panel admin</a>
	<nav>
		<a href="/admin" class:nav-active={isActive('/admin')}>Inicio</a>
		<a href="/admin/reservas" class:nav-active={isActive('/admin/reservas')}>Reservas</a>
		<a href="/admin/calendario" class:nav-active={isActive('/admin/calendario')}>Calendario</a>
		<span class="muted">{data.admin.email}</span>
		<button type="button" class="secondary" onclick={onLogout}>Salir</button>
	</nav>
</header>

<main class="admin-main">
	{@render children()}
</main>

<style>
	header button.secondary {
		padding: 0.35rem 0.75rem;
		font-size: 0.875rem;
	}

	nav a.nav-active {
		color: #2563eb;
		font-weight: 700;
	}
</style>

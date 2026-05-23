<script lang="ts">
	let { children } = $props();
</script>

<header class="site-header">
	<a class="brand" href="/">Reservas Restaurante</a>
	<nav>
		<a href="/">Inicio</a>
		<a href="/login">Admin</a>
	</nav>
</header>

<main>
	{@render children()}
</main>

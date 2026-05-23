<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<h1>Panel de administración</h1>
<p class="muted">Bienvenido, {data.admin.email}.</p>

<section class="card" style="margin-top: 1.5rem">
	<h2 style="margin-top: 0">Próximos pasos</h2>
	<ul>
		<li><strong>Onboarding</strong> — configurar mesas, turnos y calendario (subsistema 7)</li>
		<li><strong>Reservas</strong> — gestionar reservas desde el dashboard (subsistemas 5 y 9)</li>
	</ul>
	<p class="muted">
		La API de onboarding ya está protegida; las pantallas de configuración llegarán en el
		siguiente subsistema de UI.
	</p>
</section>

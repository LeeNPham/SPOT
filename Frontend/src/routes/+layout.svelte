<script>
	import '../app.postcss';
	import './styles.css';
	import NavMenu from '../lib/components/NavMenu.svelte';
	import { isLoggedIn } from '$store/stores';
	import { browser } from '$app/environment';

	$: {
		if (browser) {
			if (!document.cookie) {
				$isLoggedIn = false;
			}
		}
	}
</script>

<div class="app">
	{#if $isLoggedIn == true}
		<div class="w-full flex justify-start p-5 bg-gray-700"><NavMenu /></div>
	{/if}
	<main>
		<slot />
	</main>

	<footer>
		<p>visit <a href="https://www.github.com/leenpham">My Github</a> to learn more about me!</p>
	</footer>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	footer a {
		font-weight: bold;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>

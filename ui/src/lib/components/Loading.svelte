<script>
	export let loading;
	export let message;
	import '../../routes/styles.css';
	import { fly } from 'svelte/transition';

	let messages = [
		'Loading...',
		'This may take some time...',
		"Please don't go, we love you!",
		'I too, hate waiting...',
		"I'm bored...",
		'Vectorizing entire documents takes some time...'
	];
	let elseMessage = messages[Math.floor(Math.random() * messages.length)];

	// Function to update the elseMessage every 3 seconds
	let interval;
	$: {
		clearInterval(interval);
		interval = setInterval(() => {
			elseMessage = messages[Math.floor(Math.random() * messages.length)];
		}, 5000);
	}
</script>

{#if loading}
	<div class="loading-overlay">
		<div class="loading-spinner" />
		{#if message}
			<h1>{message}</h1>
		{:else}
			{#key elseMessage}
				<h1 in:fly={{ x: -200 }} out:fly={{ x: 200 }}>{elseMessage}</h1>
			{/key}
		{/if}
	</div>
{/if}

<div class="loading-content" class:loading={loading}>
	<slot />
</div>

<style>
	h1 {
		color: var(--color-theme-2);
		position: absolute;
        left:50%;
        top: 50%;
        transform: translate(-50%, -50%);
	}
	.loading-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.6);
		z-index: 9999;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.loading-content {
		position: relative;
		z-index: 1;
	}

	.loading-spinner {
        position: absolute;
        left: calc(50% - 24px);
        top: calc(50% - 75px);
		border: 4px solid rgba(255, 255, 255, 0.3);
		border-top: 4px solid #fff;
		border-radius: 50%;
		width: 40px;
		height: 40px;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>

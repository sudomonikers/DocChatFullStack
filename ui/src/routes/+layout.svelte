<script>
	import './styles.css';
	import { page } from '$app/stores';
	import github from '$lib/images/github.svg';
	import { fly } from 'svelte/transition';
	import { BASE_API } from '$lib/environment';

	let isMenuOpen = false;

	function toggleMenu() {
		isMenuOpen = !isMenuOpen;
	}

	// Function to handle keyboard events for the hamburger menu
	function handleMenuKeyPress(event) {
		// Check for Enter (key code 13) or Space (key code 32) key press
		if (event.key === 'Enter' || event.key === ' ' || event.key === 'Spacebar') {
			event.preventDefault();
			toggleMenu(!isMenuOpen);
		}
	}

	let documents = [];
	function getUploadedDocuments() {
		fetch(`${BASE_API}/all-document-titles`)
			.then((response) => response.json())
			.then((data) => {
				documents = data;
			});
	}
	getUploadedDocuments();
</script>

<div class="app">
	<header>
		<div class="corner">
			<div
				class="hamburger-menu"
				role="button"
				aria-label="Toggle Menu"
				tabindex="0"
				on:click={toggleMenu}
				on:keydown={handleMenuKeyPress}
				on:keyup={handleMenuKeyPress}
			>
				<div />
				<div />
				<div />
			</div>
		</div>

		<nav>
			<svg viewBox="0 0 2 3" aria-hidden="true">
				<path d="M0,0 L1,2 C1.5,3 1.5,3 2,3 L2,0 Z" />
			</svg>
			<ul>
				<li aria-current={$page.url.pathname === '/' ? 'page' : undefined}>
					<a href="/">Home</a>
				</li>
				<li aria-current={$page.url.pathname === '/upload' ? 'page' : undefined}>
					<a href="/upload">Upload</a>
				</li>
			</ul>
			<svg viewBox="0 0 2 3" aria-hidden="true">
				<path d="M0,0 L0,3 C0.5,3 0.5,3 1,2 L2,0 Z" />
			</svg>
		</nav>

		<div class="corner">
			<a href="https://github.com/sudomonikers/DocChatFullStack" target="_blank">
				<img src={github} alt="GitHub" />
			</a>
		</div>
	</header>

	<main>
		{#if isMenuOpen}
			<div>
				<div class="slideout-menu" transition:fly={{ y: 200, duration: 1000 }}>
					<h1>Chat With Document:</h1>
					{#each documents as document}
						<a href="/chat-with-file/{document}" on:click={toggleMenu}>{document}</a>
					{/each}
				</div>
			</div>
		{/if}
		<slot />
	</main>

	<footer />
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
		width: 100%;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}

	header {
		display: flex;
		justify-content: space-between;
		height: 48px;
	}

	.corner {
		width: 3em;
		height: 3em;
	}

	.corner a {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.corner img {
		width: 2em;
		height: 2em;
		object-fit: contain;
	}

	nav {
		display: flex;
		justify-content: center;
		--background: var(--color-theme-1);
	}

	svg {
		width: 2em;
		height: 3em;
		display: block;
	}

	path {
		fill: var(--background);
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background: var(--background);
		background-size: contain;
	}

	li {
		position: relative;
		height: 100%;
	}

	li[aria-current='page']::before {
		--size: 6px;
		content: '';
		width: 0;
		height: 0;
		position: absolute;
		top: 0;
		left: calc(50% - var(--size));
		border: var(--size) solid transparent;
		border-top: var(--size) solid var(--color-theme-1);
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.5rem;
		color: var(--color-theme-2);
		font-weight: 700;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	a:hover {
		color: var(--color-theme-3);
	}

	.hamburger-menu {
		display: flex;
		flex-direction: column;
		cursor: pointer;
		padding: 8px;
	}

	.hamburger-menu div {
		width: 25px;
		height: 3px;
		background-color: var(--color-theme-2);
		margin: 4px 0;
	}

	.slideout-menu {
		position: fixed;
		top: 48px; /* Adjust this based on your header height */
		bottom: 0;
		left: 0;
		width: 250px;
		background-color: var(--color-bg-2);
		padding: 1rem;
		height: 100%;
		z-index: 1000;
	}

	.slideout-menu a {
		padding: 0;
		margin: 0;
		display: block;
		height: auto;
		padding: 0.5rem 0;
		display: block;
	}

</style>

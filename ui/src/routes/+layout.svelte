<script>
	import './styles.css';
	import { page } from '$app/stores';
	import github from '$lib/images/github.svg';
	import { fly } from 'svelte/transition';

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
			  <div class="line top {isMenuOpen ? 'active' : ''}"></div>
			  <div class="line middle {isMenuOpen ? 'active' : ''}"></div>
			  <div class="line bottom {isMenuOpen ? 'active' : ''}"></div>
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
				<li aria-current={$page.url.pathname === '/chat' ? 'page' : undefined}>
					<a href="/chat-with-file">Chat</a>
				</li>
			</ul>
			<svg viewBox="0 0 2 3" aria-hidden="true">
				<path d="M0,0 L0,3 C0.5,3 0.5,3 1,2 L2,0 Z" />
			</svg>
		</nav>

		<div class="corner">
			<a href="https://github.com/sudomonikers/DocChatFullStack" target="_blank">
				<img src={github} alt="GitHub" style="height:48px;width:48px;"/>
			</a>
		</div>
	</header>

	<main>
		{#if isMenuOpen}
			<div>
				<div class="slideout-menu" transition:fly={{ y: 200, duration: 1000 }}>
					<h1>About</h1>
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

  .line {
    width: 25px;
    height: 3px;
    background-color: var(--color-theme-2);
    margin: 4px 0;
    transition: transform 0.3s ease; /* Add a transition for smooth animation */
  }

  /* Initial state of the X shape */
  .line.middle {
    transform-origin: center;
    transform: scaleY(1); /* Initially, show the middle line */
  }

  .line.top.active {
    transform: translateY(11px) rotate(45deg); /* Rotate the top line to form an X */
  }

  .line.middle.active {
    transform: scaleY(0); /* Hide the middle line when active */
  }

  .line.bottom.active {
    transform: translateY(-11px) rotate(-45deg); /* Rotate the bottom line to form an X */
  }

	.slideout-menu {
		box-sizing: border-box;
		position: fixed;
		top: 15%;
		bottom: 0;
		left: 0;
		width: 100vw;
		height: 85%;
		box-shadow: 0px 20px 50px 30px var(--color-theme-3);
		overflow-y: scroll;
		z-index: 1000;
		text-align: center;
		background-image: linear-gradient(
			to top,
			var(--color-theme-1) 50%, /* Solid color (e.g., blue) for the bottom 80% */
			75%,
			var(--color-theme-3) 100%

		);
	}

	.slideout-menu h1 {
		color: var(--color-theme-2);
	}

</style>

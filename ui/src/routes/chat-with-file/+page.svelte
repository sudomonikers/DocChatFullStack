<script>
	import { onMount } from 'svelte';
	import { BASE_API } from '$lib/environment';
	import '../styles.css';

	onMount(() => {
		getUploadedDocuments();
	});
	let originalDocuments = [];
	let documents = [];

	function getUploadedDocuments() {
		fetch(`${BASE_API}/all-document-titles`)
			.then((response) => response.json())
			.then((data) => {
				originalDocuments = data.sort();
				documents = [...originalDocuments];
			});
	}

	function handleSearch(event) {
		const searchTerm = event.target.value.toLowerCase();
		documents = originalDocuments.filter((document) => document.toLowerCase().includes(searchTerm));
	}
</script>

<div class="container">
	<h1>Chat With Document:</h1>
	<input type="text" placeholder="Filter Documents..." on:input={handleSearch} />
	{#each documents as document}
		<a href="/chat-with-file/{document}">{document}</a>
	{/each}
</div>

<style>
	.container {
		width: 66%;
		left: 50%;
		transform: translateX(-50%);
		position: relative;
		margin-top: 20px;
		padding-bottom: 15px;
		border: 2px solid var(--color-theme-2);
		height: auto;
		text-align: center;
		background-color: var(--color-theme-1);
	}

	h1 {
		color: var(--color-theme-2);
	}

	input {
		color: var(--color-theme-2);
		border: 2px solid var(--color-theme-3);
		transition: 500ms;
		padding: 10px;
		color: var(--color-theme-1);
	}

	input:focus {
		outline: none;
		border: 4px solid var(--color-theme-3);
	}

	a {
		padding: 0;
		margin: 0;
		display: block;
		height: auto;
		padding: 0.5rem 0;
		display: block;
		font-size: 26px;
		color: var(--color-theme-3);
	}

	a:hover {
		text-decoration: none;
		color: var(--color-theme-2);
	}
</style>

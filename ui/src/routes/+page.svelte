<script>
	import Terminal from '$lib/components/Terminal.svelte';
  </script>
  
  <svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
  </svelte:head>
  
  <style>
	/* Styles for the parent section */
	section {
	  width: 100%;
	  height: calc(100vh - 48px);
	  display: flex;
	  justify-content: center;
	  align-items: center;
	}
  
	/* Optional styles for the terminal container */
	.terminal {
	  width: 80%; /* Adjust the width of the terminal */
	  max-width: 800px; /* Set a maximum width for larger screens */
	}
  </style>
  
  <section>
	<div class="terminal">
		<Terminal />
	</div>
  </section>
  
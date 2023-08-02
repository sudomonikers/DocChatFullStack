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
	  padding: 15px;
	  box-sizing: border-box;
	  height: calc(100vh - 48px);
	  display: flex;
	  flex-direction: column;
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
	<h1>Chat With Documents</h1>
	<p>This is a developmental preview site to show the capabilities of using Retrieval Augmented Generation (RAG) to understand and query documents. You can click the <a href="/upload">Upload</a> button to upload any type of file. It will then be sent to an api that processes and vectorizes that document. Once your document is uploaded, you can click the hamburger menu on the top left of the nav bar to choose a document to interact with. There you will be taken to a chat screen where you can chat with a LLM specifically about that document. Try it now to see the power! If you have any questions on how to use this site, or why it could be useful, try interacting with the 'terminal' below. It has been designed specifically to inform users of how to use this site.</p>
	<div class="terminal">
		<Terminal />
	</div>
	<p>If you are interested, click the github logo in the top right of the nav to be taken to the repo for this site. While the backend you are currently interacting with is using Openai's gpt-3.5-turbo and Pinecone for a vector databse (the OP stack), I am currently working on getting this working using open source models and vector databases you can host yourself. There are real security concerns (and costs) of using these closed source premium services (not to mention a lack of control over how things will perform).</p>
  </section>
  
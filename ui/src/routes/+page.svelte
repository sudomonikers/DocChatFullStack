<script>
	export const prerender = false;
	export const ssr = false;
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h1>Chat With Documents</h1>
	<p>
		This is a developmental preview site to show the capabilities of using Retrieval Augmented
		Generation (RAG) to understand and query documents. You can click the <a href="/upload"
			>Upload</a
		>
		button to upload any type of file. It will then be sent to an api that processes and vectorizes
		that document. Once your document is uploaded, you can click the <a href="/chat">Chat</a> nav element
		to choose a document to interact with. There you will be taken to a chat screen where you can chat
		with a LLM specifically about that document. Try it now to see the power! If you have any questions
		on how to use this site, or why it could be useful, try interacting with the 'terminal' by clicking
		the hamburger menu in the top left corner. It has been designed specifically to inform users of how
		to use this site.
	</p>
	<br />
	<p>
		If you are interested, click the github logo in the top right of the nav to be taken to the repo
		for this site. While the backend you are currently interacting with is using Openai's
		gpt-3.5-turbo and Pinecone for a vector databse (the OP stack), I am currently working on
		getting this working using open source models and vector databases you can host yourself. There
		are real security concerns (and costs) of using these closed source premium services (not to
		mention a lack of control over how things will perform), and I am sure many people would be
		interested in using specific models that they fine tune or are more suited to their use case.
	</p>
</section>

<style>
	/* Styles for the parent section */
	section {
		padding: 15px;
		box-sizing: border-box;
	}
</style>

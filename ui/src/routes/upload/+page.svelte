<script>
	import { BASE_API } from '$lib/environment';
	import Loading from '$lib/components/Loading.svelte';
	import FileUploader from '$lib/components/FileUploader.svelte';
	import '../styles.css';

	let selectedFiles = [];
	let loading = false;

	async function uploadFiles() {
		const formData = new FormData();
		const files = Array.from(selectedFiles);
		files.forEach((file) => formData.append('files', file));

		try {
			loading = true;
			await fetch(`${BASE_API}/uploadfile`, {
				method: 'POST',
				body: formData
			});
			loading = false;
			selectedFiles = []; // Clear the selected files after successful upload
		} catch (error) {
			loading = false;
			console.error('Error:', error);
		}
	}
	$: fileMessage =
		selectedFiles.length > 1
			? 'Multiple Files selected'
			: selectedFiles.length === 1
			? 'One File Selected'
			: 'No files selected';
</script>

<Loading {loading}>
	<div class="file-upload-container">
		<div class="file-upload">
			<FileUploader bind:selectedFiles />
			<span>{fileMessage}</span>
			{#each selectedFiles as file}
				<span>{file.name}</span>
			{/each}
			<button 
				class="button" 
				on:click={uploadFiles} 
				disabled={selectedFiles.length === 0}>
			Upload
			</button>
		</div>
	</div>
</Loading>

<style>
	.file-upload-container {
		position: relative;
		top: 0;
		left: 0;
		width: 100%;
		height: calc(100vh - 48px);
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.file-upload {
		width: 80%;
		max-width: 600px;
		padding: 20px;
		background-color: white;
		border-radius: 8px;
		box-shadow: 0 20px 80px rgba(0, 0, 0, 0.7);
		display: flex;
		height: 60%;
		flex-direction: column;
		align-items: center;
	}
	span {
		padding: 5px;
	}
</style>

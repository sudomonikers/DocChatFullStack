<script>
	import { BASE_API } from '$lib/environment';
	import Loading from '$lib/components/Loading.svelte';
    import '../styles.css';
	let selectedFiles = [];
	let loading = false;
	$: fileNames =
		'Files: ' +
		Array.from(selectedFiles)
			.map((file) => file.name)
			.join(', ');

	async function uploadFiles() {
		const formData = new FormData();
		const files = Array.from(selectedFiles);
		files.forEach((file) => formData.append('files', file));

		try {
			loading = true;
			const response = await fetch(`${BASE_API}/uploadfile`, {
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
</script>

<Loading {loading}>
	<div class="file-upload-container">
		<div class="file-upload">
			<label for="file-input" class="upload-btn">Choose Files</label>
			<input id="file-input" type="file" multiple bind:files={selectedFiles} />
            <span id="file-names">{selectedFiles.length > 0 ? fileNames : 'No files selected'}</span>
            <ul>
                {#each selectedFiles as file}
                    <li>{file.name}</li>
                {/each}
            </ul>
			<button class="button" on:click={uploadFiles} disabled={selectedFiles.length === 0}>Upload</button>
		</div>
	</div>
</Loading>

<style>
	.file-upload-container {
		/* Set the container to take up the whole screen */
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
		/* Set the dimensions and styling for the file-upload div */
		width: 80%; /* Adjust as needed */
		max-width: 600px; /* Set a maximum width */
		padding: 20px;
		background-color: white;
		border-radius: 8px;
		box-shadow: 0 20px 80px rgba(0, 0, 0, 0.7);
		display: flex;
		height: 60%;
		flex-direction: column;
		align-items: center;
	}

	.upload-btn {
		background-color: #4caf50;
		color: white;
		padding: 10px 20px;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	.upload-btn:hover {
		background-color: #45a049;
	}

	#file-input {
		display: none;
	}

	#file-names {
		margin-top: 10px;
		font-size: 16px;
		color: #777;
	}
</style>

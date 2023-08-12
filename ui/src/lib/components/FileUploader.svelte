<script>
	export let selectedFiles = [];

	let isDragging = false;
	let inputElement;

	function handleFileSelect(event) {
		const files = event.target.files;
		selectedFiles = [...selectedFiles, ...files];
		console.log(selectedFiles);
	}

	function handleDrop(event) {
		event.preventDefault();
		isDragging = false;
		const files = event.dataTransfer.files;
		selectedFiles = [...selectedFiles, ...files];
		console.log(selectedFiles);
	}

	function handleDragOver(event) {
		event.preventDefault();
		isDragging = true;
	}

	function handleDragLeave() {
		isDragging = false;
	}

	function handleClick() {
		inputElement.click();
	}

	function handleKeyDown(event) {
		// Trigger the handleClick function on "Enter" key press (key code 13) or "Space" key press (key code 32)
		if (event.keyCode === 13 || event.keyCode === 32) {
			handleClick();
		}
	}
</script>

<div
	class="file-uploader {isDragging ? 'dragging' : ''}"
	on:drop={handleDrop}
	on:dragover={handleDragOver}
	on:dragleave={handleDragLeave}
	role="button"
	aria-dropeffect="copy"
	tabindex="0"
	on:click={handleClick}
	on:keydown={handleKeyDown}
>
	<input
		type="file"
		style="display: none;"
		on:change={handleFileSelect}
		bind:this={inputElement}
		multiple
	/>
	<span>Drag and drop files here or click to select</span>
</div>

<style>
	.file-uploader {
		border: 2px dashed #ccc;
		padding: 1rem;
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;
	}

	.dragging {
		border-color: #007bff;
	}
</style>

<script>
    import { BASE_API } from '$lib/environment';
    import Loading from '$lib/components/Loading.svelte';
    let selectedFiles = [];
    let loading = false;
    $: fileNames = 'Files: ' + Array.from(selectedFiles).map((file) => file.name).join(", "); 

    async function uploadFiles() {
        const formData = new FormData();
        const files = Array.from(selectedFiles);
        files.forEach(file => formData.append("files", file));

        try {
            loading = true;
            const response = await fetch(`${BASE_API}/uploadfile`, {
                method: "POST",
                body: formData,
            });
            console.log(response)
            loading = false;
            selectedFiles = []; // Clear the selected files after successful upload
        } catch (error) {
            loading = false;
            console.error("Error:", error);
        }
    }
</script>
<Loading {loading}>
    <div class="file-upload">
        <label for="file-input" class="upload-btn">Choose Files</label>
        <input id="file-input" type="file" multiple bind:files={selectedFiles}>
        <span id="file-names">{selectedFiles.length > 0 ? fileNames : 'No files selected'}</span>
        <button on:click={uploadFiles} disabled={selectedFiles.length === 0}>Upload</button>
    </div>
</Loading>


<style>
    .file-upload {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .upload-btn {
        background-color: #4CAF50;
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
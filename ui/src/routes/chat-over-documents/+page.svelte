<script lang="ts">
    let selectedFiles: any = [];
    $: fileNames = 'Files: ' + Array.from(selectedFiles).map((file: any) => file.name).join(", "); 

    async function uploadFiles() {
        const formData = new FormData();
        const files = Array.from(selectedFiles);
        files.forEach(file => formData.append("files", file as any));

        try {
        const response = await fetch("http://localhost:8000/uploadfile", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            alert("Files uploaded successfully!");
            selectedFiles = []; // Clear the selected files after successful upload
        } else {
            alert("Failed to upload files. Please try again.");
        }
        } catch (error) {
        console.error("Error:", error);
        }
    }
</script>

<div class="file-upload">
    <label for="file-input" class="upload-btn">Choose Files</label>
    <input id="file-input" type="file" multiple bind:files={selectedFiles}>
    <span id="file-names">{selectedFiles.length > 0 ? fileNames : 'No files selected'}</span>
    <button on:click={uploadFiles} disabled={selectedFiles.length === 0}>Upload</button>

</div>

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
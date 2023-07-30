<script>
	export let data;
	import { BASE_API } from '$lib/environment';
	import '../../../routes/styles.css';

	//we need to store the display messages separately from the history
	let messages = [];
	let history = [];
	let newMessage = '';
	let messageInFlight = false;

	function adjustTextareaRows(event) {
		const textarea = event.target;
		const minRows = 3; // Set a minimum number of rows
		const maxRows = 15; // Set a maximum number of rows
		const lineHeight = 24; // Set the line-height value in pixels (adjust as needed)
		const scrollHeight = textarea.scrollHeight;
		const currentRows = Math.floor(scrollHeight / lineHeight);
		const computedRows =
			currentRows < minRows ? minRows : currentRows > maxRows ? maxRows : currentRows;
		const newHeight = `${computedRows * lineHeight}px`;
		textarea.style.height = newHeight;
	}

	async function getFile() {
		try {
			const response = await fetch(`${BASE_API}/document/${data.file}`, {
				method: 'GET',
				headers: {
					// Add any necessary headers, such as authentication tokens
				}
			});

			const blob = await response.blob();
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = data.file;
			a.click();
			URL.revokeObjectURL(url);
		} catch (error) {
			console.error('Error while downloading File:', error);
		}
	}

	async function sendMessage() {
		const messageText = newMessage.trim();
		if (messageText !== '') {
			messages.push({ content: messageText, role: 'user' });
			messages = messages;
			newMessage = '';
		}
		messageInFlight = true;

		try {
			const response = await fetch(`${BASE_API}/chat`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					query: messageText,
					document: data.file,
					history: history.length > 0 ? history : messages
				})
			});
			const stream = response.body;

			const reader = stream.getReader();
			let result = '';
			let done = false;

			while (!done) {
				const { value, done: isDone } = await reader.read();
				if (isDone) {
					done = true;
				} else {
					result += new TextDecoder().decode(value);
				}
			}
			const parsedResult = JSON.parse(result);
			messages.push(parsedResult[parsedResult.length - 1]);
			messages = messages;
			history = parsedResult;
			messageInFlight = false;
		} catch (error) {
			messageInFlight = false;
			console.error('Error while sending message:', error);
		}
	}
</script>
<h1>Chatting With <button class="download-button" on:click={getFile}>{data.file}</button></h1>
<div class="chatbox">
	<div class="message-box">
		{#each messages as message}
			<div class="message">
				<span>{message.role}</span>
				<span>{message.content}</span>
			</div>
			<hr />
		{/each}
		{#if true}
			<div class="message">
				<span>assistant</span>
				<div class="dots"></div>
			</div>
		{/if}
	</div>
	<div class="textarea-container">
		<textarea
			bind:value={newMessage}
			placeholder="Type your message..."
			rows="3"
			on:input={adjustTextareaRows}
		/>
		<button disabled={messageInFlight} class="send-button" on:click={sendMessage}>Send</button>
	</div>
</div>

<style>
	.download-button {
		background-color: transparent;
		border: none;
		padding: 0;
		margin: 0;
		font: inherit;
		color: var(--color-theme-2);
		cursor: pointer;
		transition: 500ms;
	}

	.download-button:hover {
		color: var(--color-theme-3);
	}

	.chatbox {
		width: 80%;
		left: 10%;
		height: 100%;
		position: relative;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.message-box {
		background-color: var(--color-theme-1);
		padding: 16px;
		color: var(--color-theme-2);
		width: 100%;
		left: 10%;
		box-sizing: border-box;
	}

	.message {
		display: flex;
		align-items: center;
	}

	.message span:first-child {
		flex-basis: 10%; /* Set the first span to take up 10% of the space */
		flex-shrink: 0; /* Prevent the first span from shrinking */
	}

	.message span:last-child {
		flex: 1; /* The second span will take up the remaining space */
	}

	/* Optional: Add spacing between the spans */
	.message span {
		margin-right: 10px;
	}

	.textarea-container {
		position: fixed;
		bottom: 0;
		width: 80%;
		left: 10%;
	}

	.textarea-container textarea {
		border: 5px solid var(--color-theme-3);
		background-color: var(--color-theme-1);
		color: var(--color-theme-2);
		line-height: 24px;
		border-radius: 4px;
		padding: 8px;
		resize: none;
		transition: height 0.2s ease;
		overflow-y: hidden;
		width: 100%;
		box-sizing: border-box;
		bottom: 0;
	}

	.textarea-container textarea:focus {
		outline: none;
	}

	.send-button {
		position: absolute;
		bottom: 16px;
		right: 12px;
		padding: 8px 16px;
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	.textarea-container button {
		margin-left: 8px;
		padding: 8px 16px;
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	@keyframes changeLetter {
		0% {
			content: '';
		}
		33% {
			content: '.';
		}
		66% {
			content: '..';
		}
		100% {
			content: '...';
		}
	}
	.dots {

		&:after {
			animation: changeLetter 4s linear infinite;
			content: "";
		}
	}
</style>

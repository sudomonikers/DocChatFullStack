<script>
	import { BASE_API } from '$lib/environment';
	import { afterUpdate } from 'svelte';

	let prompt = 'UI-Control@Help ~ %';
	let currentCommand = '';
	let commandHistory = [];
	let inputElement;
	let messageInFlight = false;

	afterUpdate(() => {
		scrollTerminalToBottom();
	});

	function handleInput(event) {
		if (event.key === 'Enter') {
			commandHistory.push({ command: currentCommand, response: '' });
			commandHistory = commandHistory;
			sendMessage();
		}
	}

	function scrollTerminalToBottom() {
		const terminalContent = document.querySelector('.terminal-content');
		terminalContent.scrollTop = terminalContent.scrollHeight;
	}

	function keyboardInteraction(event) {
		if (event.key === 'Enter') {
			focusInput();
		}
	}

	function focusInput() {
		inputElement.focus();
	}

	async function sendMessage() {
		try {
			messageInFlight = true;
			const query = currentCommand;
			currentCommand = '';
			const response = await fetch(`${BASE_API}/control-ui`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					query: query
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
			if (parsedResult.response === 'wowTheUser') {
				wowTheUser();
				commandHistory[commandHistory.length - 1].response = 'Haha get rickrolled!';
			} else {
				commandHistory[commandHistory.length - 1].response = parsedResult;
			}
			commandHistory = commandHistory;

			scrollTerminalToBottom();

			messageInFlight = false;
		} catch (error) {
			messageInFlight = false;
			console.error('Error while sending message:', error);
		}
	}

	function wowTheUser() {
		const existingVideoContainer = document.getElementById('videoContainer');
		if (existingVideoContainer) {
			return; // Prevent rendering if the container already exists
		}

		const videoContainer = document.createElement('div');
		videoContainer.id = 'videoContainer';
		videoContainer.style.position = 'fixed';
		videoContainer.style.top = '0';
		videoContainer.style.left = '0';
		videoContainer.style.width = '100%';
		videoContainer.style.height = '100%';
		videoContainer.style.display = 'flex';
		videoContainer.style.justifyContent = 'center';
		videoContainer.style.alignItems = 'center';
		videoContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
		videoContainer.style.zIndex = '9999';

		// Replace the video ID with the actual YouTube video ID
		const videoId = 'dQw4w9WgXcQ';

		const iframe = document.createElement('iframe');
		iframe.width = '560';
		iframe.height = '315';
		iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
		iframe.frameborder = '0';
		iframe.allow =
			'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
		iframe.allowFullscreen = true;

		videoContainer.appendChild(iframe);
		document.body.appendChild(videoContainer);

		// Schedule the removal of the video container after 15 seconds
		setTimeout(() => {
			document.body.removeChild(videoContainer);
		}, 15000); // 15 seconds in milliseconds
	}
</script>

<div
	class="terminal"
	role="button"
	tabindex="0"
	on:click={focusInput}
	on:keydown={keyboardInteraction}
>
	<div class="terminal-header">Website Control</div>

	<div class="terminal-content" role="textbox" tabindex="0" on:keydown={handleInput}>
		<div class="command-line">
			<span class="prompt">{prompt}&nbsp;</span><span
				>Greetings. This terminal is meant to do a couple things. (Also note it has no memory of the
				conversation, unlike the chatbot in the 'chat' page)</span
			>
			<ol>
				<li>Tell you how to interact and use this website if you have questions.</li>
				<li>
					Showcase the power and potential of AI powered function calls. Try asking the terminal to
					do a basic math equation. Something with two numbers and basic arithmetic like adding,
					subtracting, multiplying, or dividing. The AI will get it right every single time because
					it has been given a 'logic' center in the form of a code library to call. Fleshing out
					code libraries for AI's to call solves the problem of hallucination, and is the future of
					how humans and machines will interact.
				</li>
				<li>
					Show how AI can be used to do things alongside the user on the UI. Try asking it to show
					you a video.
				</li>
			</ol>
			{#each commandHistory as command, index}
				<span class="prompt">{prompt}&nbsp;</span>
				<span class="command-text">{command.command}</span>
				<br />
				{#if messageInFlight && index === commandHistory.length - 1}
					<div class="dots">.</div>
				{:else}
					<span class="response">{command.response.response}</span>
				{/if}
			{/each}
		</div>

		<div class="command-line">
			<span class="prompt">{prompt}&nbsp;</span>
			<input
				disabled={messageInFlight}
				class="input-field"
				bind:value={currentCommand}
				bind:this={inputElement}
			/>
		</div>
	</div>
</div>

<style>
	.terminal {
		border: 1px solid #ccc;
		border-radius: 4px;
		background-color: black;
		color: white;
		font-family: monospace;
		padding: 8px;
		overflow: hidden;
		text-align: left;
	}

	.terminal-header {
		padding: 8px;
		background-color: #333;
		color: #fff;
		font-weight: bold;
		font-size: 1.2rem;
	}

	.terminal-content {
		height: 300px;
		overflow-y: auto;
		position: relative;
	}

	.command-line {
		position: relative;
		margin-bottom: 4px;
	}

	.prompt {
		color: lime;
		margin-right: 4px;
	}

	.response {
		width: 100%;
	}

	.command-text {
		display: inline;
	}

	.input-field {
		display: inline;
		width: calc(100% - 180px);
		background-color: transparent;
		color: #fff;
		border: none;
	}

	.input-field:focus {
		outline: none;
	}

	.terminal-content:focus {
		outline: none;
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
		color: transparent;
	}
	.dots:before {
		color: #fff;
		animation: changeLetter 4s linear infinite;
		content: '';
	}
</style>

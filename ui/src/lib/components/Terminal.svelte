<script>
	export let prompt = '$'; // Customize the prompt text here

	let commandHistory = [];
	let currentCommand = '';
	let output = '';

	function handleInput(event) {
		if (event.key === 'Enter') {
			output += `${prompt} ${currentCommand}\n`;
			commandHistory.push(currentCommand);
			// Implement your logic to handle the entered command here...
			// For this example, let's just echo back the command.
			output += `${currentCommand}\n\n`;

			currentCommand = '';
			scrollTerminalToBottom();
		}
	}

	function scrollTerminalToBottom() {
		const terminalContent = document.querySelector('.terminal-content');
		terminalContent.scrollTop = terminalContent.scrollHeight;
	}
</script>

<div class="terminal">
	<div class="terminal-header">Website Control</div>

    <div class="terminal-content" contenteditable="true" on:input={handleInput}>
		<span class="output">{output}</span>
		<span class="prompt">{prompt}</span>
		<span>{currentCommand}</span>
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
	}

	.terminal-content:focus {
		outline: none;
	}

	.prompt {
		display: inline;
		color: lime;
		margin-right: 4px;
	}

	.output {
		white-space: pre-wrap;
	}
</style>

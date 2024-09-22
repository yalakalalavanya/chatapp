const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');

// Function to send a message
function sendMessage() {
    const message = messageInput.value;
    if (message.trim() === '') return;

    // Add user's message to the chat box
    addMessage('You', message, 'user');
    
    // Clear the input field
    messageInput.value = '';

    // Send the message to the backend
    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Add bot's response to the chat box
        addMessage('Bot', data.response, 'bot');
    });
}

// Function to add a message to the chat box
function addMessage(user, message, className) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', className);
    messageElement.textContent = `${user}: ${message}`;
    chatBox.appendChild(messageElement);

    // Auto-scroll to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Fetch chat history on page load
window.onload = function() {
    fetch('/get_chat_history')
    .then(response => response.json())
    .then(history => {
        history.forEach(msg => {
            addMessage(msg.user, msg.message, msg.user === 'You' ? 'user' : 'bot');
        });
    });
}

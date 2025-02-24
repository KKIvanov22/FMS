document.addEventListener('DOMContentLoaded', () => {
    let currentChatId: string | null = null;
    let fetchMessagesInterval: ReturnType<typeof setInterval> | null = null;

    document.getElementById('createChatButton')?.addEventListener('click', () => {
        document.getElementById('chatModal')?.classList.remove('hidden');
        fetchChats();
    });

    document.getElementById('closeChatModal')?.addEventListener('click', () => {
        document.getElementById('chatModal')?.classList.add('hidden');
    });

    document.getElementById('submitChat')?.addEventListener('click', () => {
        const selectedParticipants = Array.from(document.querySelectorAll('#selectedParticipants li')).map(li => (li as HTMLElement).dataset.uid || '');
        const userId = getUserIdFromCookies();
        if (userId) {
            selectedParticipants.push(userId);
        }
        createChat(selectedParticipants);
    });

    document.getElementById('chatParticipants')?.addEventListener('input', () => {
        const input = document.getElementById('chatParticipants') as HTMLInputElement;
        fetchParticipants(input.value);
    });

    document.getElementById('closeIndividualChatModal')?.addEventListener('click', () => {
        document.getElementById('individualChatModal')?.classList.add('hidden');
        if (fetchMessagesInterval) {
            clearInterval(fetchMessagesInterval);
        }
    });

    setupSendMessageButton();

    function setupSendMessageButton(): void {
        const sendMessageButton = document.getElementById('sendMessageButton');
        if (sendMessageButton) {
            sendMessageButton.addEventListener('click', () => {
                const messageInput = document.getElementById('newMessage') as HTMLTextAreaElement;
                const message = messageInput.value;
                if (currentChatId && message) {
                    sendMessage(currentChatId, message);
                    messageInput.value = '';
                }
            });
        }
    }

    function fetchParticipants(query: string): void {
        fetch(`http://localhost:5000/get_users?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const suggestions = document.getElementById('participantSuggestions');
            if (suggestions) {
                suggestions.innerHTML = '';
                data.forEach((user: { uid: string, Username: string }) => {
                    const li = document.createElement('li');
                    li.textContent = user.Username;
                    li.classList.add('cursor-pointer', 'p-2', 'hover:bg-gray-700');
                    li.addEventListener('click', () => addParticipant(user.uid, user.Username));
                    suggestions.appendChild(li);
                });
            }
        })
        .catch(error => alert('Error fetching participants: ' + error));
    }

    function addParticipant(uid: string, username: string): void {
        const selectedParticipants = document.getElementById('selectedParticipants');
        if (selectedParticipants) {
            const li = document.createElement('li');
            li.textContent = username;
            li.dataset.uid = uid;
            li.classList.add('p-2', 'bg-gray-600', 'rounded', 'mt-2');
            selectedParticipants.appendChild(li);
        }
        const input = document.getElementById('chatParticipants') as HTMLInputElement;
        input.value = '';
        const suggestions = document.getElementById('participantSuggestions');
        if (suggestions) {
            suggestions.innerHTML = '';
        }
    }

    function createChat(participants: string[]): void {
        fetch('http://localhost:5000/create_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ participants })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                fetchChats();
            } else {
                alert(data.error);
            }
        })
        .catch(error => alert('Error creating chat: ' + error));
    }

    function fetchChats(): void {
        fetch('http://localhost:5000/get_chats')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const chatList = document.getElementById('chatList');
            if (chatList) {
                chatList.innerHTML = '';
                for (const chatId in data.chats) {
                    const li = document.createElement('li');
                    const participants = data.chats[chatId].Participants.map((uid: string) => {
                        if (data.users) {
                            const user = data.users.find((user: { uid: string, Username: string }) => user.uid === uid);
                            return user ? user.Username : uid;
                        } else {
                            return uid;
                        }
                    }).join(', ');
                    li.textContent = `Chat ID: ${chatId}, Participants: ${participants}`;
                    li.classList.add('cursor-pointer', 'p-2', 'hover:bg-gray-700');
                    li.addEventListener('click', () => openChat(chatId, participants));
                    chatList.appendChild(li);
                }
            }
        })
        .catch(error => alert('Error fetching chats: ' + error));
    }

    function openChat(chatId: string, participants: string): void {
        currentChatId = chatId;
        document.getElementById('individualChatModal')?.classList.remove('hidden');
        document.getElementById('chatTitle')!.textContent = `Chat with ${participants}`;
        fetchMessages();
        if (fetchMessagesInterval) {
            clearInterval(fetchMessagesInterval);
        }
        fetchMessagesInterval = setInterval(fetchMessages, 3000);
    }

    function fetchMessages(): void {
        if (!currentChatId) return;
        fetch(`http://localhost:5000/get_messages?chatId=${currentChatId}`)
        .then(response => response.json())
        .then(data => {
            const chatMessages = document.getElementById('chatMessages');
            if (chatMessages) {
                chatMessages.innerHTML = '';
                data.forEach((message: { message: string, sender: string, time: string }) => {
                    const li = document.createElement('li');
                    li.textContent = `${message.time} - ${message.sender}: ${message.message}`;
                    chatMessages.appendChild(li);
                });
            }
        })
        .catch(error => alert('Error fetching messages: ' + error));
    }

    function sendMessage(chatId: string, message: string): void {
        fetch('http://localhost:5000/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ chatId, message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                fetchMessages();
            } else {
                alert(data.error);
            }
        })
        .catch(error => alert('Error sending message: ' + error));
    }

    function getUserIdFromCookies(): string | null {
        const name = 'user_id=';
        const decodedCookie = decodeURIComponent(document.cookie);
        const ca = decodedCookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return null;
    }
});
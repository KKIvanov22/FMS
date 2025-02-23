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
    .catch(error => console.error('Error:', error));
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
    .catch(error => console.error('Error:', error));
}

function fetchChats(): void {
    fetch('http://localhost:5000/get_chats')
    .then(response => response.json())
    .then(data => {
        console.log('Fetched chats:', data); // Add this line
        const chatList = document.getElementById('chatList');
        if (chatList) {
            chatList.innerHTML = '';
            for (const chatId in data.chats) {
                const li = document.createElement('li');
                const participants = data.chats[chatId].Participants.map((uid: string) => {
                    const user = data.users.find((user: { uid: string, Username: string }) => user.uid === uid);
                    return user ? user.Username : uid;
                }).join(', ');
                li.textContent = `Chat ID: ${chatId}, Participants: ${participants}`;
                chatList.appendChild(li);
            }
        }
    })
    .catch(error => console.error('Error:', error));
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
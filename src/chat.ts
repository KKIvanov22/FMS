document.getElementById('createChatButton')?.addEventListener('click', () => {
    document.getElementById('chatModal')?.classList.remove('hidden');
    fetchChats();
});

document.getElementById('closeChatModal')?.addEventListener('click', () => {
    document.getElementById('chatModal')?.classList.add('hidden');
});

document.getElementById('submitChat')?.addEventListener('click', () => {
    const selectedParticipants = Array.from(document.querySelectorAll('#selectedParticipants li')).map(li => li.textContent || '');
    const username = getUsernameFromCookies();
    if (username) {
        selectedParticipants.push(username);
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
            data.forEach((user: { username: string }) => {
                const li = document.createElement('li');
                li.textContent = user.username;
                li.classList.add('cursor-pointer', 'p-2', 'hover:bg-gray-700');
                li.addEventListener('click', () => addParticipant(user.username));
                suggestions.appendChild(li);
            });
        }
    })
    .catch(error => console.error('Error:', error));
}

function addParticipant(username: string): void {
    const selectedParticipants = document.getElementById('selectedParticipants');
    if (selectedParticipants) {
        const li = document.createElement('li');
        li.textContent = username;
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
        const chatList = document.getElementById('chatList');
        if (chatList) {
            chatList.innerHTML = '';
            for (const chatId in data) {
                const li = document.createElement('li');
                li.textContent = `Chat ID: ${chatId}, Participants: ${data[chatId].Participants.join(', ')}`;
                chatList.appendChild(li);
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

function getUsernameFromCookies(): string | null {
    const name = 'username=';
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
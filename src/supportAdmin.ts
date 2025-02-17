document.addEventListener('DOMContentLoaded', () => {
    const supportListContainer = document.getElementById('support-list-container');
    const updateSupportPopup = document.getElementById('update-support-popup');
    const supportDescription = document.getElementById('support-description');
    const supportDoneCheckbox = document.getElementById('support-done') as HTMLInputElement;
    const cancelSupportUpdateButton = document.getElementById('cancel-support-update');
    const confirmSupportUpdateButton = document.getElementById('confirm-support-update');

    let currentSupportId: string | null = null;

    async function fetchSupportData() {
        try {
            const response = await fetch('http://localhost:5000/get_support');
            const data = await response.json();
            if (supportListContainer) {
                supportListContainer.innerHTML = '';
                for (const [id, support] of Object.entries(data)) {
                    const supportItem = document.createElement('div');
                    supportItem.className = 'p-4 bg-gray-800 rounded cursor-pointer hover:bg-gray-700';
                    supportItem.textContent = (support as { Name: string }).Name;
                    supportItem.addEventListener('click', () => {
                        currentSupportId = id;
                        if (supportDescription) {
                            supportDescription.textContent = (support as { Description: string }).Description;
                        }
                        supportDoneCheckbox.checked = (support as { Done: boolean }).Done;
                        if (updateSupportPopup) {
                            updateSupportPopup.classList.remove('hidden');
                        }
                    });
                    supportListContainer.appendChild(supportItem);
                }
            }
        } catch (error) {
            console.error('Error fetching support requests:', error);
        }
    }

    fetchSupportData();

    if (cancelSupportUpdateButton) {
        cancelSupportUpdateButton.addEventListener('click', () => {
            if (updateSupportPopup) {
                updateSupportPopup.classList.add('hidden');
            }
        });
    }

    if (confirmSupportUpdateButton) {
        confirmSupportUpdateButton.addEventListener('click', () => {
            if (currentSupportId) {
                const updatedSupport = {
                    id: currentSupportId,
                    done: supportDoneCheckbox.checked
                };

                fetch('http://localhost:5000/update_support', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(updatedSupport)
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Support request updated:', data);
                    if (updateSupportPopup) {
                        updateSupportPopup.classList.add('hidden');
                    }
                    location.reload();
                })
                .catch(error => console.error('Error updating support request:', error));
            }
        });
    }

    setInterval(fetchSupportData, 3600000);
});
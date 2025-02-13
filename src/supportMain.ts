const supportLink = document.getElementById('supportLink');
const supportModal = document.getElementById('supportModal');
const closeSupportModal = document.getElementById('closeSupportModal');
const submitSupport = document.getElementById('submitSupport');

if (supportLink && supportModal && closeSupportModal && submitSupport) {
    supportLink.addEventListener('click', function() {
        supportModal.classList.remove('hidden');
    });

    closeSupportModal.addEventListener('click', function() {
        supportModal.classList.add('hidden');
    });

    submitSupport.addEventListener('click', function() {
        const nameInput = document.getElementById('supportName') as HTMLInputElement;
        const descriptionInput = document.getElementById('supportDescription') as HTMLTextAreaElement;

        if (nameInput && descriptionInput) {
            const name = nameInput.value;
            const description = descriptionInput.value;

            fetch('http://localhost:5000/add_support', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, description, done: false })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert('Support request sent successfully');
                    supportModal.classList.add('hidden');
                } else {
                    alert('Error sending support request');
                }
            });
        }
    });
}
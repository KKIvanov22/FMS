document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('http://localhost:5000/user');
        if (response.ok) {
            const userData = await response.json();
            const usernameElement = document.getElementById('username');
            const companyElement = document.getElementById('company');

            if (usernameElement && companyElement) {
                usernameElement.textContent = userData.username;
                companyElement.textContent = userData.company;
            }
        } else {
            console.error('Failed to fetch user data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
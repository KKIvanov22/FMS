document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('http://localhost:5000/user', {
            credentials: 'include'
        });
        if (response.ok) {
            const userData = await response.json();
            const usernameElement = document.getElementById('username');
            const companyElement = document.getElementById('company');
            const updateCompanyButton = document.getElementById('updateCompanyButton');
            const updateCompanyModal = document.getElementById('updateCompanyModal');
            const submitUpdateButton = document.getElementById('submitUpdate');
            const closeModalButton = document.getElementById('closeModal');

            if (usernameElement && companyElement) {
                usernameElement.textContent = userData.username;
                companyElement.textContent = userData.company;
            }

            if (userData.role === 'admin' && updateCompanyButton) {
                updateCompanyButton.style.display = 'block';
            }

            updateCompanyButton?.addEventListener('click', () => {
                updateCompanyModal!.style.display = 'block';
            });

            closeModalButton?.addEventListener('click', () => {
                updateCompanyModal!.style.display = 'none';
            });

            submitUpdateButton?.addEventListener('click', async () => {
                const updateUsername = (document.getElementById('updateUsername') as HTMLInputElement).value;
                const updateCompany = (document.getElementById('updateCompany') as HTMLInputElement).value;

                if (updateUsername && updateCompany) {
                    try {
                        const updateResponse = await fetch('http://localhost:5000/update_company', {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({username: updateUsername, company: updateCompany }),
                            credentials: 'include'
                        });

                        if (updateResponse.ok) {
                            alert('Company updated successfully');
                            updateCompanyModal!.style.display = 'none';
                        } else {
                            alert('Failed to update company');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                    }
                } else {
                    alert('Please fill in both fields');
                }
            });
        } else {
            console.error('Failed to fetch user data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
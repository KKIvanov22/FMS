document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('http://localhost:5000/user', {
            credentials: 'include'
        });
        if (response.ok) {
            const userData = await response.json();
            console.log('Received userData:', userData); // Add this line to log the userData object
            const usernameElement = document.getElementById('username');
            const companyElement = document.getElementById('company');
            const updateCompanyButton = document.getElementById('updateCompanyButton');
            const updateCompanyModal = document.getElementById('updateCompanyModal');
            const submitUpdateButton = document.getElementById('submitUpdate');
            const closeModalButton = document.getElementById('closeModal');
            
            if (usernameElement && companyElement) {
                usernameElement.textContent = userData.Email;
                companyElement.textContent = userData.Company;
            }

            if (userData.Role === 'admin' && updateCompanyButton) {
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
                        }
                    } catch (error) {
                        console.error('Error updating company:', error);
                    }
                }
            });
        } else {
            console.error('Failed to fetch user data:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
});
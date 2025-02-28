document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('http://localhost:5000/user', {
            credentials: 'include'
        });
        if (response.ok) {
            const userData = await response.json();
            console.log('User data:', userData);

            const updateUserRoleButton = document.getElementById('updateUserRoleButton');
            if (updateUserRoleButton) {
                if (userData.RoleInCompany === 'admin') {
                    updateUserRoleButton.style.display = 'block';
                } else {
                    updateUserRoleButton.style.display = 'none';
                }
            }

            const updateUserRoleButtonElement = document.getElementById('updateUserRoleButton');
            if (updateUserRoleButtonElement) {
                updateUserRoleButtonElement.addEventListener('click', () => {
                    const updateUserRoleModal = document.getElementById('updateUserRoleModal');
                    if (updateUserRoleModal) {
                        updateUserRoleModal.style.display = 'block';
                    }
                });
            }

            const closeUpdateUserRoleModal = document.getElementById('closeUpdateUserRoleModal');
            if (closeUpdateUserRoleModal) {
                closeUpdateUserRoleModal.addEventListener('click', () => {
                    const updateUserRoleModal = document.getElementById('updateUserRoleModal');
                    if (updateUserRoleModal) {
                        updateUserRoleModal.style.display = 'none';
                    }
                });
            }

            const submitUpdateUserRole = document.getElementById('submitUpdateUserRole');
            if (submitUpdateUserRole) {
                submitUpdateUserRole.addEventListener('click', async () => {
                    const username = (document.getElementById('updateUserRoleUsername') as HTMLInputElement).value;
                    const role = (document.getElementById('updateUserRole') as HTMLSelectElement).value;
                    const level = (document.getElementById('updateUserLevel') as HTMLInputElement).value;

                    const response = await fetch('http://localhost:5000/update_user_role', {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ username, role, level })
                    });

                    if (response.ok) {
                        alert('User role and level updated successfully');
                        const updateUserRoleModal = document.getElementById('updateUserRoleModal');
                        if (updateUserRoleModal) {
                            updateUserRoleModal.style.display = 'none';
                        }
                    } else {
                        const errorData = await response.json();
                        alert(`Failed to update user role: ${errorData.error}`);
                    }
                });
            }
        } else {
            console.error('Failed to fetch user data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
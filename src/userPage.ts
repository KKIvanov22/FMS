document.addEventListener('DOMContentLoaded', () => {
    const editUserInfoForm = document.getElementById('editUserInfoForm') as HTMLFormElement;
    const usernameField = document.getElementById('editUsername') as HTMLInputElement;
    const emailField = document.getElementById('editEmail') as HTMLInputElement;
    const passwordField = document.getElementById('editPassword') as HTMLInputElement;
    const linkGoogleAccountButton = document.getElementById('linkGoogleAccount') as HTMLButtonElement;

    fetch('http://localhost:5000/user', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
        } else {
            usernameField.value = data.Username;
            emailField.value = data.Email;
        }
    })
    .catch(error => console.error('Error fetching user data:', error));

    editUserInfoForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const updatedUserInfo = {
            email: emailField.value,
            password: passwordField.value
        };

        fetch('http://localhost:5000/update_user', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(updatedUserInfo)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
            } else {
                alert('User information updated successfully');
            }
        })
        .catch(error => console.error('Error updating user information:', error));
    });

    
});
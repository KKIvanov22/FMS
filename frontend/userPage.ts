document.addEventListener('DOMContentLoaded', () => {
    const editUserInfoForm = document.getElementById('editUserInfoForm') as HTMLFormElement;
    const usernameField = document.getElementById('editUsername') as HTMLInputElement;
    const emailField = document.getElementById('editEmail') as HTMLInputElement;
    const passwordField = document.getElementById('editPassword') as HTMLInputElement;
    const editButton = document.getElementById('editButton') as HTMLButtonElement;
    const saveButton = document.getElementById('saveButton') as HTMLButtonElement;
    const profilePicture = document.getElementById('profilePicture') as HTMLDivElement;
    const profilePictureUrl = document.getElementById('profilePictureUrl') as HTMLInputElement;

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
            if (data.ProfilePictureUrl) {
                profilePicture.style.backgroundImage = `url(${data.ProfilePictureUrl})`;
                profilePicture.style.backgroundSize = 'cover';
            }
        }
    })
    .catch(error => console.error('Error fetching user data:', error));

    profilePicture.addEventListener('click', () => {
        profilePictureUrl.style.display = 'block';
    });

    editButton.addEventListener('click', () => {
        usernameField.disabled = false;
        emailField.disabled = false;
        passwordField.disabled = false;
        profilePictureUrl.disabled = false;
        
        editButton.style.display = "none";  
        saveButton.style.display = "block"; 
    });

    editUserInfoForm.addEventListener('submit', (event) => {
        event.preventDefault(); 

        usernameField.disabled = true;
        emailField.disabled = true;
        passwordField.disabled = true;
        profilePictureUrl.disabled = true;

        editButton.style.display = "block"; 
        saveButton.style.display = "none";  

        const updatedUserInfo = {
            email: emailField.value,
            password: passwordField.value,
            profilePictureUrl: profilePictureUrl.value
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
                profilePicture.style.backgroundImage = `url(${profilePictureUrl.value})`;
                profilePicture.style.backgroundSize = 'cover';
            }
        })
        .catch(error => console.error('Error updating user information:', error));
    });
});
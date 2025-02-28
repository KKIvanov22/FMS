declare const google: any;

document.addEventListener('DOMContentLoaded', () => {
    const editUserInfoForm = document.getElementById('editUserInfoForm') as HTMLFormElement;
    const usernameField = document.getElementById('editUsername') as HTMLInputElement;
    const emailField = document.getElementById('editEmail') as HTMLInputElement;
    const passwordField = document.getElementById('editPassword') as HTMLInputElement;
    const editButton = document.getElementById('editButton') as HTMLButtonElement;
    const saveButton = document.getElementById('saveButton') as HTMLButtonElement;
    const profilePicture = document.getElementById('profilePicture') as HTMLDivElement;
    const profilePictureUrl = document.getElementById('profilePictureUrl') as HTMLInputElement;
    const linkToGoogleButton = document.getElementById('linkToGoogle') as HTMLButtonElement;

    fetch('http://localhost:5000/user', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error fetching user data: " + data.error);
        } else {
            usernameField.value = data.Username;
            emailField.value = data.Email;
            if (data.ProfilePictureUrl) {
                profilePicture.style.backgroundImage = `url(${data.ProfilePictureUrl})`;
                profilePicture.style.backgroundSize = 'cover';
            }
        }
    })
    .catch(error => alert('Error fetching user data: ' + error));

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
            } else {
                profilePicture.style.backgroundImage = `url(${profilePictureUrl.value})`;
                profilePicture.style.backgroundSize = 'cover';
            }
        })
        .catch(error => alert('Error updating user information: ' + error));
    });

});

function signInWithGoogle() {
    interface GoogleResponse {
        credential: string;
    }

    interface UserData {
        Username: string;
        Email: string;
        ProfilePictureUrl?: string;
        error?: string;
    }

    interface UpdatedUserInfo {
        email: string;
        password: string;
        profilePictureUrl: string;
    }

    function signInWithGoogle() {
        google.accounts.id.initialize({
            client_id: "977047956351-h0i61rq2bq8lr2teuch9p4gdsbbcgukg.apps.googleusercontent.com", 
            callback: (response: GoogleResponse) => {
                fetch('http://localhost:5000/link-google', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ idToken: response.credential })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        alert('Error linking Google: ' + data.error);
                    } else {
                        alert('Google linked successfully');
                    }
                })
                .catch(error => alert('Error linking Google: ' + error));
            }
        });
        google.accounts.id.prompt();
    }
    google.accounts.id.prompt();
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        window.location.href = './main.html';
    }
});
console.log('Renderer process loaded');

document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM fully loaded and parsed');

  const loginForm = document.getElementById('login-form') as HTMLFormElement;
  const registerForm = document.getElementById('register-form') as HTMLFormElement;

  if (loginForm) {
    console.log('Login form found');
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const username = (document.getElementById('login-username') as HTMLInputElement).value;
      const password = (document.getElementById('login-password') as HTMLInputElement).value;

      try {
        const response = await fetch('http://localhost:5000/login', { 
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password })
        });

        const result = await response.json();
        if (response.ok) {
          alert('Login successful');
          if (result.role === 'admin') {
            window.location.href = './html/adminPage.html';
          } else {
            window.location.href = './html/main.html';
          }
        } else {
          console.error(`Login failed: ${result.error}`);
          alert(`Login failed: ${result.error}`);
        }
      } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login. Please try again.');
      }
    });
  } else {
    console.error('Login form not found');
  }

  if (registerForm) {
    console.log('Register form found');
    registerForm.addEventListener('submit', async (event) => {
      alert('Registering user');

      event.preventDefault();
      const username = (document.getElementById('register-username') as HTMLInputElement).value;
      const password = (document.getElementById('register-password') as HTMLInputElement).value;
      const email = (document.getElementById('register-email') as HTMLInputElement).value;

      try {
        const response = await fetch('http://localhost:5000/register', { 
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password, email })
        });

        const result = await response.json();
        if (response.ok) {
          alert('Registration successful');
          window.location.href = './html/main.html';
        } else {
          if (result.error === "Username or email already exists") {
            alert('Username or email already exists');
          } else {
            console.error(`Registration failed: ${result.error}`);
            alert(`Registration failed: ${result.error}`);
          }
        }
      } catch (error) {
        console.error('Error during registration:', error);
        alert('An error occurred during registration. Please try again.');
      }
    });
  } else {
    console.error('Register form not found');
  }
});
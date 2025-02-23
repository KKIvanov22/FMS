document.addEventListener('DOMContentLoaded', (event) => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const loginButton = document.getElementById('login-button');
    const registerButton = document.getElementById('register-button');
    const formTitle = document.getElementById('form-title');
  
    loginButton.addEventListener('click', () => {
      formTitle.textContent = 'Login';
      registerForm.classList.add('hidden');
      loginForm.classList.remove('hidden');
      loginForm.classList.add('opacity-100');
      registerForm.classList.remove('opacity-100');
    });
  
    registerButton.addEventListener('click', () => {
      formTitle.textContent = 'Register';
      loginForm.classList.add('hidden');
      registerForm.classList.remove('hidden');
      registerForm.classList.add('opacity-100');
      loginForm.classList.remove('opacity-100');
    });
  
    // Existing event listeners for form submissions
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('Login form submitted');
    });
  
    registerForm.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('Register form submitted');
    });
  
    // Additional styling or interactions can be added here
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
      input.addEventListener('focus', (e) => {
        e.target.classList.add('shadow-lg');
      });
      input.addEventListener('blur', (e) => {
        e.target.classList.remove('shadow-lg');
      });
    });
  });
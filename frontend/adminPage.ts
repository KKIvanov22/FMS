interface Company {
    name: string;
}

const companyListContainer = document.getElementById('company-list-container');
const updateCompanyPopup = document.getElementById('update-company-popup');
const newCompanyNameInput = document.getElementById('new-company-name') as HTMLInputElement;
const cancelUpdateButton = document.getElementById('cancel-update');
const confirmUpdateButton = document.getElementById('confirm-update');

let selectedCompany: Company | null = null;

async function fetchCompanies() {
    try {
        const response = await fetch('http://localhost:5000/get_companies', {
            credentials: 'include'
        });
        if (response.ok) {
            const companies: Company[] = await response.json();
            renderCompanies(companies);
        } else {
            console.error('Failed to fetch companies');
        }
    } catch (error) {
        console.error('Error fetching companies:', error);
    }
}

function renderCompanies(companies: Company[]) {
    if (companyListContainer) {
        companyListContainer.innerHTML = '';
        companies.forEach(company => {
            const companyElement = document.createElement('div');
            companyElement.className = 'company-item p-4 mb-4 bg-gray-800 rounded shadow cursor-pointer';
            companyElement.innerText = company.name;
            companyElement.addEventListener('click', () => openUpdatePopup(company));
            companyListContainer.appendChild(companyElement);
        });
    }
}

function openUpdatePopup(company: Company) {
    selectedCompany = company;
    newCompanyNameInput.value = company.name;
    if (updateCompanyPopup) {
        updateCompanyPopup.classList.remove('hidden');
    }
}

function closeUpdatePopup() {
    if (updateCompanyPopup) {
        updateCompanyPopup.classList.add('hidden');
    }
    selectedCompany = null;
}

async function updateCompanyName() {
    if (selectedCompany && newCompanyNameInput.value && newCompanyNameInput.value !== selectedCompany.name) {
        try {
            const response = await fetch('http://localhost:5000/update_company_name', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ oldName: selectedCompany.name, newName: newCompanyNameInput.value }),
                credentials: 'include'
            });

            if (response.ok) {
                alert('Company name updated successfully');
                closeUpdatePopup();
                fetchCompanies();
            } else {
                alert('Failed to update company name');
            }
        } catch (error) {
            console.error('Error updating company name:', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchCompanies();
    const showUsersButton = document.getElementById('show-users-button');
    const userListPopup = document.getElementById('user-list-popup');
    const userListContainer = document.getElementById('user-list-container');
    const closeUserListButton = document.getElementById('close-user-list');
    const editUserPopup = document.getElementById('edit-user-popup');
    const editUserForm = document.getElementById('edit-user-form') as HTMLFormElement;
    const editUserId = document.getElementById('edit-user-id') as HTMLInputElement;
    const editUsername = document.getElementById('edit-username') as HTMLInputElement;
    const editEmail = document.getElementById('edit-email') as HTMLInputElement;
    const editRole = document.getElementById('edit-role') as HTMLInputElement;
    const cancelEditUserButton = document.getElementById('cancel-edit-user');

    showUsersButton?.addEventListener('click', async () => {
        try {
            const response = await fetch('http://localhost:5000/get_all_users');
            const users = await response.json();
            if (userListContainer) {
                userListContainer.innerHTML = '';
                users.forEach((user: { uid: string, Username: string }) => {
                    const userItem = document.createElement('div');
                    userItem.className = 'p-4 bg-gray-800 rounded cursor-pointer hover:bg-gray-700';
                    userItem.textContent = user.Username;
                    userItem.addEventListener('click', () => openEditUserPopup(user));
                    userListContainer.appendChild(userItem);
                });
            }
            userListPopup?.classList.remove('hidden');
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    });

    closeUserListButton?.addEventListener('click', () => {
        userListPopup?.classList.add('hidden');
    });

    cancelEditUserButton?.addEventListener('click', () => {
        editUserPopup?.classList.add('hidden');
    });

    editUserForm?.addEventListener('submit', async (event) => {
        event.preventDefault();
        const userId = editUserId.value;
        const username = editUsername.value;
        const email = editEmail.value;
        const role = editRole.value;

        try {
            const response = await fetch(`http://localhost:5000/update_user/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, role })
            });
            const result = await response.json();
            if (response.ok) {
                alert('User updated successfully');
                editUserPopup?.classList.add('hidden');
                userListPopup?.classList.add('hidden');
            } else {
                alert(`Failed to update user: ${result.error}`);
            }
        } catch (error) {
            console.error('Error updating user:', error);
        }
    });

    function openEditUserPopup(user: { uid: string, Username: string }) {
        editUserId.value = user.uid;
        editUsername.value = user.Username;
        editEmail.value = ''; // Fetch and set email if needed
        editRole.value = ''; // Fetch and set role if needed
        editUserPopup?.classList.remove('hidden');
    }
});

cancelUpdateButton?.addEventListener('click', closeUpdatePopup);
confirmUpdateButton?.addEventListener('click', updateCompanyName);

setInterval(fetchCompanies, 3600000);
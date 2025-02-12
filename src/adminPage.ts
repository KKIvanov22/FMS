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

document.addEventListener('DOMContentLoaded', fetchCompanies);
cancelUpdateButton?.addEventListener('click', closeUpdatePopup);
confirmUpdateButton?.addEventListener('click', updateCompanyName);
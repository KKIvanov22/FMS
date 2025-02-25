document.addEventListener('DOMContentLoaded', async () => {
    async function fetchDataAndUpdateUI() {
        try {
            const response = await fetch('http://localhost:5000/user', {
                credentials: 'include'
            });
            if (response.ok) {
                const userData = await response.json();
                console.log('Received userData:', userData); 
                const usernameElement = document.getElementById('username');
                const companyElement = document.getElementById('company');
                const profilePictureElement = document.getElementById('profilePicture') as HTMLImageElement;
                const updateCompanyButton = document.getElementById('updateCompanyButton');
                const updateCompanyModal = document.getElementById('updateCompanyModal');
                const submitUpdateButton = document.getElementById('submitUpdate');
                const closeModalButton = document.getElementById('closeModal');
                
                if (usernameElement && companyElement) {
                    usernameElement.textContent = userData.Email;
                    companyElement.textContent = userData.Company;
                }

                if (profilePictureElement && userData.ProfilePictureUrl) {
                    profilePictureElement.src = userData.ProfilePictureUrl;
                }

                if (userData.RoleInCompany === 'admin' && updateCompanyButton) {
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

                if (userData.RoleInCompany === 'admin') {
                    const addMaterialsButton = document.getElementById('addMaterialsButton');
                    const addMaterialsModal = document.getElementById('addMaterialsModal');
                    const closeAddMaterialsModal = document.getElementById('closeAddMaterialsModal');
                    const submitMaterial = document.getElementById('submitMaterial');
                    const addMaterialTab = document.getElementById('addMaterialTab');
                    const manageMaterialTab = document.getElementById('manageMaterialTab');
                    const addMaterialSection = document.getElementById('addMaterialSection');
                    const manageMaterialSection = document.getElementById('manageMaterialSection');
                    const materialsList = document.getElementById('materialsList');
                    const updateMaterialModal = document.getElementById('updateMaterialModal');
                    const updateMaterialName = document.getElementById('updateMaterialName') as HTMLInputElement;
                    const updateMaterialQuantity = document.getElementById('updateMaterialQuantity') as HTMLInputElement;
                    const submitUpdateMaterial = document.getElementById('submitUpdateMaterial');
                    const closeUpdateMaterialModal = document.getElementById('closeUpdateMaterialModal');

                    let currentMaterialId: string | null = null;

                    if (addMaterialsButton) {
                        addMaterialsButton.classList.remove('hidden');
                    }

                    addMaterialsButton?.addEventListener('click', () => {
                        addMaterialsModal!.classList.remove('hidden');
                    });

                    closeAddMaterialsModal?.addEventListener('click', () => {
                        addMaterialsModal!.classList.add('hidden');
                    });

                    addMaterialTab?.addEventListener('click', () => {
                        addMaterialSection!.classList.remove('hidden');
                        manageMaterialSection!.classList.add('hidden');
                    });

                    manageMaterialTab?.addEventListener('click', async () => {
                        addMaterialSection!.classList.add('hidden');
                        manageMaterialSection!.classList.remove('hidden');
                        try {
                            const response = await fetch(`http://localhost:5000/get_company_material?company=${userData.Company}`, {
                                credentials: 'include'
                            });
                            if (response.ok) {
                                const materials = await response.json();
                                materialsList!.innerHTML = '';
                                for (const key in materials) {
                                    if (materials.hasOwnProperty(key)) {
                                        const material = materials[key];
                                        const li = document.createElement('li');
                                        li.textContent = `${material.name}: ${material.quantity}`;
                                        li.addEventListener('click', () => {
                                            currentMaterialId = key;
                                            updateMaterialName.value = material.name;
                                            updateMaterialQuantity.value = material.quantity;
                                            updateMaterialModal!.classList.remove('hidden');
                                        });
                                        materialsList!.appendChild(li);
                                    }
                                }
                            } else {
                                console.error('Failed to fetch materials:', response.statusText);
                            }
                        } catch (error) {
                            console.error('Error fetching materials:', error);
                        }
                    });

                    submitUpdateMaterial?.addEventListener('click', async () => {
                        if (currentMaterialId && updateMaterialName.value && updateMaterialQuantity.value) {
                            try {
                                const response = await fetch('http://localhost:5000/update_company_material', {
                                    method: 'POST', // Changed from PUT to POST
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({
                                        company: userData.Company,
                                        material_id: currentMaterialId,
                                        material_data: {
                                            name: updateMaterialName.value,
                                            quantity: updateMaterialQuantity.value
                                        }
                                    }),
                                    credentials: 'include'
                                });

                                if (response.ok) {
                                    alert('Material updated successfully');
                                    updateMaterialModal!.classList.add('hidden');
                                    manageMaterialTab?.click(); // Refresh the materials list
                                } else {
                                    console.error('Failed to update material:', response.statusText);
                                }
                            } catch (error) {
                                console.error('Error updating material:', error);
                            }
                        }
                    });

                    closeUpdateMaterialModal?.addEventListener('click', () => {
                        updateMaterialModal!.classList.add('hidden');
                    });

                    submitMaterial?.addEventListener('click', async () => {
                        const materialName = (document.getElementById('materialName') as HTMLInputElement).value;
                        const materialQuantity = (document.getElementById('materialQuantity') as HTMLInputElement).value;

                        if (materialName && materialQuantity) {
                            try {
                                const response = await fetch('http://localhost:5000/add_company_material', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({ company: userData.Company, materials: { name: materialName, quantity: materialQuantity } }),
                                    credentials: 'include'
                                });

                                if (response.ok) {
                                    alert('Material added successfully');
                                    addMaterialsModal!.classList.add('hidden');
                                } else {
                                    console.error('Failed to add material:', response.statusText);
                                }
                            } catch (error) {
                                console.error('Error adding material:', error);
                            }
                        }
                    });
                }
            } else {
                console.error('Failed to fetch user data:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
        }
    }

    await fetchDataAndUpdateUI();

    setInterval(fetchDataAndUpdateUI, 3600000);
});
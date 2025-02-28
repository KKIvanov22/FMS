document.addEventListener('DOMContentLoaded', async () => {
    async function fetchDataAndUpdateUI() {
        try {
            const response = await fetch('http://localhost:5000/user', {
                credentials: 'include'
            });
            if (response.ok) {
                const userData = await response.json();
                console.log('User data:', userData); 
                const createTeamButton = document.getElementById('createTeamButton');
                const createTeamModal = document.getElementById('createTeamModal');
                const submitTeamButton = document.getElementById('submitTeam');
                const closeTeamModalButton = document.getElementById('closeTeamModal');
                const teamsList = document.getElementById('teamsList');
                const updateTeamModal = document.getElementById('updateTeamModal');
                const teamMembersList = document.getElementById('teamMembersList');
                const updateTeamNameInput = document.getElementById('updateTeamName') as HTMLInputElement;
                const updateTeamMembersList = document.getElementById('updateTeamMembersList');
                const submitUpdateTeamButton = document.getElementById('submitUpdateTeam');
                const closeUpdateTeamModalButton = document.getElementById('closeUpdateTeamModal');
                const assignTaskButton = document.getElementById('assignTaskButton');
                const assignTaskModal = document.getElementById('assignTaskModal');
                const submitTaskButton = document.getElementById('submitTask');
                const closeAssignTaskModalButton = document.getElementById('closeAssignTaskModal');
                const teamTasksList = document.getElementById('teamTasksList');
                const taskNameInput = document.getElementById('taskName') as HTMLInputElement;
                const taskDescriptionInput = document.getElementById('taskDescription') as HTMLTextAreaElement;
                let currentTeamName = '';

                const usersResponse = await fetch('http://localhost:5000/get_users', {
                    credentials: 'include'
                });
                const users = await usersResponse.json();

                function populateUserCheckboxes(container: HTMLElement, selectedUsers: string[] = []) {
                    container.innerHTML = '';
                    users.forEach((user: any) => {
                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.id = `user-${user.uid}`;
                        checkbox.value = user.uid;
                        checkbox.checked = selectedUsers.includes(user.uid);

                        const label = document.createElement('label');
                        label.htmlFor = `user-${user.uid}`;
                        label.textContent = user.Username; 

                        const div = document.createElement('div');
                        div.className = 'mr-4 mb-2';
                        div.appendChild(checkbox);
                        div.appendChild(label);
                        container.appendChild(div);
                    });
                }

                interface TaskData {
                    Description: string;
                }
                
                function populateTasksList(container: HTMLElement, tasks: Record<string, TaskData>) {
                    container.innerHTML = '';
                    for (const [taskName, taskData] of Object.entries(tasks)) {
                        const taskItem = document.createElement('div');
                        taskItem.className = 'bg-gray-600 p-2 rounded-lg shadow-lg';
                        taskItem.innerHTML = `
                            <div class="font-bold">${taskName}</div>
                            <div>${taskData.Description}</div>
                        `;
                        container.appendChild(taskItem);
                    }
                }

                if (userData.RoleInCompany === 'employee') {
                    const employeeTasksResponse = await fetch('http://localhost:5000/get_employee_tasks', {
                        credentials: 'include'
                    });

                    if (employeeTasksResponse.ok) {
                        const employeeTasks = await employeeTasksResponse.json();
                        if (teamsList) {
                            teamsList.innerHTML = ''; // Clear existing tasks
                            for (const [teamName, tasks] of Object.entries(employeeTasks)) {
                                const teamItem = document.createElement('div');
                                teamItem.className = 'bg-gray-700 p-4 rounded-lg shadow-lg w-full max-w-md text-center mb-4';
                                teamItem.innerHTML = `<div class="font-bold">Team: ${teamName}</div>`;
                                const tasksContainer = document.createElement('div');
                                populateTasksList(tasksContainer, tasks as Record<string, TaskData>);
                                teamItem.appendChild(tasksContainer);
                                teamsList.appendChild(teamItem);
                            }
                        }
                    } else {
                        console.error('Failed to fetch employee tasks');
                    }
                }

                if ((userData.RoleInCompany === 'admin' || userData.RoleInCompany === 'team_leader') || createTeamButton) {
                    if (createTeamButton) {
                        createTeamButton.style.display = 'block';
                    }

                    const teamsResponse = await fetch(`http://localhost:5000/get_teams?company=${userData.Company}`, {
                        credentials: 'include'
                    });

                    if (teamsResponse.ok) {
                        const teams = await teamsResponse.json();
                        if (teamsList) {
                            teamsList.innerHTML = ''; // Clear existing teams
                            for (const [teamName, teamData] of Object.entries(teams)) {
                                const teamItem = document.createElement('div');
                                const team = teamData as { Members: string[], Tasks: any };
                                teamItem.className = 'bg-gray-700 p-4 rounded-lg shadow-lg w-full max-w-md text-center mb-4';
                                const memberUsernames = team.Members.map((memberId) => {
                                    const matchedUser = users.find((u: any) => u.uid === memberId);
                                    return matchedUser ? matchedUser.Username : memberId;
                                });
                                teamItem.textContent = `Team: ${teamName}, Members: ${memberUsernames.join(', ')}`;
                                teamItem.addEventListener('click', async () => {
                                    currentTeamName = teamName;
                                    updateTeamNameInput.value = teamName;
                                    populateUserCheckboxes(updateTeamMembersList!, team.Members);
                                    const tasksResponse = await fetch(`http://localhost:5000/get_team_tasks?company=${userData.Company}&team=${teamName}`, {
                                        credentials: 'include'
                                    });
                                    if (tasksResponse.ok) {
                                        const tasks = await tasksResponse.json();
                                        populateTasksList(teamTasksList!, tasks);
                                    }
                                    updateTeamModal!.style.display = 'block';
                                });
                                teamsList.appendChild(teamItem);
                            }
                        }
                    } else {
                        console.error('Failed to fetch teams');
                    }
                }

                createTeamButton?.addEventListener('click', () => {
                    populateUserCheckboxes(teamMembersList!);
                    createTeamModal!.style.display = 'block';

                    const fetchMaterialsButton = document.createElement('button');
                    fetchMaterialsButton.textContent = 'Fetch Materials from Inventory';
                    fetchMaterialsButton.className = 'bg-gray-600 text-white py-2 px-4 rounded hover:bg-gray-500';

                    fetchMaterialsButton.addEventListener('click', async () => {
                        try {
                            const materialsResponse = await fetch(`http://localhost:5000/get_company_material?company=${userData.Company}`, {
                                credentials: 'include'
                            });
                            if (materialsResponse.ok) {
                                const materialsData = await materialsResponse.json();
                                console.log('Materials fetched:', materialsData);
                                // Display or handle the fetched materials as needed
                            } else {
                                console.error('Failed to fetch materials');
                            }
                        } catch (error) {
                            console.error('Error fetching materials:', error);
                        }
                    });

                    createTeamModal!.querySelector('.flex')?.insertAdjacentElement('beforebegin', fetchMaterialsButton);
                });

                closeTeamModalButton?.addEventListener('click', () => {
                    createTeamModal!.style.display = 'none';
                });

                submitTeamButton?.addEventListener('click', async () => {
                    const teamName = (document.getElementById('teamName') as HTMLInputElement).value;
                    const selectedMembers = Array.from(teamMembersList!.querySelectorAll('input[type="checkbox"]:checked')).map((checkbox: any) => checkbox.value);
                    const company = userData.Company;
                    if (teamName && selectedMembers.length > 0) {
                        try {
                            const teamResponse = await fetch('http://localhost:5000/add_team', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({ company: company, teamName: teamName, members: selectedMembers }),
                                credentials: 'include'
                            });

                            if (teamResponse.ok) {
                                alert('Team created successfully');
                                createTeamModal!.style.display = 'none';
                                const teamsResponse = await fetch(`http://localhost:5000/get_teams?company=${company}`, {
                                    credentials: 'include'
                                });

                                if (teamsResponse.ok) {
                                    const teams = await teamsResponse.json();
                                    if (teamsList) {
                                        teamsList.innerHTML = ''; // Clear existing teams
                                        for (const [teamName, teamData] of Object.entries(teams)) {
                                            const teamItem = document.createElement('div');
                                            const team = teamData as { Members: string[], Tasks: any };
                                            teamItem.className = 'bg-gray-700 p-4 rounded-lg shadow-lg w-full max-w-md text-center mb-4';
                                            const memberUsernames = team.Members.map((memberId) => {
                                                const matchedUser = users.find((u: any) => u.uid === memberId);
                                                return matchedUser ? matchedUser.Username : memberId;
                                            });
                                            teamItem.textContent = `Team: ${teamName}, Members: ${memberUsernames.join(', ')}`;
                                            teamItem.addEventListener('click', async () => {
                                                currentTeamName = teamName;
                                                updateTeamNameInput.value = teamName;
                                                populateUserCheckboxes(updateTeamMembersList!, team.Members);
                                                const tasksResponse = await fetch(`http://localhost:5000/get_team_tasks?company=${userData.Company}&team=${teamName}`, {
                                                    credentials: 'include'
                                                });
                                                if (tasksResponse.ok) {
                                                    const tasks = await tasksResponse.json();
                                                    populateTasksList(teamTasksList!, tasks);
                                                }
                                                updateTeamModal!.style.display = 'block';
                                            });
                                            teamsList.appendChild(teamItem);
                                        }
                                    }
                                } else {
                                    console.error('Failed to fetch teams');
                                }
                            } else {
                                alert('Failed to create team');
                            }
                        } catch (error) {
                            console.error('Error:', error);
                        }
                    } else {
                        alert('Please fill in both fields');
                    }
                });

                closeUpdateTeamModalButton?.addEventListener('click', () => {
                    updateTeamModal!.style.display = 'none';
                });

                submitUpdateTeamButton?.addEventListener('click', async () => {
                    const newTeamName = updateTeamNameInput.value;
                    const selectedMembers = Array.from(updateTeamMembersList!.querySelectorAll('input[type="checkbox"]:checked')).map((checkbox: any) => checkbox.value);
                    const company = userData.Company;
                    if (newTeamName && selectedMembers.length > 0) {
                        try {
                            const updateResponse = await fetch('http://localhost:5000/update_team', {
                                method: 'PUT',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({ company: company, oldTeamName: currentTeamName, newTeamName: newTeamName, members: selectedMembers }),
                                credentials: 'include'
                            });

                            if (updateResponse.ok) {
                                alert('Team updated successfully');
                                updateTeamModal!.style.display = 'none';
                                const teamsResponse = await fetch(`http://localhost:5000/get_teams?company=${company}`, {
                                    credentials: 'include'
                                });

                                if (teamsResponse.ok) {
                                    const teams = await teamsResponse.json();
                                    if (teamsList) {
                                        teamsList.innerHTML = ''; // Clear existing teams
                                        for (const [teamName, teamData] of Object.entries(teams)) {
                                            const teamItem = document.createElement('div');
                                            const team = teamData as { Members: string[], Tasks: any };
                                            teamItem.className = 'bg-gray-700 p-4 rounded-lg shadow-lg w-full max-w-md text-center mb-4';
                                            const memberUsernames = team.Members.map((memberId) => {
                                                const matchedUser = users.find((u: any) => u.uid === memberId);
                                                return matchedUser ? matchedUser.Username : memberId;
                                            });
                                            teamItem.textContent = `Team: ${teamName}, Members: ${memberUsernames.join(', ')}`;
                                            teamItem.addEventListener('click', async () => {
                                                currentTeamName = teamName;
                                                updateTeamNameInput.value = teamName;
                                                populateUserCheckboxes(updateTeamMembersList!, team.Members);
                                                const tasksResponse = await fetch(`http://localhost:5000/get_team_tasks?company=${userData.Company}&team=${teamName}`, {
                                                    credentials: 'include'
                                                });
                                                if (tasksResponse.ok) {
                                                    const tasks = await tasksResponse.json();
                                                    populateTasksList(teamTasksList!, tasks);
                                                }
                                                updateTeamModal!.style.display = 'block';
                                            });
                                            teamsList.appendChild(teamItem);
                                        }
                                    }
                                } else {
                                    console.error('Failed to fetch teams');
                                }
                            } else {
                                alert('Failed to update team');
                            }
                        } catch (error) {
                            console.error('Error:', error);
                        }
                    } else {
                        alert('Please fill in both fields');
                    }
                });

                assignTaskButton?.addEventListener('click', () => {
                    assignTaskModal!.style.display = 'block';
                });

                closeAssignTaskModalButton?.addEventListener('click', () => {
                    assignTaskModal!.style.display = 'none';
                });

                submitTaskButton?.addEventListener('click', async () => {
                    const taskName = taskNameInput.value;
                    const taskDescription = taskDescriptionInput.value;
                    const company = userData.Company;
                    if (taskName && taskDescription) {
                        try {
                            const taskResponse = await fetch('http://localhost:5000/add_team_tasks', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({ company: company, teamName: currentTeamName, taskName: taskName, description: taskDescription }),
                                credentials: 'include'
                            });

                            if (taskResponse.ok) {
                                alert('Task assigned successfully');
                                assignTaskModal!.style.display = 'none';
                                const tasksResponse = await fetch(`http://localhost:5000/get_team_tasks?company=${company}&team=${currentTeamName}`, {
                                    credentials: 'include'
                                });
                                if (tasksResponse.ok) {
                                    const tasks = await tasksResponse.json();
                                    populateTasksList(teamTasksList!, tasks);
                                }
                            } else {
                                alert('Failed to assign task');
                            }
                        } catch (error) {
                            console.error('Error:', error);
                        }
                    } else {
                        alert('Please fill in both fields');
                    }
                });
            } else {
                console.error('Failed to fetch user data');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    await fetchDataAndUpdateUI();

    setInterval(fetchDataAndUpdateUI, 3600000);
});
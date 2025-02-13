document.addEventListener('DOMContentLoaded', async () => {
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
            const updateTeamNameInput = document.getElementById('updateTeamName') as HTMLInputElement;
            const submitUpdateTeamButton = document.getElementById('submitUpdateTeam');
            const closeUpdateTeamModalButton = document.getElementById('closeUpdateTeamModal');
            const teamMembersList = document.getElementById('teamMembersList');
            const updateTeamMembersList = document.getElementById('updateTeamMembersList');
            let currentTeamName = '';

            // Fetch all users for team member selection
            const usersResponse = await fetch('http://localhost:5000/get_users', {
                credentials: 'include'
            });
            const users = await usersResponse.json();

            function populateUserCheckboxes(container: HTMLElement, selectedUsers: string[] = []) {
                container.innerHTML = '';
                users.forEach((user: any) => {
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = `user-${user.username}`;
                    checkbox.value = user.username;
                    checkbox.checked = selectedUsers.includes(user.username);
                    const label = document.createElement('label');
                    label.htmlFor = `user-${user.username}`;
                    label.textContent = user.username;
                    const div = document.createElement('div');
                    div.className = 'mr-4 mb-2';
                    div.appendChild(checkbox);
                    div.appendChild(label);
                    container.appendChild(div);
                });
            }

            if (userData.RoleInCompany === 'admin' && createTeamButton) {
                createTeamButton.style.display = 'block';

                const teamsResponse = await fetch(`http://localhost:5000/get_teams?company=${userData.Company}`, {
                    credentials: 'include'
                });

                if (teamsResponse.ok) {
                    const teams = await teamsResponse.json();
                    if (teamsList) {
                        teamsList.innerHTML = ''; // Clear existing teams
                        for (const [teamName, teamData] of Object.entries(teams)) {
                            const teamItem = document.createElement('button');
                            const team = teamData as { Members: string[] };
                            teamItem.textContent = `Team: ${teamName}, Members: ${team.Members.join(', ')}`;
                            teamItem.addEventListener('click', () => {
                                currentTeamName = teamName;
                                updateTeamNameInput.value = teamName;
                                populateUserCheckboxes(updateTeamMembersList!, team.Members);
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
                                        const teamItem = document.createElement('button');
                                        const team = teamData as { Members: string[] };
                                        teamItem.textContent = `Team: ${teamName}, Members: ${team.Members.join(', ')}`;
                                        teamItem.addEventListener('click', () => {
                                            currentTeamName = teamName;
                                            updateTeamNameInput.value = teamName;
                                            populateUserCheckboxes(updateTeamMembersList!, team.Members);
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
                                        const teamItem = document.createElement('button');
                                        const team = teamData as { Members: string[] };
                                        teamItem.textContent = `Team: ${teamName}, Members: ${team.Members.join(', ')}`;
                                        teamItem.addEventListener('click', () => {
                                            currentTeamName = teamName;
                                            updateTeamNameInput.value = teamName;
                                            populateUserCheckboxes(updateTeamMembersList!, team.Members);
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
        } else {
            console.error('Failed to fetch user data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
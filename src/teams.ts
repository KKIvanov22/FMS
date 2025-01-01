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
            const updateTeamMembersInput = document.getElementById('updateTeamMembers') as HTMLInputElement;
            const submitUpdateTeamButton = document.getElementById('submitUpdateTeam');
            const closeUpdateTeamModalButton = document.getElementById('closeUpdateTeamModal');
            let currentTeamName = '';

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
                                updateTeamMembersInput.value = team.Members.join(', ');
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
                createTeamModal!.style.display = 'block';
            });

            closeTeamModalButton?.addEventListener('click', () => {
                createTeamModal!.style.display = 'none';
            });

            submitTeamButton?.addEventListener('click', async () => {
                const teamName = (document.getElementById('teamName') as HTMLInputElement).value;
                const teamMembers = (document.getElementById('teamMembers') as HTMLInputElement).value.split(',');
                const company = userData.Company;
                if (teamName && teamMembers.length > 0) {
                    try {
                        const teamResponse = await fetch('http://localhost:5000/add_team', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ company: company, teamName: teamName, members: teamMembers }),
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
                                            updateTeamMembersInput.value = team.Members.join(', ');
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
                const newTeamMembers = updateTeamMembersInput.value.split(',');
                const company = userData.Company;
                if (newTeamName && newTeamMembers.length > 0) {
                    try {
                        const updateResponse = await fetch('http://localhost:5000/update_team', {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ company: company, oldTeamName: currentTeamName, newTeamName: newTeamName, members: newTeamMembers }),
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
                                            updateTeamMembersInput.value = team.Members.join(', ');
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
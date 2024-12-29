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
            if (userData.roleInCompany === 'admin' && createTeamButton) {
                createTeamButton.style.display = 'block';
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
                const company = userData.company;
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
        } else {
            console.error('Failed to fetch user data');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
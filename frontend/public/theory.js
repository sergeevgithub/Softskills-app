document.addEventListener('DOMContentLoaded', () => {
    const theoryContainer = document.getElementById('theory-container');
    const token = localStorage.getItem('token');

    // Redirect to login if not authenticated
    if (!token) {
        alert('You are not logged in. Redirecting to login page.');
        window.location.href = 'index.html';
        return;
    }

    // Fetch theory data from the server
    const fetchTheoryData = async (dayNumber) => {
        try {
            const response = await fetch('/theory', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({ day_number: dayNumber }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch theory data');
            }

            const theoryData = await response.json();
            console.log('Fetched theory data:', theoryData);
            renderTheory(theoryData);

        } catch (error) {
            console.error('Error fetching theory data:', error);
        }
    };

    // Function to render the theory content
    const renderTheory = (data) => {
        // Clear the theory container before rendering
        theoryContainer.innerHTML = '';

        // Core Concept
        const coreConcept = document.createElement('section');
        coreConcept.innerHTML = `
            <h2>Core Concept</h2>
            <p>${data.coreConcept}</p>
        `;
        theoryContainer.appendChild(coreConcept);

        // Types of Conflicts
        const typesSection = document.createElement('section');
        typesSection.innerHTML = `<h2>Types of Conflicts</h2>`;
        data.typesOfConflicts.forEach(type => {
            const typeDiv = document.createElement('div');
            typeDiv.innerHTML = `
                <h3>${type.type}</h3>
                <p>${type.description}</p>
                <ul>
                    ${type.causes?.map(item => `<li>${item}</li>`).join('') || ''}
                    ${type.involves?.map(item => `<li>${item}</li>`).join('') || ''}
                    ${type.triggers?.map(item => `<li>${item}</li>`).join('') || ''}
                    ${type.characteristics?.map(item => `<li>${item}</li>`).join('') || ''}
                </ul>
            `;
            typesSection.appendChild(typeDiv);
        });
        theoryContainer.appendChild(typesSection);

        // Conflict Dynamics
        const dynamicsSection = document.createElement('section');
        dynamicsSection.innerHTML = `
            <h2>Conflict Dynamics</h2>
            <div>
                <h3>Constructive Conflicts</h3>
                <p>${data.conflictDynamics.constructiveConflicts.description}</p>
                <ul>
                    ${data.conflictDynamics.constructiveConflicts.benefits.map(benefit => `<li>${benefit}</li>`).join('')}
                </ul>
            </div>
            <div>
                <h3>Destructive Conflicts</h3>
                <p>${data.conflictDynamics.destructiveConflicts.description}</p>
                <ul>
                    ${data.conflictDynamics.destructiveConflicts.effects.map(effect => `<li>${effect}</li>`).join('')}
                </ul>
            </div>
        `;
        theoryContainer.appendChild(dynamicsSection);
    };

    // Add event listeners for navigation buttons
    const nextButton = document.getElementById('next-button');
    nextButton.addEventListener('click', () => {
        window.location.href = 'activity.html';
    });

    const homeButton = document.getElementById('home-button');
    homeButton.addEventListener('click', () => {
        window.location.href = 'study_plan.html';
    });

    // Fetch and render theory data for the current day
    const currentDay = localStorage.getItem('day_number');
    fetchTheoryData(currentDay);
});

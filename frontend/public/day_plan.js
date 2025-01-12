document.addEventListener('DOMContentLoaded', () => {
    const fieldsContainer = document.getElementById('fields-container');
    const token = localStorage.getItem('token');

    if (!token) {
        alert('You are not logged in. Redirecting to login page.');
        window.location.href = 'index.html'; // Redirect to login if not authenticated
        return;
    }
    // Fetch day plan data from the server
    const fetchDayPlan = async (dayNumber) => {
        try {
            const response = await fetch('/day_plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ day_number: dayNumber }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch day plan');
            }

            const data = await response.json();
            renderActivities(data.activities_number);
        } catch (error) {
            console.error('Error fetching day plan:', error);
        }
    };

    // Render buttons based on the number of activities
    const renderActivities = (activitiesNumber) => {
        fieldsContainer.innerHTML = ''; // Clear previous content
        fieldsContainer.innerHTML += `<button class="field" onclick="handleClick('Theory')">Theory</button>`;
        for (let i = 1; i <= activitiesNumber; i++) {
            fieldsContainer.innerHTML += `<button class="field" onclick="handleClick('Activity ${i}')">Activity ${i}</button>`;
        }
    };

    // Handle button clicks
    window.handleClick = (section) => {
        if (section == 'Theory') {
//            alert('You clicked on ${section}');
            window.location.href = 'theory.html';
        }
        else {
            window.location.href = 'activity.html';
        }
//        alert(`You clicked on ${section}`);
        // Add navigation logic here (e.g., redirect to another page)
    };

    // Fetch and render activities for a specific day
    const currentDay = localStorage.getItem('day_number'); // Replace with dynamic day number logic if needed
    fetchDayPlan(currentDay);
});

// Simulate fetching the study plan JSON from the server
//const fetchStudyPlan = async () => {
//    return {
//        study_plan: [
//            { day_number: 1, topic: "Understanding Conflict", available: true },
//            { day_number: 2, topic: "Conflict Causes and Triggers", available: false },
//            { day_number: 3, topic: "Conflict Response Styles", available: false },
//            { day_number: 4, topic: "Active Listening", available: false },
//            { day_number: 5, topic: "Non-Verbal Communication", available: false },
//            { day_number: 6, topic: "Assertive Communication", available: false },
//            { day_number: 7, topic: "Emotional Regulation", available: false },
//            { day_number: 8, topic: "Negotiation Fundamentals", available: false },
//            { day_number: 9, topic: "Conflict Resolution Strategies", available: false }
//        ]
//    };
//};

document.addEventListener('DOMContentLoaded', async () => {
    localStorage.setItem('token', 'amoma')
    const token = localStorage.getItem('token');

    if (!token) {
        alert('You are not logged in. Redirecting to login page.');
        window.location.href = 'index.html'; // Redirect to login if not authenticated
        return;
    }

    const response = await fetch('/study_plan', {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (response.ok) {
        const data = await response.json();
        const container = document.getElementById('study-plan-container');

        data.study_plan.forEach(section => {
            const sectionDiv = document.createElement('div');
            sectionDiv.className = `study-section ${section.available ? 'available' : 'unavailable'}`;
            sectionDiv.innerText = `Day ${section.day_number}: ${section.topic}`;

            if (section.available) {
                sectionDiv.addEventListener('click', () => {
                    alert(`You selected: ${section.topic}`);
                    window.location.href = 'day_plan.html';
                });
            }

            container.appendChild(sectionDiv);
        });
    } else {
        alert('Failed to load courses. Please try again.');
    }
});

// Render the study plan in the container
//const renderStudyPlan = async () => {
//    const data = await fetchStudyPlan(); // Simulate fetching JSON data from the server
//    const container = document.getElementById('study-plan-container');
//
//    data.study_plan.forEach(section => {
//        const sectionDiv = document.createElement('div');
//        sectionDiv.className = `study-section ${section.available ? 'available' : 'unavailable'}`;
//        sectionDiv.innerText = `Day ${section.day_number}: ${section.topic}`;
//
//        if (section.available) {
//            sectionDiv.addEventListener('click', () => {
//                alert(`You selected: ${section.topic}`);
//                // Logic to load the section content can go here
//            });
//        }
//
//        container.appendChild(sectionDiv);
//    });
//};
//
//// Initialize the study plan rendering
//document.addEventListener('DOMContentLoaded', renderStudyPlan);

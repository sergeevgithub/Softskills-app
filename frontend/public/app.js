document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const addCourseForm = document.getElementById("add-course-form");
    const courseList = document.getElementById("course-list");
    const coursesSection = document.getElementById("courses-section");
    const loginSection = document.getElementById("login-section");

    let token = null;

    // Handle login
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("http://localhost:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(errorData.message || "Login failed.");
                return;
            }

            const data = await response.json();
            token = data.access_token;

            // Show courses section
            loginSection.style.display = "none";
            coursesSection.style.display = "block";
            fetchCourses();
        } catch (error) {
            console.error("Login error:", error);
            alert("An error occurred during login.");
        }
    });

    // Fetch courses
    async function fetchCourses() {
        try {
            const response = await fetch("http://localhost:5000/courses", {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                alert("Failed to fetch courses.");
                return;
            }

            const courses = await response.json();
            courseList.innerHTML = "";
            courses.forEach((course) => {
                const li = document.createElement("li");
                li.textContent = `${course.title}: ${course.description}`;
                courseList.appendChild(li);
            });
        } catch (error) {
            console.error("Error fetching courses:", error);
            alert("An error occurred while fetching courses.");
        }
    }

    // Add a new course
    addCourseForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const title = document.getElementById("course-title").value;
        const description = document.getElementById("course-description").value;

        try {
            const response = await fetch("http://localhost:5000/courses", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ title, description }),
            });

            if (!response.ok) {
                alert("Failed to add course.");
                return;
            }

            const newCourse = await response.json();
            const li = document.createElement("li");
            li.textContent = `${newCourse.title}: ${newCourse.description}`;
            courseList.appendChild(li);

            addCourseForm.reset();
        } catch (error) {
            console.error("Error adding course:", error);
            alert("An error occurred while adding the course.");
        }
    });
});

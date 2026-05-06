const API_BASE = window.location.origin;

// ---------------- LOGIN ---------------- //

async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {

        const response = await fetch(`${API_BASE}/auth/login`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email,
                password
            })

        });

        const data = await response.json();

        if (response.ok) {

            localStorage.setItem(
                "token",
                data.access_token
            );

            // IMPORTANT FIX
            window.location.href = "/dashboard-page";

        } else {

            alert(data.msg || "Login failed");

        }

    } catch (error) {

        console.error(error);

        alert("Server error");

    }

}


// ---------------- LOAD DASHBOARD ---------------- //

async function loadDashboard() {

    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "/";
        return;
    }

    try {

        const response = await fetch(`${API_BASE}/dashboard`, {

            headers: {
                Authorization: `Bearer ${token}`
            }

        });

        const data = await response.json();

        if (!response.ok) {

            alert(data.msg || "Unauthorized");

            localStorage.removeItem("token");

            window.location.href = "/";

            return;
        }

        document.getElementById("projects").innerText =
            data.projects;

        document.getElementById("tasks").innerText =
            data.tasks;

        document.getElementById("myTasks").innerText =
            data.my_tasks;

        document.getElementById("completed").innerText =
            data.completed;

    } catch (error) {

        console.error(error);

    }

}


// ---------------- LOAD TASKS ---------------- //

async function loadTasks() {

    const token = localStorage.getItem("token");

    try {

        const response = await fetch(`${API_BASE}/tasks`, {

            headers: {
                Authorization: `Bearer ${token}`
            }

        });

        const tasks = await response.json();

        const taskList =
            document.getElementById("taskList");

        if (!taskList) return;

        taskList.innerHTML = "";

        tasks.forEach(task => {

            const div = document.createElement("div");

            div.className = "task-card";

            div.innerHTML = `
                <h3>${task.title}</h3>
                <p>Status: ${task.status}</p>

                <button onclick="markDone(${task.id})">
                    Mark Done
                </button>
            `;

            taskList.appendChild(div);

        });

    } catch (error) {

        console.error(error);

    }

}


// ---------------- CREATE TASK ---------------- //

async function createTask() {

    const title =
        document.getElementById("taskTitle").value;

    const token = localStorage.getItem("token");

    try {

        const response = await fetch(`${API_BASE}/tasks`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },

            body: JSON.stringify({
                title: title,
                project_id: 1,
                assigned_to: 1
            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("Task created successfully");

            loadTasks();
            loadDashboard();

        } else {

            alert(data.msg || "Task creation failed");

        }

    } catch (error) {

        console.error(error);

    }

}


// ---------------- MARK TASK DONE ---------------- //

async function markDone(taskId) {

    const token = localStorage.getItem("token");

    try {

        const response = await fetch(
            `${API_BASE}/tasks/${taskId}`,
            {

                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },

                body: JSON.stringify({
                    status: "done"
                })

            }
        );

        if (response.ok) {

            loadTasks();
            loadDashboard();

        }

    } catch (error) {

        console.error(error);

    }

}


// ---------------- LOGOUT ---------------- //

function logout() {

    localStorage.removeItem("token");

    window.location.href = "/";

}


// ---------------- AUTO LOAD ---------------- //

if (
    window.location.pathname === "/dashboard-page"
) {

    loadDashboard();
    loadTasks();

}
const API = "";


// ---------------- LOGIN ----------------

async function login() {

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    try {

        const response = await fetch(
            `${API}/auth/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

            localStorage.setItem(
                "token",
                data.access_token
            );

            window.location.href = "/dashboard";

        } else {

            alert(data.msg || "Login failed");
        }

    } catch (error) {

        console.error(error);

        alert("Server error");
    }
}


// ---------------- LOAD DASHBOARD ----------------

async function loadDashboard() {

    const token =
        localStorage.getItem("token");

    if (!token) {
        window.location.href = "/";
        return;
    }

    try {

        const response = await fetch(
            `${API}/api/dashboard`,
            {

                headers: {
                    Authorization: `Bearer ${token}`
                }

            }
        );

        const data = await response.json();

        document.getElementById("projects").innerText =
            data.projects ?? 0;

        document.getElementById("tasks").innerText =
            data.tasks ?? 0;

        document.getElementById("myTasks").innerText =
            data.my_tasks ?? 0;

        document.getElementById("completed").innerText =
            data.completed ?? 0;

        // LOAD TASKS ALSO
        loadTasks();

    } catch (error) {

        console.error(error);
    }
}


// ---------------- CREATE TASK ----------------

async function createTask() {

    const token =
        localStorage.getItem("token");

    const title =
        document.getElementById("taskTitle").value;

    if (!title) {
        alert("Enter task title");
        return;
    }

    try {

        const response = await fetch(
            `${API}/tasks`,
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },

                body: JSON.stringify({
                    title: title
                })

            }
        );

        const data = await response.json();

        alert(data.msg);

        document.getElementById("taskTitle").value = "";

        // REFRESH
        loadDashboard();
        loadTasks();

    } catch (error) {

        console.error(error);
    }
}


// ---------------- LOAD TASKS ----------------

async function loadTasks() {

    const token =
        localStorage.getItem("token");

    try {

        const response = await fetch(
            `${API}/tasks`,
            {

                headers: {
                    Authorization: `Bearer ${token}`
                }

            }
        );

        const tasks = await response.json();

        const container =
            document.getElementById("taskContainer");

        container.innerHTML = "";

        if (tasks.length === 0) {

            container.innerHTML =
                "<li>No tasks available</li>";

            return;
        }

        tasks.forEach(task => {

            const li =
                document.createElement("li");

            li.className = "task-item";

            li.innerHTML = `
                <span>
                    ${task.title}
                    - ${task.status}
                </span>

                <button onclick="markDone(${task.id})">
                    Mark Done
                </button>
            `;

            container.appendChild(li);
        });

    } catch (error) {

        console.error(error);
    }
}


// ---------------- MARK TASK DONE ----------------

async function markDone(taskId) {

    const token =
        localStorage.getItem("token");

    try {

        const response = await fetch(
            `${API}/tasks/${taskId}`,
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

        const data = await response.json();

        alert(data.msg);

        loadDashboard();
        loadTasks();

    } catch (error) {

        console.error(error);
    }
}


// ---------------- LOGOUT ----------------

function logout() {

    localStorage.removeItem("token");

    window.location.href = "/";
}
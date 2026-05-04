const API = "http://127.0.0.1:5000";

// LOGIN
function login() {
  fetch(`${API}/auth/login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      email: document.getElementById("email").value,
      password: document.getElementById("password").value
    })
  })
  .then(res => res.json())
  .then(data => {
    localStorage.setItem("token", data.access_token);
    window.location.href = "dashboard.html";
  });
}

// LOGOUT
function logout() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}

// DASHBOARD
function loadDashboard() {
  fetch(`${API}/dashboard`, {
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("stats").innerHTML = `
      <div class="stat-card">
        <h3>Projects</h3>
        <p>${data.projects}</p>
      </div>
      <div class="stat-card">
        <h3>Total Tasks</h3>
        <p>${data.tasks}</p>
      </div>
      <div class="stat-card">
        <h3>My Tasks</h3>
        <p>${data.my_tasks}</p>
      </div>
      <div class="stat-card">
        <h3>Completed</h3>
        <p>${data.completed}</p>
      </div>
    `;
  });
}

// TASKS
function loadTasks() {
  fetch(`${API}/tasks`, {
    headers: {
      "Authorization": "Bearer " + localStorage.getItem("token")
    }
  })
  .then(res => res.json())
  .then(tasks => {
    document.getElementById("tasks").innerHTML = tasks.map(t => `
      <div class="task">
        <b>${t.title}</b><br><br>

        <span class="badge ${t.status}">
          ${t.status}
        </span>

        <br><br>

        <button onclick="updateTask(${t.id}, 'todo')" class="todo">Todo</button>
        <button onclick="updateTask(${t.id}, 'in-progress')" class="inprogress">In Progress</button>
        <button onclick="updateTask(${t.id}, 'done')" class="done">Done</button>
      </div>
    `).join("");
  });
}

// UPDATE TASK
function updateTask(id, status) {
  fetch(`${API}/tasks/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + localStorage.getItem("token")
    },
    body: JSON.stringify({status})
  })
  .then(() => {
    loadTasks();
    loadDashboard();
  });
}

// AUTO LOAD
if (window.location.pathname.includes("dashboard")) {
  loadDashboard();
  loadTasks();
}
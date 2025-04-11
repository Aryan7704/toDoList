async function prioritizeTasks() {
    const res = await fetch("/prioritize");
    const list = document.getElementById("prioritized-list");
    list.innerHTML = "";
    try {
        const data = await res.json();
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            data.forEach(task => {
                const li = document.createElement("li");
                li.textContent = `${task.title} - ${task.description} (Due: ${task.deadline})`;
                list.appendChild(li);
            });
        }
    } catch (err) {
        list.innerHTML = `<li>Failed to fetch prioritized tasks.</li>`;
    }
}
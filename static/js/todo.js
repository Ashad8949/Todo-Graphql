// Function to fetch and display todo items
async function fetchTodos() {
    const response = await fetch('/graphql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({ query: '{ todos { id, title, description, time } }' }),
    });

    const data = await response.json();
    const todos = data.data.todos;

    // Display todo items in the UI
    const todoList = document.getElementById('todoList');
    todoList.innerHTML = '';
    todos.forEach(todo => {
        const todoItem = document.createElement('div');
        todoItem.classList.add('todo-item');
        todoItem.innerHTML = `
            <h3>${todo.title}</h3>
            <p>${todo.description}</p>
            <p>${todo.time}</p>
            <button onclick="viewTask('${todo.id}')">View</button>
            <button onclick="deleteTask('${todo.id}')">Delete</button>
        `;
        todoList.appendChild(todoItem);
    });
}

// Function to show/hide the new task form
function toggleNewTaskForm() {
    const newTaskForm = document.getElementById('newTaskForm');
    newTaskForm.classList.toggle('hidden');
}

// Function to submit a new task
async function addTodo() {
    const title = document.getElementById('todoTitle').value;
    const description = document.getElementById('todoDescription').value;
    const time = document.getElementById('todoTime').value;
    const imageInput = document.getElementById('imageInput');
    let image = null;

    if (imageInput.files.length > 0) {
        image = imageInput.files[0];
    }

    // Create a JSON object with the GraphQL mutation
    const mutation = `
        mutation CreateTodo($title: String!, $description: String!, $time: String!, $image: Upload) {
            createTodo(title: $title, description: $description, time: $time) {
                todo {
                    id
                    title
                    description
                    time
                    image
                }
            }
        }
    `;

    // Create a FormData object to hold the variables for the GraphQL mutation
    const variables = {
        title,
        description,
        time,
        image: null // Ensure image is set to null if not provided
    };

    const formData = new FormData();
    formData.append('query', mutation);
    formData.append('variables', JSON.stringify(variables));
    // Append image file to FormData if it exists
    if (image) {
        formData.append('image', image);
    }

    // Perform a POST request to submit the new task
    const response = await fetch('/graphql', {
        method: 'POST',
        body: formData,
    });

    // Parse the response as JSON
    const data = await response.json();

    // Check if the task was successfully created
    if (data.data && data.data.createTodo) {
        const newTodo = data.data.createTodo.todo;
        console.log('New todo created:', newTodo);
        // Optionally, you can update the UI to display the newly created todo
        fetchTodos(); // Fetch and display all todos to update the UI
    } else {
        console.error('Failed to create todo:', data.errors);
        // Handle error, display error message, etc.
    }
}


// Function to view a task
function viewTask(taskId) {
    // Redirect to the task details page or display in a modal
}

// Function to delete a task
async function deleteTask(taskId) {
    // Perform a DELETE request to delete the task using GraphQL mutation
    const response = await fetch('/graphql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query: `
                mutation {
                    deleteTodo(id: "${taskId}") {
                        success
                    }
                }
            `
        }),
    });

    const data = await response.json();

    if (data.data.delete_todo.success) {
        // Task deleted successfully, you can perform any additional actions here if needed
        console.log(`Task with ID ${taskId} deleted successfully`);
        // Refresh the list of todo items after deletion
        fetchTodos();
    } else {
        // Error occurred while deleting task
        console.error(`Error deleting task with ID ${taskId}`);
    }
}


// Event listener for the New Task button
document.getElementById('newTaskButton').addEventListener('click', toggleNewTaskForm);

// Event listener for the Cancel button in the new task form
document.getElementById('cancelButton').addEventListener('click', toggleNewTaskForm);

// Fetch todos when the page loads
fetchTodos();

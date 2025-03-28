// DOM Elements
const loginTab = document.getElementById('login-tab');
const signupTab = document.getElementById('signup-tab');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const loginBtn = document.getElementById('login-btn');
const signupBtn = document.getElementById('signup-btn');
const authContainer = document.getElementById('auth-container');
const dashboard = document.getElementById('dashboard');
const userInfo = document.querySelector('.user-info');
const username = document.querySelector('.username');
const logoutBtn = document.getElementById('logout');
const resultsBtn = document.getElementById('results-btn');
const resultsModal = document.getElementById('results-modal');
const closeModal = document.getElementById('close-modal');
const loader = document.getElementById('loader');

const resultsList = document.getElementById("results-list");
const percentileSpan = document.getElementById("percentile");
const rankSpan = document.getElementById("rank");
// Tab switching
loginTab.addEventListener('click', () => {
    loginTab.classList.add('active');
    signupTab.classList.remove('active');
    loginForm.style.display = 'block';
    signupForm.style.display = 'none';
});

signupTab.addEventListener('click', () => {
    signupTab.classList.add('active');
    loginTab.classList.remove('active');
    signupForm.style.display = 'block';
    loginForm.style.display = 'none';
});

// Login functionality
loginBtn.addEventListener('click', async () => {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
        alert('Please fill in all fields');
        return;
    }

    // Show loading indicator
    loader.style.display = 'block';

    try {
        const response = await fetch('http://localhost:8080/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (data.status === 'success') {
            authContainer.style.display = 'none';
            dashboard.style.display = 'block';
            userInfo.style.display = 'flex';
            username.textContent = data.username;
        } else {
            alert(data.message);
        }
    } catch (error) {
        alert('An error occurred. Please try again.');
    } finally {
        loader.style.display = 'none';
    }
});

// Signup functionality
signupBtn.addEventListener('click', async () => {
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const confirm = document.getElementById('signup-confirm').value;

    if (!name || !email || !password || !confirm) {
        alert('Please fill in all fields');
        return;
    }

    if (password !== confirm) {
        alert('Passwords do not match');
        return;
    }

    // Show loading indicator
    loader.style.display = 'block';

    try {
        const response = await fetch('http://localhost:8080/students/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();
        if (data.status === 'success') {
            loginTab.click();
            alert('Account created successfully! Please login.');
        } else {
            alert(data.message);
        }
    } catch (error) {
        alert('An error occurred. Please try again.');
        console.log(error);
    } finally {
        loader.style.display = 'none';
    }
});

// Results button functionality
resultsBtn.addEventListener('click', async () => {
    // Show loading indicator
    loader.style.display = 'block';

    try {
        const response = await fetch('http://localhost:8080/results/get', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: document.getElementById('login-email').value })
        });

        const data = await response.json();
        if (data.status === 'success') {
            // Display results in modal
            displayResults(data.results);

            // resultsModal.style.display = 'flex';
        } else {
            alert("Error: "+data.message);
        }
    } catch (error) {
        // console.log(error);
        alert('An error occurred. Please try again.');
    } finally {
        loader.style.display = 'none';
    }
});

    // Function to Display Results in Modal
function displayResults(results) {
    resultsList.innerHTML = ""; // Clear previous results
    if (!results) {
        resultsList.innerHTML = "<li>No results available</li>";
        return;
    }

    Object.entries(results).forEach(([subject, score]) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${subject}: ${score}/100`;
        resultsList.appendChild(listItem);
    });

    percentileSpan.textContent = results.percentile || "N/A";
    rankSpan.textContent = results.rank || "N/A";

    resultsModal.style.display = "flex"; // Show modal
}
// Logout functionality
logoutBtn.addEventListener('click', () => {
    // Show auth container and hide dashboard
    authContainer.style.display = 'block';
    dashboard.style.display = 'none';
    userInfo.style.display = 'none';
    
    // Clear form fields
    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';
});


// Close modal functionality
closeModal.addEventListener('click', () => {
    resultsModal.style.display = 'none';
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === resultsModal) {
        resultsModal.style.display = 'none';
    }
});
// Function to get CSRF token from cookies
function getCSRFToken() {
    const name = "csrftoken";
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// function to show loading spinner
function showLoading(selector) {
    selector.innerHTML =
  '<svg class="animate-spin h-5 w-5 mr-2 text-white" viewBox="0 0 24 24"> <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle> <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 0116 0"></path> </svg> sending request...';
    selector.disabled = true;
}

// function to hide loading spinner
function hideLoading(selector, text) {
    selector.innerHTML = text;
    selector.disabled = false;
}
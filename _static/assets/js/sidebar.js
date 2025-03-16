
document.addEventListener('DOMContentLoaded', () => {
    // Get references to the button and sidebar
    const toggleButtons = document.querySelectorAll('.dashboardSidebarToggleButton');;
    const sidebar = document.getElementById('dashboard-sidebar');

    // Add a click event listener to the button
    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            console.log('clicked');
            sidebar.classList.toggle('dashboard-sidebar-hidden');
        });
    });
});

function toggleSidebarSubmenu(submenuId) {
    const submenu = document.getElementById(submenuId);
    submenu.classList.toggle('max-h-0');
    submenu.classList.toggle('max-h-40'); // Adjust based on your content
}
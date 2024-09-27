// Function to open the catalog modal
document.getElementById('catalogButton').addEventListener('click', function() {
    openModal('catalogModal');
});

// Function to open the basket modal
document.getElementById('basketButton').addEventListener('click', function() {
    openModal('basketModal');
});

// Function to open a specific modal
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

// Function to close a specific modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close the modal when clicking outside of the modal content
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
};

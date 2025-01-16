// Function to create and show a toast
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');

    // Create toast element
    const toast = document.createElement('div');
    toast.classList.add('toast', 'fade', 'show', `bg-${type}`);
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    toast.setAttribute('style', 'width: fit-content');
    toast.style.marginBottom = '1rem';

    toast.innerHTML = `
        <div class="d-flex justify-content-end">
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body" style="width: fit-content">
            ${message}
        </div>
    `;

    toastContainer.appendChild(toast);

    // Automatically remove toast after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        toast.classList.add('hide');
        setTimeout(() => toast.remove(), 300); // Remove toast element after fade
    }, 5000);
}
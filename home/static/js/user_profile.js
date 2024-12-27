document.addEventListener('DOMContentLoaded', function () {
    const subUsersTable = document.querySelector('#sub-users-table');
    const subUsersLoader = document.getElementById('sub-users-loader');
    const addSubUserSection = document.getElementById('add-sub-user-section');

    const toggleSpinner = (show) => {
        if (show) {
            subUsersLoader.style.display = 'flex'; // Show the spinner
            subUsersLoader.offsetHeight; // Trigger a reflow
            subUsersTable.style.display = 'none';  // Hide the table
        } else {
            subUsersLoader.style.display = 'none'; // Hide the spinner
            subUsersLoader.offsetHeight; // Trigger a reflow
            subUsersTable.style.display = 'table'; // Show the table
        }
    };

    // Fetch and Render Profile Data
    const fetchProfileData = () => {
        toggleSpinner(true); // Show spinner
        fetch('/api/user-profile/')
            .then(response => response.json())
            .then(data => {
                // Render user details
                document.getElementById('username').textContent = data.username;

                if (data.parent == null) {
                    subUsersTable.querySelector('tbody').innerHTML = ''; // Clear table
                    if (data.sub_users.length > 0) {
                        data.sub_users.forEach(subUser => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${subUser.username}</td>
                                <td>
                                    <button class="btn btn-danger btn-sm delete-sub-user" data-id="${subUser.id}">
                                        Delete
                                    </button>
                                </td>
                            `;
                            subUsersTable.querySelector('tbody').appendChild(row);
                        });

                        // Delete Sub-User Handler
                        document.querySelectorAll('.delete-sub-user').forEach(button => {
                            button.addEventListener('click', function () {
                                deleteSubUser(this.dataset.id);
                            });
                        });
                    } else {
                        subUsersTable.querySelector('tbody').innerHTML = '<tr><td colspan="3">No Sub-Users</td></tr>';
                    }

                    // Toggle Add-Sub-User Section
                    addSubUserSection.style.display = data.sub_users.length < data.allowed_sub_users_count ? 'block' : 'none';
                }
                toggleSpinner(false); // Hide spinner
            })
            .catch(error => {
                showToast(`Error fetching profile data: ${error}`, 'danger');
                toggleSpinner(false); // Hide spinner
            });
    };

    // Add Sub-User
    const addSubUser = (subUserName) => {
        toggleSpinner(true); // Show spinner
        const csrfToken = getCSRFToken();
        fetch('/add-sub-user/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `sub_username=${subUserName}&csrfmiddlewaretoken=${csrfToken}`,
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast(data.success, 'success');
                    fetchProfileData(); // Refresh profile data
                } else {
                    showToast(data.error, 'danger');
                    toggleSpinner(false); // Hide spinner
                }
            })
            .catch(error => {
                showToast(`Error adding sub-user: ${error}`, 'danger');
                toggleSpinner(false); // Hide spinner
            });
    };

    // Delete Sub-User
    const deleteSubUser = (subUserId) => {
        toggleSpinner(true); // Show spinner
        fetch(`/delete-sub-user/${subUserId}/`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': getCSRFToken() },
        })
            .then(response => {
                if (response.ok) {
                    showToast('Sub-User deleted successfully', 'success');
                    fetchProfileData(); // Refresh profile data
                } else {
                    showToast('Failed to delete Sub-User', 'danger');
                    toggleSpinner(false); // Hide spinner
                }
            })
            .catch(error => {
                showToast(`Error deleting Sub-User: ${error}`, 'danger');
                toggleSpinner(false); // Hide spinner
            });
    };

    // Get CSRF Token
    const getCSRFToken = () => {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    };

    // Add Event Listener to Add-Sub-User Form
    document.getElementById('add-sub-user-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const subUserName = document.getElementById('sub_username').value;
        addSubUser(subUserName);
    });

    // Initial Fetch of Profile Data
    fetchProfileData();
});

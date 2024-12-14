document.addEventListener('DOMContentLoaded', function() {

    const subUsersTable = document.querySelector('#sub-users-table tbody');
    const addSubUserSection = document.getElementById('add-sub-user-section');

    // Fetch and Render Profile Data
    const fetchProfileData = () => {
        fetch('/api/user-profile/')
            .then(response => response.json())
            .then(data => {
                // Always Render User Details
                document.getElementById('username').textContent = data.username;

                // Render Sub-User List or Add Form
                if (data.parent == null) {
                    if (data.sub_users.length > 0) {
                        subUsersTable.innerHTML = ''; // Clear Sub-Users Table
                        data.sub_users.forEach(subUser => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${subUser.id}</td>
                                <td>${subUser.username}</td>
                                <td>
                                    <button class="btn btn-danger btn-sm delete-sub-user" data-id="${subUser.id}">
                                        Delete
                                    </button>
                                </td>
                            `;
                            subUsersTable.appendChild(row);
                        });

                        // Add Event Listeners for Delete Buttons
                        $(document).on('click', '.delete-sub-user', function (e) {
                            e.preventDefault();
                            deleteSubUser($(this).data('id'));
                        });

                    } else if (data.sub_users.length === 0) {
                        // Show Add Sub-User Form
                        subUsersTable.innerHTML = '<tr><td colspan="3">No Sub-Users</td></tr>';
                    }

                    // Show Add Sub-User Form
                    if (data.sub_users.length === 2) {
                        addSubUserSection.style.display = 'none';
                    }else if (data.sub_users.length < 2) {
                        // Show Sub-Users Section
                        addSubUserSection.style.display = 'block';
                        // Add sub-user
                        // document.getElementById('add-sub-user-form').removeEventListener('submit');
                        $('#add-sub-user-form').unbind('submit').bind('submit', function(e) {
                            e.preventDefault();
                            const subUserName = document.getElementById('sub_username').value;
                            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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
                                    document.getElementById('sub_username').value = "";
                                    // location.reload(); // Reload to show the new sub-user
                                    fetchProfileData(); // Refresh Profile Data
                                } else {
                                    showToast(data.error, 'danger');
                                }
                            }).catch(error => {
                                showToast(`${error}`, 'danger');

                            });
                        });
                    }
                }
            }).catch(error => {
                showToast(`Error fetching profile data : ${error}`, 'danger');

            });
    };

    // Delete Sub-User
    const deleteSubUser = (subUserId) => {
        fetch(`/delete-sub-user/${subUserId}/`, { method: 'DELETE', headers: { 'X-CSRFToken': getCSRFToken() } })
            .then(response => {
                if (response.ok) {
                    showToast('Sub-User deleted successfully', 'success');
                    fetchProfileData(); // Refresh Profile Data
                } else {
                    showToast('Failed to delete Sub-User', 'danger');
                }
            })
            .catch(error => {
                showToast(`Error deleting Sub-User: ${error}`, 'danger');
            });
    };

    // Get CSRF Token
    const getCSRFToken = () => {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    };

    // Initial Fetch of Profile Data
    fetchProfileData();
});

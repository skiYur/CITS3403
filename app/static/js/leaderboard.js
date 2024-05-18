// leaderboard.js
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/leaderboard')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('leaderboard-body');
        tbody.innerHTML = '';  // Clear existing entries
        data.forEach((user, index) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <th scope="row">${index + 1}</th>
                <td>
                    <a href="/user/${user.username}">
                        <img src="${user.avatar ? '/static/' + user.avatar : '/static/images/avatars/default_avatar.png'}" alt="${user.username}'s avatar" class="avatar-leaderboard">
                        ${user.username}
                    </a>
                </td>
                <td>${user.postsCount}</td>`;
            tbody.appendChild(tr);
        });
    })
    .catch(error => console.error('Error loading the leaderboard:', error));
});

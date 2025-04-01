document.addEventListener('DOMContentLoaded', function() {
    // Notifications Toggle
    const notificationBtn = document.getElementById('notification-btn');
    const notificationsPanel = document.getElementById('notifications-panel');
    
    if (notificationBtn && notificationsPanel) {
        // Toggle notifications panel when bell icon is clicked
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationsPanel.classList.toggle('hidden');
            
            // If opening the panel, mark as read
            if (!notificationsPanel.classList.contains('hidden')) {
                const badge = document.getElementById('notification-badge');
                if (badge) {
                    // Don't hide immediately, let the server update it
                    console.log('Notifications panel opened');
                }
            }
        });
        
        // Close panel when clicking outside
        document.addEventListener('click', function(e) {
            if (!notificationsPanel.contains(e.target) && e.target !== notificationBtn) {
                notificationsPanel.classList.add('hidden');
            }
        });
        
        // Mark all notifications as read
        const markAllReadBtn = document.getElementById('mark-all-read');
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', function() {
                fetch('/mark_notifications_read', {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.querySelectorAll('.notification-item').forEach(item => {
                            item.classList.remove('unread');
                        });
                        const badge = document.getElementById('notification-badge');
                        if (badge) {
                            badge.classList.add('hidden');
                        }
                    }
                })
                .catch(error => console.error('Error marking notifications as read:', error));
            });
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Function to adjust notification panel position if it overflows the viewport
    function adjustNotificationPanelPosition() {
        const notificationsPanel = document.querySelector('.notifications-panel:not(.hidden)');
        if (!notificationsPanel) return;
        
        const rect = notificationsPanel.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        
        // If the panel extends beyond the right edge of the viewport
        if (rect.right > viewportWidth) {
            const overflowAmount = rect.right - viewportWidth;
            const currentRight = parseInt(window.getComputedStyle(notificationsPanel).right);
            notificationsPanel.style.right = (currentRight + overflowAmount + 10) + 'px'; // Add 10px buffer
        }
        
        // Ensure the panel doesn't go off the left edge either
        if (rect.left < 0) {
            notificationsPanel.style.right = (viewportWidth - rect.width - 10) + 'px';
        }
    }
    
    // Call this function whenever the notification panel is shown
    const notificationBtn = document.getElementById('notification-btn');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', function() {
            setTimeout(adjustNotificationPanelPosition, 10); // Small delay to ensure panel is visible
        });
    }
    
    // Adjust on window resize
    window.addEventListener('resize', function() {
        const notificationsPanel = document.querySelector('.notifications-panel:not(.hidden)');
        if (notificationsPanel) {
            adjustNotificationPanelPosition();
        }
    });

    // ...existing code...
});

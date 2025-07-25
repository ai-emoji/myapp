document.addEventListener('DOMContentLoaded', function() {
    const messages = ["xin chào", "hân hạnh đón tiếp", "một hai ba"];
    let idx = 0;
    const el = document.getElementById('dynamic-menu1-text');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    // Function to update text content
    function updateText() {
        if (el) {
            el.textContent = messages[idx];
        }
    }
    
    // Initialize with first message
    updateText();
    
    // Auto change every 3 seconds
    let autoInterval = setInterval(() => {
        idx = (idx + 1) % messages.length;
        updateText();
    }, 3000);
    
    // Previous button click handler
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            // Clear auto interval when user manually changes
            clearInterval(autoInterval);
            idx = (idx - 1 + messages.length) % messages.length;
            updateText();
            // Restart auto interval after 5 seconds of inactivity
            autoInterval = setInterval(() => {
                idx = (idx + 1) % messages.length;
                updateText();
            }, 3000);
        });
    }
    
    // Next button click handler
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            // Clear auto interval when user manually changes
            clearInterval(autoInterval);
            idx = (idx + 1) % messages.length;
            updateText();
            // Restart auto interval after 5 seconds of inactivity
            autoInterval = setInterval(() => {
                idx = (idx + 1) % messages.length;
                updateText();
            }, 3000);
        });
    }
});
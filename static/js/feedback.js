document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('feedback-form');
    const emailInput = document.getElementById('email');
    const messageInput = document.getElementById('message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Clear previous errors
        const errors = form.querySelectorAll('.error-message');
        errors.forEach(err => err.remove());

        // Basic client-side validation
        let valid = true;
        if (!emailInput.value.trim()) {
            showError(emailInput, 'Email is required');
            valid = false;
        }
        if (!messageInput.value.trim()) {
            showError(messageInput, 'Message is required');
            valid = false;
        }
        if (messageInput.value.length > 5000) {
            showError(messageInput, 'Message too long (max 5000 chars)');
            valid = false;
        }

        if (!valid) return;

        try {
            const response = await fetch('/api/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: emailInput.value.trim(),
                    phone: document.getElementById('phone')?.value?.trim() || null,
                    message: messageInput.value.trim()
                })
            });

            const data = await response.json();
            
            if (response.ok) {
                window.location.href = '/feedback/success';
            } else {
                showError(form, data.error || 'Error submitting feedback');
            }
        } catch (err) {
            showError(form, 'Network error submitting feedback');
        }
    });

    function showError(element, message) {
        const error = document.createElement('div');
        error.className = 'error-message';
        error.textContent = message;
        element.parentNode.insertBefore(error, element.nextSibling);
    }
});
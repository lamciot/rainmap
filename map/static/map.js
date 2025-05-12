// disable minute form
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.querySelector('input[type="datetime-local"]');
    dateInput.addEventListener('input', function() {
        if (!this.value) return;
        
        const date = new Date(this.value);
        if (date.getMinutes() !== 0) {
            date.setMinutes(0);
            this.value = date.toISOString().slice(0, 16);
        }
    });
    
    // Optional: Force initial value to whole hour
    // if (dateInput.value) {
    //     const date = new Date(dateInput.value);
    //     if (date.getMinutes() !== 0) {
    //     date.setMinutes(0);
    //     dateInput.value = date.toISOString().slice(0, 16);
    //     }
    // }
});
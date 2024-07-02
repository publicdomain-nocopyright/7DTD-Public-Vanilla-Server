document.addEventListener('DOMContentLoaded', () => {
    const containers = document.querySelectorAll('.hover-container');
    
    containers.forEach(container => {
        const infoBox = container.querySelector('.hover-info-box');

        let timeoutId;

        const showInfoBox = () => {
            clearTimeout(timeoutId);
            infoBox.style.display = 'block';
            setTimeout(() => {
                infoBox.style.opacity = '1';
            }, 10); // Small delay to trigger CSS transition
        };

        const hideInfoBox = () => {
            timeoutId = setTimeout(() => {
                infoBox.style.opacity = '0';
                setTimeout(() => {
                    infoBox.style.display = 'none';
                }, 300); // Match the transition duration
            }, 300); // Delay before hiding the box
        };

        container.addEventListener('mouseenter', showInfoBox);
        container.addEventListener('mouseleave', hideInfoBox);
        infoBox.addEventListener('mouseenter', showInfoBox);
        infoBox.addEventListener('mouseleave', hideInfoBox);
    });
});

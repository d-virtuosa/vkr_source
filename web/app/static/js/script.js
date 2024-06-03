// static/js/scripts.js

document.addEventListener('DOMContentLoaded', function () {
    const animatedText = document.querySelector('.animated-text');
    let count = 0;
    setInterval(() => {
        const colors = ['#ff0000', '#ff8000', '#ffff00', '#00ff00', '#0000ff', '#ff00ff'];
        animatedText.style.color = colors[count];
        count = (count + 1) % colors.length;
    }, 1000);
});

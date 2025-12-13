
document.addEventListener('DOMContentLoaded', () => {
    // Data tanggal valid dari backend (format YYYY-MM-DD); passed via global variable in HTML
    if (typeof validDates === 'undefined') return;

    // Parsing data tanggal
    const dateMap = {};
    if (validDates && validDates.length > 0) {
        validDates.forEach(dateStr => {
            const parts = dateStr.split('-');
            const y = parseInt(parts[0]);
            const m = parseInt(parts[1]);
            const d = parseInt(parts[2]);

            if (!dateMap[y]) dateMap[y] = {};
            if (!dateMap[y][m]) dateMap[y][m] = [];
            dateMap[y][m].push(d);
        });
    }

    const yearSelect = document.getElementById('year');
    const monthSelect = document.getElementById('month');
    const daySelect = document.getElementById('day');
    const form = document.getElementById('predictionForm');

    // Helper functions exposed or kept internal
    const updateDays = () => {
        const y = yearSelect.value;
        const m = monthSelect.value;
        daySelect.innerHTML = '';

        if (y && m && dateMap[y] && dateMap[y][m]) {
            const days = dateMap[y][m].sort((a, b) => a - b);
            days.forEach(d => daySelect.add(new Option(d, d)));
        }
    };

    const updateMonths = () => {
        const y = yearSelect.value;
        monthSelect.innerHTML = '';

        if (y && dateMap[y]) {
            const months = Object.keys(dateMap[y]).sort((a, b) => a - b);
            months.forEach(m => monthSelect.add(new Option(m, m)));
        }
        updateDays();
    };

    // Initial population
    const years = Object.keys(dateMap).sort((a, b) => b - a);
    years.forEach(y => yearSelect.add(new Option(y, y)));

    if (years.length > 0) {
        updateMonths();
    }

    // Event listeners
    yearSelect.addEventListener('change', updateMonths);
    monthSelect.addEventListener('change', updateDays);

    if (form) {
        form.addEventListener('submit', () => {
            const btn = document.getElementById('predictBtn');
            if (btn) btn.classList.add('loading');
        });
    }
});

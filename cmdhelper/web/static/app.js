// Theme handling
function initTheme() {
    const isDark = localStorage.getItem('theme') === 'dark';
    document.documentElement.classList.toggle('dark', isDark);
}

document.getElementById('themeToggle').addEventListener('click', () => {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!');
    });
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

// Command display
function displayCommand(command, examples, category) {
    return `
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-lg">
            <div class="flex justify-between items-center">
                <h2 class="text-xl font-bold">${command}</h2>
                <span class="px-2 py-1 text-sm rounded bg-primary/20 text-primary">
                    ${category}
                </span>
            </div>
            <div class="mt-4 space-y-2">
                ${examples.map(ex => {
                    const [desc, cmd] = ex.split('::');
                    return `
                        <div class="border-l-4 border-primary p-3 bg-gray-50 dark:bg-gray-900">
                            <p class="text-sm mb-2">${desc}</p>
                            <div class="flex justify-between items-center">
                                <code class="font-mono">${cmd}</code>
                                <button onclick="copyToClipboard('${cmd}')"
                                    class="text-primary hover:text-primary/80">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <!-- Copy icon -->
                                    </svg>
                                </button>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
    `;
}

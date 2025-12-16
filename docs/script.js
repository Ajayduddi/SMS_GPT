document.addEventListener('DOMContentLoaded', () => {



    // --- Navbar Scroll Effect ---
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // --- Chat Animation ---
    const chatContainer = document.getElementById('chat-messages');
    if (chatContainer) {
        const messages = [
            { type: 'user', text: 'Define Artificial Intelligence?', time: 1000 },
            { type: 'bot', text: 'AI is the simulation of human intelligence by machines. 🧠', time: 2500 },
            { type: 'user', text: 'Can you summarize the news?', time: 4500 },
            { type: 'bot', text: 'Sure! Here are the top headlines... [Fetching Live Data] 🌍', time: 6000 }
        ];

        let msgIndex = 0;

        function createMessage(text, type) {
            const div = document.createElement('div');
            div.className = `chat-bubble ${type === 'user' ? 'chat-user' : 'chat-bot'}`;
            div.innerText = text;
            return div;
        }

        function runChat() {
            if (msgIndex >= messages.length) {
                setTimeout(() => {
                    chatContainer.innerHTML = '';
                    msgIndex = 0;
                    runChat();
                }, 5000);
                return;
            }

            const msg = messages[msgIndex];
            setTimeout(() => {
                const bubble = createMessage(msg.text, msg.type);
                chatContainer.appendChild(bubble);
                msgIndex++;
                runChat();
            }, msg.time - (msgIndex > 0 ? messages[msgIndex - 1].time : 0));
        }

        runChat();
    }

    // --- Copy Code Functionality ---
    window.copyCode = function () {
        const code = `git clone https://github.com/Ajayduddi/SMS_GPT.git
cd SMS_GPT
pip install -r requirements.txt
python main.py`;

        navigator.clipboard.writeText(code).then(() => {
            // Show toast
            const toast = document.getElementById('toast');
            if (toast) {
                toast.style.opacity = '1';
                setTimeout(() => { toast.style.opacity = '0'; }, 2000);
            }

            // Button feedback
            const btn = document.getElementById('copyBtn');
            if (btn) {
                const originalHtml = btn.innerHTML;
                btn.innerHTML = '<i class="fa-solid fa-check" style="color: var(--secondary)"></i>';
                setTimeout(() => {
                    btn.innerHTML = originalHtml;
                }, 2000);
            }
        });
    };

    // --- Scroll Animations (Intersection Observer) ---
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
});

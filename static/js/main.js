// ============================================
// ExamHub - MAIN.JS (PART 1)
// Card • Tabs • Filter • Search
// ============================================

// --------------------------------------------
// TOGGLE QUESTION CARD
// --------------------------------------------
function toggleCard(card) {

    card.classList.toggle("open");

}

// --------------------------------------------
// TAB SWITCHING
// --------------------------------------------
function switchTab(tab, btn) {

    document.querySelectorAll(".tab-btn").forEach(button => {

        button.classList.remove("active");

    });

    btn.classList.add("active");

    const important = document.getElementById("tab-important");
    const all = document.getElementById("tab-all");
    const filter = document.getElementById("unitFilter");

    if (important)
        important.style.display =
            tab === "important" ? "flex" : "none";

    if (all)
        all.style.display =
            tab === "all" ? "flex" : "none";

    if (filter)
        filter.style.display =
            tab === "all" ? "flex" : "none";

}

// --------------------------------------------
// FILTER UNIT
// --------------------------------------------
function filterUnit(unit, btn) {

    document.querySelectorAll(".unit-btn").forEach(button => {

        button.classList.remove("active");

    });

    btn.classList.add("active");

    document.querySelectorAll(".unit-section").forEach(section => {

        if (unit === "all") {

            section.style.display = "block";

            return;

        }

        section.style.display =
            section.dataset.unit === unit
                ? "block"
                : "none";

    });

}

// --------------------------------------------
// SEARCH QUESTIONS
// --------------------------------------------
function searchQuestions() {

    const input = document.getElementById("searchInput");

    if (!input) return;

    const value = input.value.toLowerCase();

    document.querySelectorAll(".question-card").forEach(card => {

        const text = card.innerText.toLowerCase();

        if (text.includes(value)) {

            card.style.display = "block";

        }

        else {

            card.style.display = "none";

        }

    });

}
// ============================================
// ExamHub - MAIN.JS (PART 2)
// Copy • Toast • Bookmark
// ============================================


// --------------------------------------------
// COPY ANSWER
// --------------------------------------------
function copyAnswer(event, id) {

    event.stopPropagation();

    const answer = document.getElementById("ans-" + id);

    if (!answer) {

        showToast("❌ Answer not found");

        return;

    }

    navigator.clipboard.writeText(answer.innerText).then(() => {
          // Google Analytics - Copy Answer
        if (typeof gtag === "function") {
        gtag("event", "copy_answer", {
            subject: typeof SUBJECT_CONTEXT !== "undefined" ? SUBJECT_CONTEXT : "General"
        });
        }

        const btn = event.target;

        const oldText = btn.innerHTML;

        btn.innerHTML = "✅ Copied";

        btn.classList.add("btn-copied");

        showToast("Answer Copied Successfully");

        setTimeout(() => {

            btn.innerHTML = oldText;

            btn.classList.remove("btn-copied");

        }, 2000);

    });

}


// --------------------------------------------
// TOAST MESSAGE
// --------------------------------------------
function showToast(message) {

    const toast = document.getElementById("toast");

    if (!toast) return;

    toast.innerHTML = message;

    toast.classList.add("show");

    clearTimeout(window.toastTimer);

    window.toastTimer = setTimeout(() => {

        toast.classList.remove("show");

    }, 2500);

}


// --------------------------------------------
// BOOKMARK QUESTION
// --------------------------------------------
function bookmarkQuestion(id, button) {

    let bookmarks =
        JSON.parse(localStorage.getItem("bookmarks")) || [];

    if (bookmarks.includes(id)) {

        bookmarks = bookmarks.filter(item => item !== id);

        showToast("❌ Bookmark Removed");

        if (button)
            button.innerHTML = "🤍";

    }

    else {

        bookmarks.push(id);

        showToast("⭐ Added to Bookmark");

        if (button)
            button.innerHTML = "❤️";

    }

    localStorage.setItem(

        "bookmarks",

        JSON.stringify(bookmarks)

    );

}


// --------------------------------------------
// LOAD BOOKMARKS
// --------------------------------------------
function loadBookmarks() {

    const bookmarks =
        JSON.parse(localStorage.getItem("bookmarks")) || [];

    document.querySelectorAll(".bookmark-btn").forEach(btn => {

        const id = btn.dataset.id;

        if (bookmarks.includes(id)) {

            btn.innerHTML = "❤️";

        }

        else {

            btn.innerHTML = "🤍";

        }

    });

}
// ============================================
// AI CHAT
// ============================================

// Prevent multiple requests
let aiLoading = false;

// OPEN / CLOSE AI
function toggleAI() {

    const box = document.getElementById("aiBox");
    const fab = document.getElementById("aiFab");

    if (!box || !fab) return;

    box.classList.toggle("open");

    fab.style.display =
        box.classList.contains("open")
            ? "none"
            : "flex";

}

function closeAI() {

    const box = document.getElementById("aiBox");
    const fab = document.getElementById("aiFab");

    if (!box || !fab) return;

    box.classList.remove("open");

    fab.style.display = "flex";

}

// Ask AI from Question
function askAI(event, question) {

    event.stopPropagation();

    const input = document.getElementById("aiInput");

    if (!input) return;

    toggleAI();

    input.value = question;

    sendAI();

}

// SEND TO GEMINI
async function sendAI() {

    if (aiLoading) return;

    const input = document.getElementById("aiInput");

    if (!input) return;

    const question = input.value.trim();

    // Google Analytics - AI Question

if (typeof gtag === "function") {

    gtag("event", "ask_ai", {

        question: question,

        subject: typeof SUBJECT_CONTEXT !== "undefined" ? SUBJECT_CONTEXT : "General"

    });

}





    if (question === "") return;

    aiLoading = true;

    addMessage(question, "user");

    input.value = "";

    const loading = addMessage("🤖 Thinking...", "bot loading");

    try {

        const response = await fetch("/api/ask", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                question: question,

                context:
                    typeof SUBJECT_CONTEXT !== "undefined"
                        ? SUBJECT_CONTEXT
                        : "Electrical Engineering"

            })

        });

        const data = await response.json();

loading.remove();

if (data.error) {

    addMessage(data.error, "bot");

    aiLoading = false;

    return;

}

addMessage(data.answer, "bot");

}

catch (err) {

    loading.remove();

    addMessage("⚠ Unable to connect to AI. L Please try again later.", "bot");

}

aiLoading = false;
}
// ============================================
// AI MESSAGE
// ============================================

function addMessage(text, type) {

    const container = document.getElementById("aiMessages");

    if (!container) return;

    const div = document.createElement("div");

    div.className = "ai-msg " + type;

    div.style.whiteSpace = "pre-wrap";

    div.innerText = text;

    container.appendChild(div);

    container.scrollTop = container.scrollHeight;

    return div;

}


// ============================================
// CLEAR CHAT
// ============================================

function clearAIChat() {

    const container = document.getElementById("aiMessages");

    if (!container) return;

    container.innerHTML = "";

    showToast("Chat Cleared");

}


// ============================================
// AUTO SCROLL
// ============================================

function scrollAIBottom() {

    const container = document.getElementById("aiMessages");

    if (!container) return;

    container.scrollTop = container.scrollHeight;

}


// ============================================
// DOM LOADED
// ============================================

document.addEventListener("DOMContentLoaded", () => {

    loadBookmarks();

    const input = document.getElementById("aiInput");

    if (input) {

        input.addEventListener("keydown", function(e){

            if(e.key === "Enter" && !e.shiftKey){

                e.preventDefault();

                sendAI();

            }

        });

    }

    scrollAIBottom();

});
// ============================================
// ExamHub - MAIN.JS (PART 5)
// Progress • Back To Top • Animation
// ============================================


// --------------------------------------------
// READING PROGRESS BAR
// --------------------------------------------
window.addEventListener("scroll", () => {

    const progress = document.getElementById("progressBar");

    if (!progress) return;

    const totalHeight =
        document.documentElement.scrollHeight -
        window.innerHeight;

    const currentHeight = window.scrollY;

    const percentage =
        (currentHeight / totalHeight) * 100;

    progress.style.width = percentage + "%";

});


// --------------------------------------------
// BACK TO TOP
// --------------------------------------------
function backToTop() {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}


// --------------------------------------------
// SHOW / HIDE TOP BUTTON
// --------------------------------------------
window.addEventListener("scroll", () => {

    const btn = document.getElementById("topBtn");

    if (!btn) return;

    if (window.scrollY > 300) {

        btn.classList.add("show");

    }

    else {

        btn.classList.remove("show");

    }

});


// --------------------------------------------
// FADE-IN ANIMATION
// --------------------------------------------
const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("visible");

        }

    });

}, {

    threshold: 0.15

});


// --------------------------------------------
// LOAD ANIMATIONS
// --------------------------------------------
document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(

        ".question-card, .subject-card, .unit-section"

    ).forEach(item => {

        observer.observe(item);

    });

});


// --------------------------------------------
// CONSOLE MESSAGE
// --------------------------------------------
console.log(
    "%c⚡ ExamHub Loaded Successfully",
    "color:#00e5ff;font-size:16px;font-weight:bold;"
);
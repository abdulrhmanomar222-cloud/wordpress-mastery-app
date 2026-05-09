import os
import datetime
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy

# --- 1. Core Configuration ---
app = Flask(__name__)

# Cloud-friendly Database Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Use an environment variable for the DB URL if available (for production safety)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "pro_learning_hub.db")}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 2. Professional Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)
    completed_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# --- 3. High-Performance Mobile-Ready Frontend ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>EduPlus | Professional Learning Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; -webkit-tap-highlight-color: transparent; }
        .glass-effect { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
        .btn-gradient { background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); }
        .correct { background-color: #dcfce7 !important; border-color: #22c55e !important; color: #15803d !important; }
        .wrong { background-color: #fee2e2 !important; border-color: #ef4444 !important; color: #b91c1c !important; }
    </style>
</head>
<body class="p-3 md:p-8">
    <div class="max-w-3xl mx-auto space-y-6">
        <header class="glass-effect flex justify-between items-center p-4 rounded-2xl shadow-sm border border-gray-200 sticky top-4 z-50">
            <div class="flex items-center gap-2">
                <div class="bg-blue-600 p-2 rounded-lg text-white"><i class="fas fa-graduation-cap text-xl"></i></div>
                <h1 class="text-xl font-extrabold tracking-tight text-gray-900">EduPlus <span class="text-blue-600">+</span></h1>
            </div>
            <button onclick="sharePlatform()" class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-xl transition flex items-center gap-2 font-semibold">
                <i class="fas fa-share-nodes"></i><span class="hidden sm:inline">Share</span>
            </button>
        </header>

        <section class="bg-white rounded-3xl shadow-lg overflow-hidden border border-gray-100">
            <div class="aspect-video bg-black">
                <iframe class="w-full h-full" src="https://www.youtube.com/embed/rkmGNyRbQRo" frameborder="0" allowfullscreen></iframe>
            </div>
            <div class="p-6">
                <span class="bg-blue-100 text-blue-700 text-xs font-bold px-3 py-1 rounded-full uppercase">Module 1</span>
                <h2 class="text-2xl font-bold mt-2 text-gray-800">WordPress Mastery 2026</h2>
                <p class="text-gray-500 mt-1">Learn how to build high-performance websites from scratch.</p>
            </div>
        </section>

        <section class="bg-white p-6 md:p-10 rounded-3xl shadow-xl border border-gray-100 relative overflow-hidden">
            <div id="quiz-header" class="mb-8">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-bold text-gray-900">Knowledge Check</h3>
                    <span id="progress-text" class="text-sm font-semibold text-blue-600">Question 1/10</span>
                </div>
                <div class="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
                    <div id="progress-bar" class="h-full btn-gradient transition-all duration-500" style="width: 10%"></div>
                </div>
            </div>
            <div id="quiz-body">
                <h4 id="question-text" class="text-xl font-semibold text-gray-800 mb-6 min-h-[60px]">Loading question...</h4>
                <div id="options-grid" class="grid grid-cols-1 gap-3"></div>
            </div>
            <div id="quiz-footer" class="mt-8 flex justify-end">
                <button id="next-btn" onclick="loadNextQuestion()" class="hidden btn-gradient text-white px-8 py-3 rounded-2xl font-bold shadow-lg transform active:scale-95 transition">
                    Next Question <i class="fas fa-arrow-right ml-2"></i>
                </button>
            </div>
            <div id="results-view" class="hidden text-center py-10">
                <i class="fas fa-trophy text-6xl text-yellow-400 mb-4"></i>
                <h3 class="text-3xl font-bold text-gray-800">Quiz Completed!</h3>
                <p id="final-score" class="text-lg text-gray-500 mt-2 font-medium"></p>
                <button onclick="resetQuiz()" class="mt-6 bg-gray-900 text-white px-8 py-3 rounded-2xl font-bold">Restart Quiz</button>
            </div>
        </section>

        <footer class="text-center text-gray-400 py-10">
            <p class="text-sm">Directed by <b>Abdulrahman Omar</b></p>
            <p class="text-xs mt-1">Professional E-Learning Architecture © 2026</p>
        </footer>
    </div>

    <script>
        const questions = [
            { q: "What does CMS stand for?", o: ["Content Management System", "Central Module Server", "Cloud Media Storage", "Code Management Suite"], a: 0 },
            { q: "Which language is WordPress primarily built on?", o: ["Python", "PHP", "Java", "Ruby"], a: 1 },
            { q: "What is a 'Plugin' in WordPress?", o: ["A type of theme", "Additional functionality", "A hosting provider", "A security hacker"], a: 1 },
            { q: "Where is WordPress data stored?", o: ["Excel File", "Browser Cache", "Database (MySQL)", "Cloud Images"], a: 2 },
            { q: "What is the default editor in modern WordPress?", o: ["Classic", "Gutenberg", "Elementor", "Divi"], a: 1 },
            { q: "Which of these is used for SEO?", o: ["Yoast", "WooCommerce", "BuddyPress", "Contact Form 7"], a: 0 },
            { q: "What is a 'Theme' responsible for?", o: ["Database speed", "Site design/look", "Hosting costs", "Domain registration"], a: 1 },
            { q: "WordPress is Open Source. What does this mean?", o: ["It's very expensive", "Code is private", "Anyone can modify it", "It only works on Windows"], a: 2 },
            { q: "Which company created WordPress?", o: ["Google", "Microsoft", "Automattic", "Apple"], a: 2 },
            { q: "What percentage of the web uses WordPress?", o: ["Over 40%", "Less than 5%", "Exactly 10%", "Only 1%"], a: 0 }
        ];

        let currentIdx = 0;
        let score = 0;

        function sharePlatform() {
            if (navigator.share) {
                navigator.share({
                    title: 'EduPlus Learning',
                    text: 'Check out this professional WordPress course by Abdulrahman Omar!',
                    url: window.location.href
                });
            } else { alert("Share link: " + window.location.href); }
        }

        function loadQuestion() {
            const q = questions[currentIdx];
            document.getElementById('question-text').innerText = q.q;
            document.getElementById('progress-text').innerText = `Question ${currentIdx + 1}/10`;
            document.getElementById('progress-bar').style.width = `${(currentIdx + 1) * 10}%`;
            const grid = document.getElementById('options-grid');
            grid.innerHTML = '';
            document.getElementById('next-btn').classList.add('hidden');
            q.o.forEach((opt, index) => {
                const btn = document.createElement('button');
                btn.className = "w-full text-left p-4 border-2 border-gray-100 rounded-2xl font-semibold transition-all hover:border-blue-300 active:scale-[0.98]";
                btn.innerText = opt;
                btn.onclick = () => selectOption(index, btn);
                grid.appendChild(btn);
            });
        }

        function selectOption(idx, btn) {
            const correct = questions[currentIdx].a;
            const allBtns = document.querySelectorAll('#options-grid button');
            allBtns.forEach(b => b.disabled = true);
            if (idx === correct) { btn.classList.add('correct'); score++; }
            else { btn.classList.add('wrong'); allBtns[correct].classList.add('correct'); }
            document.getElementById('next-btn').classList.remove('hidden');
        }

        function loadNextQuestion() {
            currentIdx++;
            if (currentIdx < questions.length) loadQuestion();
            else showResults();
        }

        function showResults() {
            document.getElementById('quiz-header').classList.add('hidden');
            document.getElementById('quiz-body').classList.add('hidden');
            document.getElementById('next-btn').classList.add('hidden');
            document.getElementById('results-view').classList.remove('hidden');
            document.getElementById('final-score').innerText = `You scored ${score} out of ${questions.length}`;
        }

        function resetQuiz() {
            currentIdx = 0; score = 0;
            document.getElementById('quiz-header').classList.remove('hidden');
            document.getElementById('quiz-body').classList.remove('hidden');
            document.getElementById('results-view').classList.add('hidden');
            loadQuestion();
        }
        loadQuestion();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_LAYOUT)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email="admin@eduplus.com").first():
            db.session.add(User(username="Abdulrahman", email="admin@eduplus.com", password="secure_password_2026"))
            db.session.commit()
    # Host 0.0.0.0 is required for Render deployment
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

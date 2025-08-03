from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import random

WELLNESS_PROMPTS = [
    ("Stand up and stretch for a minute!", "STRETCH"),
    ("Grab some water and take a sip!", "HYDRATED"),
    ("10 shoulder rolls each way. Type OK when finished.", "OK"),
    ("Look away from the screen for 20 seconds (20-20-20 rule). Type RESTED to continue.", "RESTED"),
    ("Walk around for a minute. Type WALKED.", "WALKED"),
]
MOTIVATIONAL_QUOTES = [
    "Small steps every day. Type this to continue.",
    "Your health fuels your hustle! Type this to continue.",
    "You are more than your work. Type this to continue.",
    "Success is the sum of small efforts. Repeat this."
]
MINI_EXERCISES = [
    ("Do 10 desk push-ups! Type DONE!", "DONE"),
    ("Do 15 squats! Type SQUATS when you're done.", "SQUATS"),
    ("March in place for 60 seconds. Type DONE!", "DONE"),
]
HYDRATION = ("Refill your glass and drink. Type REFRESHED!", "REFRESHED")
EYE_REST = ("Gaze at something 20 feet away for 20 seconds. Type EYES after!", "EYES")

class TaskWindow(QDialog):
    def __init__(self, task_type):
        super().__init__()
        self.setWindowTitle("Wellness Break!")
        self.setMinimumSize(400, 200)
        layout = QVBoxLayout()
        self.input = QLineEdit()
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setStyleSheet("font-size: 16px; padding: 8px;")
        self.submit_btn.clicked.connect(self.check_answer)
        self.input.returnPressed.connect(self.check_answer)
        self.answer = ""

        if task_type == "Random Wellness Prompt":
            prompt, self.answer = random.choice(WELLNESS_PROMPTS)
            layout.addWidget(QLabel(f"🕒 {prompt}"))
        elif task_type == "Motivational Quote":
            quote = random.choice(MOTIVATIONAL_QUOTES)
            self.answer = quote
            layout.addWidget(QLabel(f"🌟 {quote}"))
        elif task_type == "Mini Exercise":
            prompt, self.answer = random.choice(MINI_EXERCISES)
            layout.addWidget(QLabel(f"🏋️ {prompt}"))
        elif task_type == "Hydration Reminder":
            layout.addWidget(QLabel(f"💧 {HYDRATION[0]}"))
            self.answer = HYDRATION[1]
        elif task_type == "Eye Rest":
            layout.addWidget(QLabel(f"👀 {EYE_REST[0]}"))
            self.answer = EYE_REST[1]
        else:
            # Fallback
            self.answer = "DONE"
            layout.addWidget(QLabel("Take a moment to breathe. Type DONE to dismiss."))

        layout.addWidget(self.input)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def check_answer(self):
        if self.input.text().strip() == self.answer:
            self.accept()
        else:
            self.input.setText("")
            self.input.setPlaceholderText("Try again...")

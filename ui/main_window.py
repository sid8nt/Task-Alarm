import json
import os
import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QTimeEdit,
    QPushButton, QListWidget, QListWidgetItem, QHBoxLayout,
    QComboBox, QLineEdit, QCheckBox, QMessageBox
)
from PyQt5.QtCore import QTime, QTimer, QDateTime, Qt
from PyQt5.QtMultimedia import QSound
from .task_window import TaskWindow

# Absolute path for your sound file
ALARM_SOUND = r"C:\Users\smane\OneDrive\Desktop\project2-2\TaskAlarmProject\ui\sound.wav"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def get_today():
    return datetime.datetime.today().strftime("%a")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Break & Wellness Assistant")
        self.setMinimumSize(700, 520)
        self.alarm_list = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_alarms)
        self.timer.start(1000)
        self.setup_ui()
        self.load_alarms()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Break Name (e.g., Hydration Break)")
        self.name_input.setStyleSheet("font-size: 24px;")

        self.time_picker = QTimeEdit()
        self.time_picker.setDisplayFormat("hh:mm AP")
        self.time_picker.setStyleSheet("font-size: 24px;")

        self.task_type_box = QComboBox()
        self.task_type_box.addItems([
            "Random Wellness Prompt", "Motivational Quote", "Mini Exercise", 
            "Hydration Reminder", "Eye Rest"
        ])
        self.task_type_box.setStyleSheet("font-size: 24px;")

        days_layout = QHBoxLayout()
        self.day_checkboxes = []
        for day in DAYS:
            checkbox = QCheckBox(day)
            checkbox.setStyleSheet("font-size: 20px;")
            self.day_checkboxes.append(checkbox)
            days_layout.addWidget(checkbox)

        self.set_alarm_btn = QPushButton("Set Break Reminder")
        self.set_alarm_btn.setStyleSheet("font-size: 20px; padding: 10px;")
        self.set_alarm_btn.clicked.connect(self.set_alarm)

        layout.addWidget(QLabel("Break/Alarm Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Time:"))
        layout.addWidget(self.time_picker)
        layout.addWidget(QLabel("Reminder Type:"))
        layout.addWidget(self.task_type_box)
        layout.addWidget(QLabel("Repeat on:"))
        layout.addLayout(days_layout)
        layout.addWidget(self.set_alarm_btn)

        # Info on why breaks matter
        info_lbl = QLabel(
            "💡 This app nudges you for regular wellness breaks. "
            "Small actions—stretch, hydrate, eye rest—can boost health and focus!"
        )
        info_lbl.setStyleSheet("color: #444; font-size: 17px; font-style:italic")
        layout.addWidget(info_lbl)

        self.alarm_list_widget = QListWidget()
        layout.addWidget(self.alarm_list_widget)

        self.delete_btn = QPushButton("Delete Selected Break")
        self.delete_btn.setStyleSheet("font-size: 20px;")
        self.delete_btn.clicked.connect(self.delete_selected_alarm)
        layout.addWidget(self.delete_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_alarm(self):
        name = self.name_input.text().strip() or "Screen Break"
        time = self.time_picker.time().toString("hh:mm AP")
        task_type = self.task_type_box.currentText()
        days = [cb.text() for cb in self.day_checkboxes if cb.isChecked()]
        alarm = {"name": name, "time": time, "task": task_type, "days": days, "active": True}
        self.alarm_list.append(alarm)

        item_text = f"{name} at {time} | {task_type} | {'/'.join(days) if days else 'Once'}"
        item = QListWidgetItem(item_text)
        item.setData(Qt.UserRole, alarm)
        self.alarm_list_widget.addItem(item)

        self.save_alarms()
        self.name_input.clear()
        for cb in self.day_checkboxes:
            cb.setChecked(False)

    def delete_selected_alarm(self):
        for item in self.alarm_list_widget.selectedItems():
            self.alarm_list_widget.takeItem(self.alarm_list_widget.row(item))
        self.save_alarms_from_list()

    def check_alarms(self):
        current_time = QDateTime.currentDateTime().toString("hh:mm AP")
        current_day = get_today()
        for i in range(self.alarm_list_widget.count()):
            item = self.alarm_list_widget.item(i)
            alarm = item.data(Qt.UserRole)
            if not alarm.get("active", True):
                continue
            if alarm["time"] == current_time and (not alarm["days"] or current_day in alarm["days"]):
                QSound.play(ALARM_SOUND)
                # Wellness-focused pop-up
                TaskWindow(alarm["task"]).exec_()
                if not alarm["days"]:
                    alarm["active"] = False
                    item.setData(Qt.UserRole, alarm)
        self.save_alarms_from_list()

    def save_alarms(self):
        with open("alarms.json", "w") as f:
            json.dump(self.alarm_list, f, indent=4)

    def save_alarms_from_list(self):
        self.alarm_list = []
        for i in range(self.alarm_list_widget.count()):
            self.alarm_list.append(self.alarm_list_widget.item(i).data(Qt.UserRole))
        self.save_alarms()

    def load_alarms(self):
        if os.path.exists("alarms.json"):
            with open("alarms.json", "r") as f:
                self.alarm_list = json.load(f)
            for alarm in self.alarm_list:
                item_text = f"{alarm['name']} at {alarm['time']} | {alarm['task']} | {'/'.join(alarm['days']) if alarm['days'] else 'Once'}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, alarm)
                self.alarm_list_widget.addItem(item)

'''
Settings for application.
'''

from PySide6.QtCore import Slot, Qt, Signal, QObject, QRect
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox,
    QHBoxLayout, QLineEdit, 
    QSlider, QLabel, QPushButton,
    QMenu
)
from PySide6.QtGui import QAction
import os, json


class Settings(QObject):
    class Variables:
        api_key = ""
        base_url = ""
        model = ""
        system_prompt = ""
        temperature = 0.7
        geometry = {"coord": [0, 0], "rect": [300, 500]}
        
    def __init__(self):
        self.variables = Settings.Variables
        self.load()
        
    def save(self, geometry: QRect = None):
        """Save settings to file."""
        data = self.get_data() or {}
        data["api_key"] = self.variables.api_key
        data["base_url"] = self.variables.base_url
        data["model"] = self.variables.model
        data["system_prompt"] = self.variables.system_prompt
        data["temperature"] = self.variables.temperature
        if geometry:
            data["geometry"] = {"coord": [geometry.x(), geometry.y()], "rect": [geometry.width(), geometry.height()]}
        with open("settings.json", "w") as f:
            json.dump(data, f, indent=4)
            
            
    def load(self):
        """Load settings from file."""
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                data = json.load(f)
                self.variables.api_key = data.get("api_key", "")
                self.variables.base_url = data.get("base_url", "")
                self.variables.model = data.get("model", "")
                self.variables.system_prompt = data.get("system_prompt", "")
                self.variables.temperature = data.get("temperature", 0.7)
                self.variables.geometry = data.get("geometry", {"coord": [0, 0], "rect": [300, 300]})
            return data
        else:
            self.save()
            
    def get_data(self) -> dict:
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                return json.load(f)
            
    def set_api_key(self, api_key: str):
        self.variables.api_key = api_key
        self.save()
        
    def set_base_url(self, base_url: str):
        self.variables.base_url = base_url
        self.save()
        
    def set_model(self, model: str):
        self.variables.model = model
        self.save()
        
    def set_system_prompt(self, system_prompt: str):
        self.variables.system_prompt = system_prompt
        self.save()
        
    def set_temperature(self, temperature: float):
        self.variables.temperature = temperature
        self.save()
        
    def set_geometry(self, geometry: QRect):
        self.variables.geometry = {"coord": [geometry.x(), geometry.y()], "rect": [geometry.width(), geometry.height()]}
        self.save(geometry)
        
    def get_geometry(self) -> QRect:
        return QRect(self.variables.geometry["coord"][0], self.variables.geometry["coord"][1], self.variables.geometry["rect"][0], self.variables.geometry["rect"][1])


class SetUI(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__()
        self.data = Settings.get_data(self)
        self.activateWindow()
        self.setFocus()
        # Components
        self.parent_box = QGroupBox()
        self.layout = QVBoxLayout()
        self.temp_layout = QHBoxLayout()
        self.parent_layout = QVBoxLayout()
        self.parent_layout.addWidget(self.parent_box)
        self.setLayout(self.parent_layout)
        
        # Components
        self.api_key = QLineEdit()
        self.base_url = QLineEdit()
        self.model = QLineEdit()
        self.system_prompt = QLineEdit()
        self.temperature = QSlider(Qt.Orientation.Horizontal)
        self.temperature_label = QLabel()
        self.temp_layout.addWidget(self.temperature)
        self.temp_layout.addWidget(self.temperature_label)
        self.close_btn = QPushButton("Okay")
        self.close_btn.setMinimumHeight(40)

        # Options Menu  
        self.menu = QMenu()
        self.options = ["gpt-3.5-turbo-0125", "gpt-4-0125-preview", "gpt-4", "gpt-4-32k"]
        for option in self.options:
            action = QAction(option)
            action.triggered.connect(lambda: self.model.setText(option))
            self.menu.addAction(action)
        self.model.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.model.customContextMenuRequested.connect(lambda: self.menu.exec_())
                
        # Placeholders
        self.api_key.setPlaceholderText("API Key")
        self.base_url.setPlaceholderText("Base URL")
        self.model.setPlaceholderText("Model")
        self.system_prompt.setPlaceholderText("System Prompt")
                
        # Set Values
        self.api_key.setText(self.data.get("api_key", ""))
        self.base_url.setText(self.data.get("base_url", ""))
        self.model.setText(self.data.get("model", ""))
        self.system_prompt.setText(self.data.get("system_prompt", ""))
        self.temperature.setValue(self.data.get("temperature", 0.7) * 10)
        self.temperature_label.setText(f"Temperature: {self.data.get('temperature', 0.7)}")
        self.temperature.setMaximum(17)
        self.temperature.setMinimum(0)
        
        self.layout.addWidget(self.api_key)
        self.layout.addWidget(self.base_url)
        self.layout.addWidget(self.model)
        self.layout.addWidget(self.system_prompt)
        self.layout.addLayout(self.temp_layout)
        self.layout.addWidget(self.close_btn)
                
        # Signals & Slots
        self.api_key.textChanged.emit(self.api_key.text())
        self.base_url.textChanged.emit(self.base_url.text())
        self.model.textChanged.emit(self.model.text())
        self.system_prompt.textChanged.emit(self.system_prompt.text())
        self.temperature.valueChanged.emit(self.temperature.value()/10)
        self.close_btn.clicked.connect(self.close)
        self.temperature.valueChanged.connect(self.update_temperature)
        
        # Frameless Window
        self.parent_box.setLayout(self.layout)
        self.load_stylesheet()
        self.set_window_flags()
        
        # Set position to parent 
        self.setGeometry(parent.geometry().x(), parent.geometry().y(), 300, 300)

    def update_temperature(self, value: int):
        self.temperature_label.setText(f"Temperature: {value/10}")

    def self_has_focus(self, widget: QWidget = None):
        if not widget:
            widget = self
        # Recursively check
        try:
            if widget.hasFocus():
                return True
        except:
            return False
        
        if widget.children() == []:
            return False
        for child in widget.children():
            if self.self_has_focus(child):
                return True
        return False
        
    def load_stylesheet(self, style_sheet: str = "form_styles.qss"):
        with open("styles/"+style_sheet, 'r') as qss:
            style_sheet = qss.read()
        self.setStyleSheet(style_sheet)
        
    def set_window_flags(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        


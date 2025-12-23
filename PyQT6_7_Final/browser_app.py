from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class BrowserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Browser")
        self.setWindowIcon(QIcon("icons/browser.webp"))
        self.resize(1000, 700)

        self.view = QWebEngineView()
        self.view.setUrl(QUrl("https://www.google.com"))

        self.url_bar = QLineEdit()
        self.url_bar.setText("https://www.google.com")
        self.url_bar.returnPressed.connect(self.load_url)

        layout = QVBoxLayout(self)
        layout.addWidget(self.url_bar)
        layout.addWidget(self.view)

    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.view.setUrl(QUrl(url))

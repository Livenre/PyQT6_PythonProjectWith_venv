import os
import sys

from PyQt6.QtGui import QPixmap, QIcon, QPainter, QBrush, QColor
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QMenu, QToolButton,
                             QFileDialog, QWidget,
                             QVBoxLayout, QGraphicsBlurEffect
                             )
from PyQt6.QtCore import Qt, QSize, QSettings, QUrl
from PyQt6 import uic

from paint_app import PaintApp
from desktop_icon import DesktopIcon
from taskbar import TaskBar

from browser_app import BrowserApp


class Desktop(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("miniOS.ui", self)
        self.setWindowTitle("MiniOS")
        self.resize(1000, 720)

        self.apps = {}

        # if self.statusBar():
        #     self.statusBar().hide()
        # if self.toolBar:
        #     self.toolBar.hide()

        # --- новая структура окна (desktop + taskbar) ---
        central = QWidget(self)
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # рабочий стол (обои + иконки)
        layout.addWidget(self.wallpaperLabel, 1)

        # нижняя панель
        self.taskbar = TaskBar(self)
        layout.addWidget(self.taskbar)
        # ----------------------
        self.taskbar.btn_start.clicked.connect(self.open_start_menu)

        self.setWindowIcon(QIcon("icons/minios.jpg"))

        self.wallpaperLabel.setScaledContents(True)
        self.wallpaperLabel.setSizePolicy(
            self.wallpaperLabel.sizePolicy().Policy.Ignored,
            self.wallpaperLabel.sizePolicy().Policy.Ignored
        )

        # --- настройки приложения ---
        self.settings = QSettings("MiniOS", "Desktop")
        self.wallpaper_source = None  # ← добавлено
        self.load_wallpaper()
        self.update_taskbar_background()

        # разрешаем контекстное меню для рабочего стола
        self.wallpaperLabel.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.wallpaperLabel.customContextMenuRequested.connect(
            self.show_desktop_context_menu
        )

        # Paint (у тебя actionPaint уже есть в .ui)
        self.actionPaint.triggered.connect(self.open_paint)
        self.actionChangeWallpaper.triggered.connect(self.change_wallpaper)

        # # --- создаём "Пуск" как кнопку с меню ---
        # self.start_menu = QMenu(self)
        # self.start_menu.addAction(self.actionPaint)  # пока пусть там будет Paint
        # self.start_menu.addAction(self.actionChangeWallpaper)
        #
        # self.btnStart = QToolButton(self)
        # self.btnStart.setText("Пуск")
        # self.btnStart.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        # self.btnStart.setMenu(self.start_menu)
        #
        # # --- вставляем кнопку в toolbar ---
        # self.toolBar.insertWidget(self.toolBar.actions()[0], self.btnStart)

        # --- иконка Paint на рабочем столе ---
        self.paint_icon = DesktopIcon(
            icon_path="icons/paint.jpg",
            text="Paint",
            #parent=self.centralWidget()
            parent = self.wallpaperLabel
        )

        self.paint_icon.move(20, 20)
        self.paint_icon.activated.connect(self.open_paint)
        self.paint_icon.show()

        # При наведении на ярлык, курсор меняется на готовность нажать
        # self.paint_icon.setCursor(Qt.CursorShape.PointingHandCursor)

        # --- иконка Browser на рабочем столе ---
        self.browser_icon = DesktopIcon(
            icon_path="icons/browser.webp",
            text="Browser",
            parent=self.wallpaperLabel
        )

        self.browser_icon.move(120, 20)
        self.browser_icon.activated.connect(self.open_browser)
        self.browser_icon.show()

    def open_app(self, key, app_cls, icon_path):
        window = self.apps.get(key)

        if window is None:
            window = app_cls()
            window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

            self.taskbar.add_app(window, icon_path)
            window.destroyed.connect(lambda: self.on_app_destroyed(key))

            self.apps[key] = window

        window.show()
        window.raise_()
        window.activateWindow()

    def on_app_destroyed(self, key):
        self.apps[key] = None


    def open_paint(self):
        self.open_app(
            key="paint",
            app_cls=PaintApp,
            icon_path="icons/paint.jpg"
        )

    def open_browser(self):
        self.open_app(
            key="minibrowser",
            app_cls=BrowserApp,
            icon_path="icons/browser.webp"
        )

    def change_wallpaper(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать обои",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.jfif *.webp)"
        )

        if not file_path:
            return

        self.settings.setValue("wallpaper_path", file_path)

        pixmap = QPixmap(file_path)
        self.wallpaperLabel.setPixmap(pixmap)
        self.update_taskbar_background()

    def load_wallpaper(self):
        path = self.settings.value("wallpaper_path", "")

        if path and os.path.exists(path):
            pixmap = QPixmap(path)
            self.wallpaperLabel.setPixmap(pixmap)


    def show_desktop_context_menu(self, pos):
        menu = QMenu(self)
        menu.addAction(self.actionChangeWallpaper)

        global_pos = self.wallpaperLabel.mapToGlobal(pos)
        menu.exec(global_pos)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        desktop = self.centralWidget()

        for icon in desktop.findChildren(DesktopIcon):
            max_x = desktop.width() - icon.width()
            max_y = desktop.height() - icon.height()

            x = icon.x()
            y = icon.y()

            moved = False

            if x > max_x:
                x = max_x
                moved = True
            if y > max_y:
                y = max_y
                moved = True

            if x < 0:
                x = 0
                moved = True
            if y < 0:
                y = 0
                moved = True

            if moved:
                icon.move(x, y)

        self.update_taskbar_background()

    def open_start_menu(self):
        menu = QMenu(self)

        act_paint = menu.addAction(QIcon("icons/paint.jpg"), "Paint")
        act_browser = menu.addAction(QIcon("icons/browser.webp"), "Browser")

        menu.addSeparator()

        act_exit = menu.addAction(QIcon("icons/power.png"), "Завершить работу")

        action = menu.exec(
            self.taskbar.btn_start.mapToGlobal(
                self.taskbar.btn_start.rect().topLeft()
            )
        )

        if action == act_paint:
            self.open_paint()
        elif action == act_browser:
            self.open_browser()
        elif action == act_exit:
            QApplication.quit()

    def update_taskbar_background(self):
        pixmap = self.wallpaperLabel.pixmap()
        if not pixmap:
            return

        bar_height = self.taskbar.height()
        w = self.wallpaperLabel.width()
        h = self.wallpaperLabel.height()

        # берём нижнюю часть обоев
        cropped = pixmap.copy(0, h - bar_height, w, bar_height)

        # лёгкое затемнение + "стекло"
        blurred = QPixmap(cropped.size())
        blurred.fill(Qt.GlobalColor.transparent)

        painter = QPainter(blurred)
        painter.drawPixmap(0, 0, cropped)
        painter.fillRect(
            blurred.rect(),
            QColor(255, 255, 255, 120)
        )
        painter.end()

        palette = self.taskbar.palette()
        palette.setBrush(self.taskbar.backgroundRole(), QBrush(blurred))
        self.taskbar.setAutoFillBackground(True)
        self.taskbar.setPalette(palette)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("MiniOS")
    app.setOrganizationName("MiniOS")

    window = Desktop()
    window.show()
    sys.exit(app.exec())

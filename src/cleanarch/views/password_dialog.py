"""
Модальный диалог запроса пароля суперпользователя (sudo) с проверкой.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib
import subprocess
import threading
from typing import Callable

class PasswordDialog:
    def __init__(self, parent_window: Gtk.Window, on_success: Callable[[str], None]):
        self.parent_window = parent_window
        self.on_success = on_success

        self.dialog = Adw.AlertDialog()
        self.dialog.set_heading("Требуются права администратора")
        self.dialog.set_body("Для очистки системных кэшей и логов введите пароль вашей учётной записи:")

        # Контейнер для поля ввода и ошибки
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_start(8)
        box.set_margin_end(8)
        box.set_margin_top(4)
        box.set_margin_bottom(4)

        self.entry = Gtk.PasswordEntry()
        self.entry.set_show_peek_icon(True)
        self.entry.set_activates_default(True)
        box.append(self.entry)

        # Метка ошибки
        self.error_label = Gtk.Label()
        self.error_label.add_css_class("error")
        self.error_label.set_visible(False)
        box.append(self.error_label)

        # Спиннер проверки
        self.spinner = Gtk.Spinner()
        self.spinner.set_visible(False)
        box.append(self.spinner)

        self.dialog.set_extra_child(box)

        # Кнопки
        self.dialog.add_response("cancel", "Отмена")
        self.dialog.add_response("confirm", "Подтвердить")
        self.dialog.set_response_appearance("confirm", Adw.ResponseAppearance.SUGGESTED)
        self.dialog.set_default_response("confirm")

        self.dialog.connect("response", self._on_response)

    def present(self):
        self.dialog.present(self.parent_window)
        # Фокус на поле ввода после отображения
        GLib.idle_add(self.entry.grab_focus)

    def _on_response(self, _dialog, response: str):
        if response == "confirm":
            password = self.entry.get_text()
            if not password:
                self.error_label.set_text("Пожалуйста, введите пароль")
                self.error_label.set_visible(True)
                self.present()
                return

            self.error_label.set_visible(False)
            self.spinner.set_visible(True)
            self.spinner.start()

            # Проверяем пароль в фоне
            def check_worker():
                try:
                    proc = subprocess.run(
                        ["sudo", "-S", "-k", "-v"],
                        input=f"{password}\n",
                        capture_output=True,
                        text=True,
                        timeout=6
                    )
                    success = (proc.returncode == 0)
                except Exception:
                    success = False

                GLib.idle_add(self._on_check_complete, success, password)

            threading.Thread(target=check_worker, daemon=True).start()

    def _on_check_complete(self, success: bool, password: str):
        self.spinner.stop()
        self.spinner.set_visible(False)

        if success:
            if self.on_success:
                self.on_success(password)
        else:
            self.error_label.set_text("❌ Неверный пароль. Попробуйте снова.")
            self.error_label.set_visible(True)
            self.entry.set_text("")
            self.present()

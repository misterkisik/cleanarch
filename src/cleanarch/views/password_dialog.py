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

class PasswordDialog(Adw.Window):
    def __init__(self, parent_window: Gtk.Window, on_success: Callable[[str], None]):
        super().__init__(transient_for=parent_window, modal=True)
        self.on_success = on_success
        self.set_title("Права администратора")
        self.set_default_size(380, 260)
        self.set_resizable(False)
        self.set_destroy_with_parent(True)

        toolbar_view = Adw.ToolbarView()
        self.set_content(toolbar_view)

        # HeaderBar
        header_bar = Adw.HeaderBar()
        header_bar.set_show_start_title_buttons(False)
        header_bar.set_show_end_title_buttons(False)

        cancel_btn = Gtk.Button(label="Отмена")
        cancel_btn.add_css_class("flat")
        cancel_btn.connect("clicked", lambda _: self.close())
        header_bar.pack_start(cancel_btn)

        self.confirm_btn = Gtk.Button(label="Подтвердить")
        self.confirm_btn.add_css_class("suggested-action")
        self.confirm_btn.connect("clicked", lambda _: self._on_confirm())
        header_bar.pack_end(self.confirm_btn)

        toolbar_view.add_top_bar(header_bar)

        # Содержимое
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        content_box.set_margin_top(16)
        content_box.set_margin_bottom(16)

        # Иконка ключа
        icon = Gtk.Image.new_from_icon_name("dialog-password-symbolic")
        icon.set_pixel_size(48)
        icon.add_css_class("accent")
        content_box.append(icon)

        # Пояснение
        title_label = Gtk.Label(label="Требуются права администратора")
        title_label.add_css_class("title-3")
        content_box.append(title_label)

        desc_label = Gtk.Label(
            label="Для очистки системных кэшей и логов введите пароль вашей учётной записи:"
        )
        desc_label.set_wrap(True)
        desc_label.set_justify(Gtk.Justification.CENTER)
        desc_label.add_css_class("dim-label")
        desc_label.add_css_class("caption")
        content_box.append(desc_label)

        # Поле ввода пароля
        self.entry = Gtk.PasswordEntry()
        self.entry.set_show_peek_icon(True)
        self.entry.connect("activate", lambda _: self._on_confirm())
        content_box.append(self.entry)

        # Ошибка
        self.error_label = Gtk.Label()
        self.error_label.add_css_class("error")
        self.error_label.set_visible(False)
        content_box.append(self.error_label)

        # Спиннер
        self.spinner = Gtk.Spinner()
        self.spinner.set_visible(False)
        toolbar_view.set_content(content_box)
        self.set_focus(self.entry)

    def present_dialog(self):
        self.present()

    def _on_confirm(self):
        password = self.entry.get_text()
        if not password:
            self.error_label.set_text("Пожалуйста, введите пароль")
            self.error_label.set_visible(True)
            self.set_focus(self.entry)
            return

        self.error_label.set_visible(False)
        self.spinner.set_visible(True)
        self.spinner.start()
        self.confirm_btn.set_sensitive(False)
        self.entry.set_sensitive(False)

        def check_worker():
            try:
                proc = subprocess.run(
                    ["sudo", "-S", "-v"],
                    input=f"{password}\n",
                    capture_output=True,
                    text=True,
                    timeout=6
                )
                success = (proc.returncode == 0)
            except Exception:
                success = False

            if not success:
                try:
                    subprocess.run(["faillock", "--reset"], capture_output=True)
                except Exception:
                    pass

            GLib.idle_add(self._on_check_complete, success, password)

        threading.Thread(target=check_worker, daemon=True).start()

    def _on_check_complete(self, success: bool, password: str):
        self.spinner.stop()
        self.spinner.set_visible(False)
        self.confirm_btn.set_sensitive(True)
        self.entry.set_sensitive(True)

        if success:
            self.close()
            if self.on_success:
                self.on_success(password)
        else:
            self.error_label.set_text("❌ Неверный пароль. Попробуйте снова.")
            self.error_label.set_visible(True)
            self.entry.set_text("")
            self.set_focus(self.entry)

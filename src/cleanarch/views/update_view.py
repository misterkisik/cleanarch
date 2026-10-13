"""
Представление обновления компонентов Arch Linux и AUR.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
import os
import shutil
from typing import Callable, Optional
from cleanarch.cleaner import build_update_script
from cleanarch.views.password_dialog import PasswordDialog

class UpdateView(Adw.PreferencesPage):
    def __init__(
        self,
        on_start_update: Callable[[str], None],
        on_toast: Callable[[str], None]
    ):
        super().__init__()
        self.on_start_update = on_start_update
        self.on_toast = on_toast

        group = Adw.PreferencesGroup()
        group.set_title("Обновление системы и репозиториев")
        group.set_description(
            "Регулярное обновление обеспечивает безопасность и актуальность вашего ПО в Arch Linux."
        )

        # 1. Полное обновление pacman + yay
        full_row = Adw.ActionRow()
        full_row.set_title("Полное обновление (pacman + AUR)")
        full_row.set_subtitle("Синхронизирует репозитории и обновляет все пакеты системы и пользовательские программы AUR")
        full_row.set_icon_name("software-update-available-symbolic")

        full_btn = Gtk.Button(label="Обновить систему")
        full_btn.set_valign(Gtk.Align.CENTER)
        full_btn.add_css_class("suggested-action")
        full_btn.connect("clicked", lambda _: self._run_task("full_update"))
        full_row.add_suffix(full_btn)
        full_row.set_activatable_widget(full_btn)
        group.add(full_row)

        # 2. Обновление ключей archlinux-keyring
        keyring_row = Adw.ActionRow()
        keyring_row.set_title("Обновить ключи безопасности (archlinux-keyring)")
        keyring_row.set_subtitle("Исправляет частые ошибки 'corrupted package / invalid PGP signature' перед обновлением")
        keyring_row.set_icon_name("dialog-password-symbolic")

        keyring_btn = Gtk.Button(label="Обновить ключи")
        keyring_btn.set_valign(Gtk.Align.CENTER)
        keyring_btn.add_css_class("flat")
        keyring_btn.connect("clicked", lambda _: self._run_task("keyring"))
        keyring_row.add_suffix(keyring_btn)
        keyring_row.set_activatable_widget(keyring_btn)
        group.add(keyring_row)

        # 3. Flatpak обновление (если установлен)
        if shutil.which("flatpak"):
            flatpak_row = Adw.ActionRow()
            flatpak_row.set_title("Обновить приложения Flatpak")
            flatpak_row.set_subtitle("Загружает последние версии установленных Flatpak программ и сред выполнения")
            flatpak_row.set_icon_name("application-x-executable-symbolic")

            flatpak_btn = Gtk.Button(label="Обновить Flatpak")
            flatpak_btn.set_valign(Gtk.Align.CENTER)
            flatpak_btn.add_css_class("flat")
            flatpak_btn.connect("clicked", lambda _: self._run_task("flatpak"))
            flatpak_row.add_suffix(flatpak_btn)
            flatpak_row.set_activatable_widget(flatpak_btn)
            group.add(flatpak_row)

        self.add(group)

    def _run_task(self, task: str):
        if task in ("full_update", "keyring") and os.geteuid() != 0:
            def on_pw_success(password: str):
                script = build_update_script(task, has_sudo_pass=True)
                if self.on_start_update:
                    self.on_start_update(script, password)

            dlg = PasswordDialog(self.get_root(), on_success=on_pw_success)
            dlg.present()
        else:
            script = build_update_script(task, has_sudo_pass=False)
            if self.on_start_update:
                self.on_start_update(script, None)

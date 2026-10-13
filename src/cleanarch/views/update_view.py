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
from cleanarch.i18n import tr

class UpdateView(Adw.PreferencesPage):
    def __init__(
        self,
        on_start_update: Callable[[str], None],
        on_toast: Callable[[str], None]
    ):
        super().__init__()
        self.on_start_update = on_start_update
        self.on_toast = on_toast

        self.group = Adw.PreferencesGroup()
        self.group.set_title(tr("update_title"))
        self.group.set_description(tr("update_desc"))

        # 1. Полное обновление pacman + yay
        self.full_row = Adw.ActionRow()
        self.full_row.set_title(tr("up_full_title"))
        self.full_row.set_subtitle(tr("up_full_desc"))
        self.full_row.set_icon_name("software-update-available-symbolic")

        self.full_btn = Gtk.Button(label=tr("up_full_btn"))
        self.full_btn.set_valign(Gtk.Align.CENTER)
        self.full_btn.add_css_class("suggested-action")
        self.full_btn.connect("clicked", lambda _: self._run_task("full_update"))
        self.full_row.add_suffix(self.full_btn)
        self.full_row.set_activatable_widget(self.full_btn)
        self.group.add(self.full_row)

        # 2. Обновление ключей archlinux-keyring
        self.keyring_row = Adw.ActionRow()
        self.keyring_row.set_title(tr("up_keyring_title"))
        self.keyring_row.set_subtitle(tr("up_keyring_desc"))
        self.keyring_row.set_icon_name("dialog-password-symbolic")

        self.keyring_btn = Gtk.Button(label=tr("up_keyring_btn"))
        self.keyring_btn.set_valign(Gtk.Align.CENTER)
        self.keyring_btn.add_css_class("suggested-action")
        self.keyring_btn.connect("clicked", lambda _: self._run_task("keyring"))
        self.keyring_row.add_suffix(self.keyring_btn)
        self.keyring_row.set_activatable_widget(self.keyring_btn)
        self.group.add(self.keyring_row)

        # 3. Flatpak обновление (если установлен)
        self.flatpak_row = None
        self.flatpak_btn = None
        if shutil.which("flatpak"):
            self.flatpak_row = Adw.ActionRow()
            self.flatpak_row.set_title(tr("up_flatpak_title"))
            self.flatpak_row.set_subtitle(tr("up_flatpak_desc"))
            self.flatpak_row.set_icon_name("application-x-executable-symbolic")

            self.flatpak_btn = Gtk.Button(label=tr("up_flatpak_btn"))
            self.flatpak_btn.set_valign(Gtk.Align.CENTER)
            self.flatpak_btn.add_css_class("suggested-action")
            self.flatpak_btn.connect("clicked", lambda _: self._run_task("flatpak"))
            self.flatpak_row.add_suffix(self.flatpak_btn)
            self.flatpak_row.set_activatable_widget(self.flatpak_btn)
            self.group.add(self.flatpak_row)

        self.add(self.group)

    def retranslate(self):
        """Обновляет все заголовки и кнопки страницы обновления при смене языка."""
        self.group.set_title(tr("update_title"))
        self.group.set_description(tr("update_desc"))

        self.full_row.set_title(tr("up_full_title"))
        self.full_row.set_subtitle(tr("up_full_desc"))
        self.full_btn.set_label(tr("up_full_btn"))

        self.keyring_row.set_title(tr("up_keyring_title"))
        self.keyring_row.set_subtitle(tr("up_keyring_desc"))
        self.keyring_btn.set_label(tr("up_keyring_btn"))

        if self.flatpak_row and self.flatpak_btn:
            self.flatpak_row.set_title(tr("up_flatpak_title"))
            self.flatpak_row.set_subtitle(tr("up_flatpak_desc"))
            self.flatpak_btn.set_label(tr("up_flatpak_btn"))

    def _run_task(self, task: str):
        if task in ("full_update", "keyring") and os.geteuid() != 0:
            def on_pw_success(password: str):
                script = build_update_script(task, has_sudo_pass=True)
                if self.on_start_update:
                    self.on_start_update(script, password)

            dlg = PasswordDialog(self.get_root(), on_success=on_pw_success)
            dlg.present_dialog()
        else:
            script = build_update_script(task, has_sudo_pass=False)
            if self.on_start_update:
                self.on_start_update(script, None)

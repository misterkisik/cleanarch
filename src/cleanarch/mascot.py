"""
Виджет отображения маскота (персонажа) и диалогового блока статуса.
"""

import os
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gdk
from typing import Optional

from cleanarch.i18n import tr

def find_mascot_path() -> Optional[str]:
    """Находит файл изображения маскота в системе или локальном каталоге."""
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "mascot.png"),
        "/usr/share/cleanarch/mascot.png",
        "/home/misterkisik/Загрузки/Dwt4vx9V-Photoroom.png",
        os.path.expanduser("~/Загрузки/Dwt4vx9V-Photoroom.png"),
    ]
    for p in candidates:
        abs_p = os.path.abspath(p)
        if os.path.exists(abs_p):
            return abs_p
    return None

class MascotWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_size_request(280, -1)
        self.set_margin_start(16)
        self.set_margin_end(16)
        self.set_margin_top(16)
        self.set_margin_bottom(16)

        self._current_mood = "idle"
        self._current_extra = ""

        # 1. Диалоговое облачко (реплика персонажа)
        self.bubble_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.bubble_box.add_css_class("card")
        self.bubble_box.set_margin_bottom(8)

        # Заголовок облачка
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        header_box.set_margin_start(12)
        header_box.set_margin_end(12)
        header_box.set_margin_top(10)
        
        icon = Gtk.Image.new_from_icon_name("starred-symbolic")
        icon.add_css_class("accent")
        header_box.append(icon)

        self.name_label = Gtk.Label(label=tr("mascot_name"))
        self.name_label.add_css_class("heading")
        header_box.append(self.name_label)
        self.bubble_box.append(header_box)

        # Текст реплики
        self.phrase_label = Gtk.Label()
        self.phrase_label.set_wrap(True)
        self.phrase_label.set_justify(Gtk.Justification.LEFT)
        self.phrase_label.set_margin_start(12)
        self.phrase_label.set_margin_end(12)
        self.phrase_label.set_margin_bottom(8)
        self.phrase_label.add_css_class("body")
        self.bubble_box.append(self.phrase_label)

        # Дополнительный статус (например, освобождено места)
        self.status_label = Gtk.Label()
        self.status_label.set_wrap(True)
        self.status_label.set_margin_start(12)
        self.status_label.set_margin_end(12)
        self.status_label.set_margin_bottom(10)
        self.status_label.add_css_class("caption")
        self.status_label.add_css_class("dim-label")
        self.bubble_box.append(self.status_label)

        self.append(self.bubble_box)

        # 2. Изображение персонажа
        mascot_path = find_mascot_path()
        if mascot_path and os.path.exists(mascot_path):
            self.picture = Gtk.Picture.new_for_filename(mascot_path)
            self.picture.set_can_shrink(True)
            if hasattr(Gtk, "ContentFit"):
                self.picture.set_content_fit(Gtk.ContentFit.CONTAIN)
            self.picture.set_vexpand(True)
            self.picture.set_hexpand(True)
            self.append(self.picture)
        else:
            fallback_label = Gtk.Label(label="[Маскот не найден]")
            fallback_label.set_vexpand(True)
            self.append(fallback_label)

        # Начальная фраза
        self.set_mood("idle")

    def retranslate(self):
        """Обновляет имя маскота и реплику при смене языка."""
        self.name_label.set_text(tr("mascot_name"))
        self.set_mood(self._current_mood, self._current_extra)

    def set_speech(self, phrase: str, subtitle: str = ""):
        """Устанавливает текст реплики и подпись."""
        self.phrase_label.set_text(phrase)
        self.status_label.set_text(subtitle)
        self.status_label.set_visible(bool(subtitle))

    def set_mood(self, mood: str, extra_info: str = ""):
        """Переключает реплику в зависимости от текущего состояния программы."""
        self._current_mood = mood
        self._current_extra = extra_info

        if mood == "idle":
            self.set_speech(
                tr("mascot_idle"),
                tr("mascot_ready")
            )
        elif mood == "scanning":
            self.set_speech(
                tr("mascot_scanning"),
                tr("mascot_scanning_sub")
            )
        elif mood == "scanned":
            self.set_speech(
                tr("mascot_scanned", extra=extra_info),
                tr("mascot_scanned_sub", extra=extra_info)
            )
        elif mood == "cleaning":
            self.set_speech(
                tr("mascot_cleaning"),
                tr("mascot_cleaning_sub")
            )
        elif mood == "done":
            self.set_speech(
                tr("mascot_done"),
                extra_info or tr("mascot_done_sub")
            )
        elif mood == "updating":
            self.set_speech(
                tr("mascot_updating"),
                tr("mascot_updating_sub")
            )
        elif mood == "error":
            self.set_speech(
                tr("mascot_error"),
                tr("mascot_error_sub")
            )

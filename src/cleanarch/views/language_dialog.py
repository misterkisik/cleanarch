"""
Диалоговое окно выбора языка при первом запуске CleanArch.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from typing import Callable, Optional
from cleanarch.i18n import SUPPORTED_LANGUAGES, tr, set_language, get_current_language

LANG_INFO = [
    ("ru", "🇷🇺  Русский", "Русский интерфейс программы"),
    ("en", "🇬🇧  English", "English user interface"),
    ("es", "🇪🇸  Español", "Interfaz en español"),
    ("fr", "🇫🇷  Français", "Interface en français"),
]

class FirstRunLanguageDialog(Adw.Window):
    def __init__(self, parent_window: Gtk.Window, on_completed: Optional[Callable[[str], None]] = None):
        super().__init__(transient_for=parent_window, modal=True)
        self.on_completed = on_completed
        self.set_title("CleanArch")
        self.set_default_size(440, 520)
        self.set_resizable(False)
        self.set_destroy_with_parent(True)

        self.selected_lang = get_current_language()
        if self.selected_lang not in SUPPORTED_LANGUAGES:
            self.selected_lang = "ru"

        toolbar_view = Adw.ToolbarView()
        self.set_content(toolbar_view)

        # HeaderBar без лишних кнопок закрытия
        header_bar = Adw.HeaderBar()
        header_bar.set_show_start_title_buttons(False)
        header_bar.set_show_end_title_buttons(False)
        toolbar_view.add_top_bar(header_bar)

        # Основной контейнер
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_hexpand(True)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content.set_margin_start(24)
        content.set_margin_end(24)
        content.set_margin_top(20)
        content.set_margin_bottom(24)

        # Иконка приложения / локали
        icon = Gtk.Image.new_from_icon_name("preferences-desktop-locale-symbolic")
        icon.set_pixel_size(56)
        icon.add_css_class("accent")
        content.append(icon)

        # Заголовок
        self.title_label = Gtk.Label(label=tr("welcome_title"))
        self.title_label.add_css_class("title-2")
        self.title_label.set_wrap(True)
        self.title_label.set_justify(Gtk.Justification.CENTER)
        content.append(self.title_label)

        # Подзаголовок
        self.desc_label = Gtk.Label(label=tr("welcome_subtitle"))
        self.desc_label.add_css_class("body")
        self.desc_label.add_css_class("dim-label")
        self.desc_label.set_wrap(True)
        self.desc_label.set_justify(Gtk.Justification.CENTER)
        content.append(self.desc_label)

        # Группа карточек выбора языков
        group = Adw.PreferencesGroup()
        self.radio_buttons = {}
        first_radio = None

        for code, name, desc in LANG_INFO:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(desc)

            radio = Gtk.CheckButton()
            if first_radio is None:
                first_radio = radio
            else:
                radio.set_group(first_radio)

            if code == self.selected_lang:
                radio.set_active(True)

            radio.connect("toggled", self._on_radio_toggled, code)
            row.add_prefix(radio)
            row.set_activatable_widget(radio)
            self.radio_buttons[code] = radio
            group.add(row)

        content.append(group)

        # Кнопка подтверждения
        self.continue_btn = Gtk.Button(label=tr("btn_continue"))
        self.continue_btn.add_css_class("suggested-action")
        self.continue_btn.add_css_class("pill")
        self.continue_btn.set_size_request(-1, 46)
        self.continue_btn.connect("clicked", self._on_continue_clicked)
        content.append(self.continue_btn)

        scroll.set_child(content)
        toolbar_view.set_content(scroll)

    def _on_radio_toggled(self, button: Gtk.CheckButton, code: str):
        if button.get_active():
            self.selected_lang = code
            # Живой предпросмотр языка в диалоге
            set_language(code, first_run_done=False)
            self.title_label.set_text(tr("welcome_title"))
            self.desc_label.set_text(tr("welcome_subtitle"))
            self.continue_btn.set_label(tr("btn_continue"))

    def _on_continue_clicked(self, _btn):
        set_language(self.selected_lang, first_run_done=True)
        self.close()
        if self.on_completed:
            self.on_completed(self.selected_lang)

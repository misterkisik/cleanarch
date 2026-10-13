"""
Главное окно CleanArch: слева маскот с репликами, справа разделы управления и консоль.
"""

import os
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GObject, Gdk, GLib
from cleanarch.mascot import MascotWidget
from cleanarch.views.clean_view import CleanView
from cleanarch.views.update_view import UpdateView
from cleanarch.views.terminal_view import TerminalView
from cleanarch.views.language_dialog import FirstRunLanguageDialog
from cleanarch.i18n import tr, set_language, get_current_language, SUPPORTED_LANGUAGES, is_first_run

class CleanArchWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(tr("app_title"))
        self.set_default_size(980, 720)

        # Регистрация путей к иконке в IconTheme
        display = Gdk.Display.get_default()
        if display:
            icon_theme = Gtk.IconTheme.get_for_display(display)
            search_dirs = [
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data")),
                os.path.expanduser("~/.local/share/icons/hicolor"),
                os.path.expanduser("~/.local/share/pixmaps"),
                "/usr/share/icons/hicolor",
                "/usr/share/pixmaps",
            ]
            for d in search_dirs:
                if os.path.exists(d):
                    icon_theme.add_search_path(d)

        # Оверлей для тостов
        self.toast_overlay = Adw.ToastOverlay()
        self.set_content(self.toast_overlay)

        # ToolbarView
        toolbar_view = Adw.ToolbarView()
        self.toast_overlay.set_child(toolbar_view)

        # Стек страниц справа
        self.view_stack = Adw.ViewStack()

        # Маскот (слева)
        self.mascot = MascotWidget()

        # Терминальный лог
        self.terminal_view = TerminalView(on_toast=self.show_toast)

        # Страница очистки
        self.clean_view = CleanView(
            on_start_clean=self._on_start_clean,
            on_status_change=self._on_status_change,
            on_toast=self.show_toast
        )

        # Страница обновления
        self.update_view = UpdateView(
            on_start_update=self._on_start_update,
            on_toast=self.show_toast
        )

        # Добавление страниц в стек
        self.page_clean = self.view_stack.add_titled_with_icon(
            self.clean_view,
            "clean",
            tr("tab_clean"),
            "edit-clear-all-symbolic"
        )
        self.page_update = self.view_stack.add_titled_with_icon(
            self.update_view,
            "update",
            tr("tab_update"),
            "software-update-available-symbolic"
        )
        self.page_terminal = self.view_stack.add_titled_with_icon(
            self.terminal_view,
            "terminal",
            tr("tab_terminal"),
            "utilities-terminal-symbolic"
        )

        # Переключатель в шапке
        self.title_switcher = Adw.ViewSwitcherTitle(stack=self.view_stack)
        self.title_switcher.set_title(tr("app_title"))
        self.title_switcher.set_subtitle(tr("app_subtitle"))

        # HeaderBar
        header_bar = Adw.HeaderBar()
        header_bar.set_title_widget(self.title_switcher)

        # Меню в шапке
        self.menu_button = Gtk.MenuButton()
        self.menu_button.set_icon_name("open-menu-symbolic")
        self.menu_button.set_tooltip_text(tr("menu_about"))
        header_bar.pack_end(self.menu_button)

        toolbar_view.add_top_bar(header_bar)

        # Основной макет: слева маскот, справа функционал
        main_h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # Левая колонка
        main_h_box.append(self.mascot)

        # Разделитель
        sep = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        main_h_box.append(sep)

        # Правая колонка
        self.view_stack.set_hexpand(True)
        self.view_stack.set_vexpand(True)
        main_h_box.append(self.view_stack)

        toolbar_view.set_content(main_h_box)

        # Регистрация действий окна и построение меню
        self._setup_actions()
        self._build_menu()

        # Проверка первого запуска для выбора языка
        GLib.idle_add(self._check_first_run)

    def _check_first_run(self):
        if is_first_run():
            dlg = FirstRunLanguageDialog(self, on_completed=self._on_first_run_completed)
            dlg.present()
        return False

    def _on_first_run_completed(self, lang: str):
        self.retranslate()
        self._build_menu()
        self.show_toast(tr("toast_lang_changed"))

    def _setup_actions(self):
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about_activated)
        self.add_action(about_action)

        set_lang_action = Gio.SimpleAction.new("set_lang", GLib.VariantType.new("s"))
        set_lang_action.connect("activate", self._on_set_lang)
        self.add_action(set_lang_action)

    def _build_menu(self):
        menu = Gio.Menu()

        lang_menu = Gio.Menu()
        lang_items = [
            ("ru", "🇷🇺 Русский"),
            ("en", "🇬🇧 English"),
            ("es", "🇪🇸 Español"),
            ("fr", "🇫🇷 Français"),
        ]
        curr = get_current_language()
        for code, name in lang_items:
            prefix = "✓ " if code == curr else "    "
            item = Gio.MenuItem.new(f"{prefix}{name}", None)
            item.set_action_and_target_value("win.set_lang", GLib.Variant.new_string(code))
            lang_menu.append_item(item)

        menu.append_submenu(tr("menu_language"), lang_menu)
        menu.append(tr("menu_about"), "win.about")
        self.menu_button.set_menu_model(menu)

    def _on_set_lang(self, _action, param):
        lang = param.get_string()
        if lang in SUPPORTED_LANGUAGES:
            set_language(lang)
            self.retranslate()
            self._build_menu()
            self.show_toast(tr("toast_lang_changed"))

    def retranslate(self):
        """Динамически переводит все элементы окна и дочерних представлений."""
        self.set_title(tr("app_title"))
        self.title_switcher.set_title(tr("app_title"))
        self.title_switcher.set_subtitle(tr("app_subtitle"))

        if self.page_clean:
            self.page_clean.set_title(tr("tab_clean"))
        if self.page_update:
            self.page_update.set_title(tr("tab_update"))
        if self.page_terminal:
            self.page_terminal.set_title(tr("tab_terminal"))

        self.menu_button.set_tooltip_text(tr("menu_about"))

        # Обновляем дочерние представления
        if hasattr(self.clean_view, "retranslate"):
            self.clean_view.retranslate()
        if hasattr(self.update_view, "retranslate"):
            self.update_view.retranslate()
        if hasattr(self.terminal_view, "retranslate"):
            self.terminal_view.retranslate()
        if hasattr(self.mascot, "retranslate"):
            self.mascot.retranslate()

    def _on_about_activated(self, _action, _param):
        if hasattr(Adw, "AboutDialog"):
            dialog = Adw.AboutDialog()
            dialog.set_application_name("CleanArch")
            dialog.set_application_icon("cleanarch")
            dialog.set_version("1.0.0")
            dialog.set_developer_name("MisterKisik")
            dialog.set_comments(tr("about_comments"))
            dialog.set_website("https://github.com/misterkisik/cleanarch")
            dialog.set_issue_url("https://github.com/misterkisik/cleanarch/issues")
            dialog.set_copyright("© 2026 MisterKisik")
            dialog.set_license_type(Gtk.License.GPL_3_0)
            dialog.present(self)
        else:
            about = Adw.AboutWindow(transient_for=self)
            about.set_application_name("CleanArch")
            about.set_application_icon("cleanarch")
            about.set_version("1.0.0")
            about.set_developer_name("MisterKisik")
            about.set_comments(tr("about_comments"))
            about.set_website("https://github.com/misterkisik/cleanarch")
            about.set_issue_url("https://github.com/misterkisik/cleanarch/issues")
            about.set_copyright("© 2026 MisterKisik")
            about.set_license_type(Gtk.License.GPL_3_0)
            about.present()

    def show_toast(self, message: str):
        toast = Adw.Toast.new(message)
        toast.set_timeout(2)
        self.toast_overlay.add_toast(toast)

    def _on_status_change(self, status: str, extra: str):
        self.mascot.set_mood(status, extra)

    def _on_start_clean(self, script: str, password: str = None):
        self.mascot.set_mood("cleaning")
        self.view_stack.set_visible_child_name("terminal")
        self.terminal_view.run_script(
            script,
            on_complete=self._on_clean_finished,
            password=password
        )

    def _on_clean_finished(self, returncode: int):
        if returncode == 0:
            self.mascot.set_mood("done", tr("toast_clean_done"))
            self.show_toast(tr("toast_clean_done"))
            # Пересканируем размеры
            self.clean_view.start_scan()
        else:
            self.mascot.set_mood("error")
            self.show_toast(tr("toast_clean_error"))

    def _on_start_update(self, script: str, password: str = None):
        self.mascot.set_mood("updating")
        self.view_stack.set_visible_child_name("terminal")
        self.terminal_view.run_script(
            script,
            on_complete=self._on_update_finished,
            password=password
        )

    def _on_update_finished(self, returncode: int):
        if returncode == 0:
            self.mascot.set_mood("done", tr("toast_update_done"))
            self.show_toast(tr("toast_update_done"))
        else:
            self.mascot.set_mood("error")
            self.show_toast(tr("toast_update_error"))

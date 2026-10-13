"""
Главное окно CleanArch: слева маскот с репликами, справа разделы управления и консоль.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, GObject
from cleanarch.mascot import MascotWidget
from cleanarch.views.clean_view import CleanView
from cleanarch.views.update_view import UpdateView
from cleanarch.views.terminal_view import TerminalView

class CleanArchWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("CleanArch")
        self.set_default_size(980, 720)

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
        self.view_stack.add_titled_with_icon(
            self.clean_view,
            "clean",
            "Очистка",
            "edit-clear-all-symbolic"
        )
        self.view_stack.add_titled_with_icon(
            self.update_view,
            "update",
            "Обновление",
            "software-update-available-symbolic"
        )
        self.view_stack.add_titled_with_icon(
            self.terminal_view,
            "terminal",
            "Консоль / Лог",
            "utilities-terminal-symbolic"
        )

        # Переключатель в шапке
        self.title_switcher = Adw.ViewSwitcherTitle(stack=self.view_stack)
        self.title_switcher.set_title("CleanArch")
        self.title_switcher.set_subtitle("Очистка и оптимизация Arch Linux")

        # HeaderBar
        header_bar = Adw.HeaderBar()
        header_bar.set_title_widget(self.title_switcher)

        # Меню в шапке
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu_button.set_tooltip_text("Меню")
        menu = Gio.Menu()
        menu.append("О программе", "win.about")
        menu_button.set_menu_model(menu)
        header_bar.pack_end(menu_button)

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

        # Регистрация действий окна
        self._setup_actions()

    def _setup_actions(self):
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self._on_about_activated)
        self.add_action(about_action)

    def _on_about_activated(self, _action, _param):
        if hasattr(Adw, "AboutDialog"):
            dialog = Adw.AboutDialog()
            dialog.set_application_name("CleanArch")
            dialog.set_application_icon("system-software-install-symbolic")
            dialog.set_version("1.0.0")
            dialog.set_developer_name("MisterKisik")
            dialog.set_comments(
                "Графическая утилита для очистки кэшей pacman/yay, логов и обновления системы Arch Linux."
            )
            dialog.set_license_type(Gtk.License.GPL_3_0)
            dialog.present(self)
        else:
            about = Adw.AboutWindow(transient_for=self)
            about.set_application_name("CleanArch")
            about.set_version("1.0.0")
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
            self.mascot.set_mood("done", "Кэши успешно очищены!")
            self.show_toast("Очистка успешно завершена!")
            # Пересканируем размеры
            self.clean_view.start_scan()
        else:
            self.mascot.set_mood("error")
            self.show_toast("Произошла ошибка при очистке!")

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
            self.mascot.set_mood("done", "Система успешно обновлена!")
            self.show_toast("Обновление завершено!")
        else:
            self.mascot.set_mood("error")
            self.show_toast("Обновление прервано или завершилось с ошибкой!")

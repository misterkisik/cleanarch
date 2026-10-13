"""
Представление встроенного терминального лога для отображения выполнения команд в реальном времени.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Gdk
import subprocess
import threading
from typing import Callable, Optional

class TerminalView(Gtk.Box):
    def __init__(self, on_toast: Optional[Callable[[str], None]] = None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.on_toast = on_toast
        self.current_process: Optional[subprocess.Popen] = None
        self.set_margin_start(16)
        self.set_margin_end(16)
        self.set_margin_top(16)
        self.set_margin_bottom(16)

        # Панель управления логом сверху
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        
        self.status_icon = Gtk.Image.new_from_icon_name("utilities-terminal-symbolic")
        top_bar.append(self.status_icon)

        self.status_label = Gtk.Label(label="Ожидание задач...")
        self.status_label.add_css_class("heading")
        self.status_label.set_hexpand(True)
        self.status_label.set_halign(Gtk.Align.START)
        top_bar.append(self.status_label)

        # Спиннер прогресса
        self.spinner = Gtk.Spinner()
        top_bar.append(self.spinner)

        # Кнопка остановки
        self.stop_btn = Gtk.Button.new_from_icon_name("process-stop-symbolic")
        self.stop_btn.set_tooltip_text("Прервать выполнение")
        self.stop_btn.add_css_class("destructive-action")
        self.stop_btn.set_sensitive(False)
        self.stop_btn.connect("clicked", self._on_stop_clicked)
        top_bar.append(self.stop_btn)

        # Кнопка копирования
        copy_btn = Gtk.Button.new_from_icon_name("edit-copy-symbolic")
        copy_btn.set_tooltip_text("Скопировать весь лог")
        copy_btn.add_css_class("flat")
        copy_btn.connect("clicked", self._on_copy_clicked)
        top_bar.append(copy_btn)

        # Кнопка очистки лога
        clear_btn = Gtk.Button.new_from_icon_name("edit-clear-symbolic")
        clear_btn.set_tooltip_text("Очистить вывод")
        clear_btn.add_css_class("flat")
        clear_btn.connect("clicked", lambda _: self.clear_log())
        top_bar.append(clear_btn)

        self.append(top_bar)

        # Текстовое поле консоли
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.add_css_class("card")

        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_cursor_visible(False)
        self.text_view.set_monospace(True)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text_view.set_top_margin(12)
        self.text_view.set_bottom_margin(12)
        self.text_view.set_left_margin(12)
        self.text_view.set_right_margin(12)
        self.buffer = self.text_view.get_buffer()

        scrolled.set_child(self.text_view)
        self.append(scrolled)

        self.append_log("=== Консоль CleanArch готова к выполнению задач ===\n")

    def append_log(self, text: str):
        end_iter = self.buffer.get_end_iter()
        self.buffer.insert(end_iter, text)
        # Автопрокрутка вниз
        mark = self.buffer.create_mark(None, self.buffer.get_end_iter(), False)
        self.text_view.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)

    def clear_log(self):
        self.buffer.set_text("")
        self.status_label.set_text("Лог очищен")

    def run_script(self, script: str, on_complete: Optional[Callable[[int], None]] = None):
        """Запускает выполнение bash-скрипта в отдельном потоке с потоковым выводом."""
        if self.current_process and self.current_process.poll() is None:
            if self.on_toast:
                self.on_toast("Предыдущая задача ещё выполняется!")
            return

        self.status_label.set_text("Выполняется...")
        self.status_icon.set_from_icon_name("system-run-symbolic")
        self.spinner.start()
        self.stop_btn.set_sensitive(True)
        self.append_log(f"\n--- [Старт: {GLib.DateTime.new_now_local().format('%H:%M:%S')}] ---\n")

        def worker():
            try:
                proc = subprocess.Popen(
                    ["bash", "-c", script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                self.current_process = proc

                for line in proc.stdout:
                    GLib.idle_add(self.append_log, line)

                proc.wait()
                code = proc.returncode
            except Exception as e:
                code = 1
                GLib.idle_add(self.append_log, f"\nОшибка запуска: {e}\n")

            GLib.idle_add(self._on_finished, code, on_complete)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def _on_finished(self, returncode: int, on_complete: Optional[Callable[[int], None]]):
        self.spinner.stop()
        self.stop_btn.set_sensitive(False)
        self.current_process = None

        if returncode == 0:
            self.status_label.set_text("Успешно завершено! ✓")
            self.status_icon.set_from_icon_name("emblem-ok-symbolic")
            self.append_log("\n--- [Завершено успешно] ---\n")
        else:
            self.status_label.set_text(f"Завершено с кодом {returncode} ✗")
            self.status_icon.set_from_icon_name("dialog-warning-symbolic")
            self.append_log(f"\n--- [Завершено с ошибкой (код {returncode})] ---\n")

        if on_complete:
            on_complete(returncode)

    def _on_stop_clicked(self, _btn):
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                self.append_log("\n[Прервано пользователем]\n")
            except Exception:
                pass

    def _on_copy_clicked(self, _btn):
        start = self.buffer.get_start_iter()
        end = self.buffer.get_end_iter()
        text = self.buffer.get_text(start, end, True)
        display = Gdk.Display.get_default()
        if display:
            clipboard = display.get_clipboard()
            clipboard.set(text)
        if self.on_toast:
            self.on_toast("Лог скопирован в буфер")

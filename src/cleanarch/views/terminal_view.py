"""
Представление встроенного терминального лога для отображения выполнения команд в реальном времени.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Gdk
import os
import subprocess
import threading
from typing import Callable, Optional
from cleanarch.i18n import tr

class TerminalView(Gtk.Box):
    def __init__(self, on_toast: Optional[Callable[[str], None]] = None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.on_toast = on_toast
        self.current_process: Optional[subprocess.Popen] = None
        self._last_status = "waiting"
        self._last_code = 0
        self.set_margin_start(16)
        self.set_margin_end(16)
        self.set_margin_top(16)
        self.set_margin_bottom(16)

        # Панель управления логом сверху
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        
        self.status_icon = Gtk.Image.new_from_icon_name("utilities-terminal-symbolic")
        top_bar.append(self.status_icon)

        self.status_label = Gtk.Label(label=tr("term_waiting"))
        self.status_label.add_css_class("heading")
        self.status_label.set_hexpand(True)
        self.status_label.set_halign(Gtk.Align.START)
        top_bar.append(self.status_label)

        # Спиннер прогресса
        self.spinner = Gtk.Spinner()
        top_bar.append(self.spinner)

        # Кнопка остановки
        self.stop_btn = Gtk.Button.new_from_icon_name("process-stop-symbolic")
        self.stop_btn.set_tooltip_text(tr("term_stop_tooltip"))
        self.stop_btn.add_css_class("destructive-action")
        self.stop_btn.set_sensitive(False)
        self.stop_btn.connect("clicked", self._on_stop_clicked)
        top_bar.append(self.stop_btn)

        # Кнопка копирования
        self.copy_btn = Gtk.Button.new_from_icon_name("edit-copy-symbolic")
        self.copy_btn.set_tooltip_text(tr("term_copy_tooltip"))
        self.copy_btn.add_css_class("flat")
        self.copy_btn.connect("clicked", self._on_copy_clicked)
        top_bar.append(self.copy_btn)

        # Кнопка очистки лога
        self.clear_btn = Gtk.Button.new_from_icon_name("edit-clear-symbolic")
        self.clear_btn.set_tooltip_text(tr("term_clear_tooltip"))
        self.clear_btn.add_css_class("flat")
        self.clear_btn.connect("clicked", lambda _: self.clear_log())
        top_bar.append(self.clear_btn)

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

        self.append_log(tr("term_ready"))

    def retranslate(self):
        """Обновляет подсказки и строку статуса при смене языка."""
        self.stop_btn.set_tooltip_text(tr("term_stop_tooltip"))
        self.copy_btn.set_tooltip_text(tr("term_copy_tooltip"))
        self.clear_btn.set_tooltip_text(tr("term_clear_tooltip"))

        if self._last_status == "waiting":
            self.status_label.set_text(tr("term_waiting"))
        elif self._last_status == "running":
            self.status_label.set_text(tr("term_running"))
        elif self._last_status == "success":
            self.status_label.set_text(tr("term_success"))
        elif self._last_status == "error":
            self.status_label.set_text(tr("term_error", code=self._last_code))
        elif self._last_status == "cleared":
            self.status_label.set_text(tr("status_log_cleared"))

    def append_log(self, text: str):
        end_iter = self.buffer.get_end_iter()
        self.buffer.insert(end_iter, text)
        # Автопрокрутка вниз
        mark = self.buffer.create_mark(None, self.buffer.get_end_iter(), False)
        self.text_view.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)

    def clear_log(self):
        self.buffer.set_text("")
        self._last_status = "cleared"
        self.status_label.set_text(tr("status_log_cleared"))

    def run_script(
        self,
        script: str,
        on_complete: Optional[Callable[[int], None]] = None,
        password: Optional[str] = None
    ):
        """Запускает выполнение bash-скрипта в отдельном потоке с потоковым выводом."""
        if self.current_process and self.current_process.poll() is None:
            if self.on_toast:
                self.on_toast(tr("toast_task_running"))
            return

        self._last_status = "running"
        self.status_label.set_text(tr("term_running"))
        self.status_icon.set_from_icon_name("system-run-symbolic")
        self.spinner.start()
        self.stop_btn.set_sensitive(True)
        self.append_log(f"\n--- [{tr('tab_terminal')}: {GLib.DateTime.new_now_local().format('%H:%M:%S')}] ---\n")

        def worker():
            try:
                env = os.environ.copy()
                if password:
                    env["CLEANARCH_PASS"] = password

                proc = subprocess.Popen(
                    ["bash", "-c", script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    env=env
                )
                self.current_process = proc

                for line in proc.stdout:
                    GLib.idle_add(self.append_log, line)

                proc.wait()
                code = proc.returncode
            except Exception as e:
                code = 1
                GLib.idle_add(self.append_log, f"\nError: {e}\n")

            GLib.idle_add(self._on_finished, code, on_complete)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def _on_finished(self, returncode: int, on_complete: Optional[Callable[[int], None]]):
        self.spinner.stop()
        self.stop_btn.set_sensitive(False)
        self.current_process = None
        self._last_code = returncode

        if returncode == 0:
            self._last_status = "success"
            self.status_label.set_text(tr("term_success"))
            self.status_icon.set_from_icon_name("emblem-ok-symbolic")
            self.append_log(f"\n--- [{tr('term_success')}] ---\n")
        else:
            self._last_status = "error"
            self.status_label.set_text(tr("term_error", code=returncode))
            self.status_icon.set_from_icon_name("dialog-warning-symbolic")
            self.append_log(f"\n--- [{tr('term_error', code=returncode)}] ---\n")

        if on_complete:
            on_complete(returncode)

    def _on_stop_clicked(self, _btn):
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                self.append_log(tr("log_aborted_by_user"))
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
            self.on_toast(tr("toast_log_copied"))

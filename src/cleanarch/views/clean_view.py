"""
Представление выбора элементов очистки системы и кэшей.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib
import os
import threading
from typing import Callable, Dict, List, Optional
from cleanarch.cleaner import scan_all_items, format_size, build_clean_script, CleanItem
from cleanarch.views.password_dialog import PasswordDialog
from cleanarch.i18n import tr

class CleanView(Adw.PreferencesPage):
    def __init__(
        self,
        on_start_clean: Callable[[str], None],
        on_status_change: Callable[[str, str], None],
        on_toast: Callable[[str], None]
    ):
        super().__init__()
        self.on_start_clean = on_start_clean
        self.on_status_change = on_status_change
        self.on_toast = on_toast
        
        self.items: Dict[str, CleanItem] = {}
        self.rows: Dict[str, Adw.ActionRow] = {}
        self.check_buttons: Dict[str, Gtk.CheckButton] = {}
        self.size_labels: Dict[str, Gtk.Label] = {}
        self.is_scanning = False

        # Группа сводки и кнопок действий
        self.summary_group = Adw.PreferencesGroup()
        self.summary_group.set_title(tr("clean_title"))
        self.summary_group.set_description(tr("clean_desc"))

        # Строка общего размера
        self.total_row = Adw.ActionRow()
        self.total_row.set_title(tr("total_to_free"))
        self.total_row.set_subtitle(tr("status_calculating"))
        self.total_row.set_icon_name("drive-harddisk-symbolic")

        # Кнопки действий справа от общей суммы
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        btn_box.set_valign(Gtk.Align.CENTER)

        self.rescan_btn = Gtk.Button.new_from_icon_name("view-refresh-symbolic")
        self.rescan_btn.set_tooltip_text(tr("btn_rescan_tooltip"))
        self.rescan_btn.add_css_class("flat")
        self.rescan_btn.connect("clicked", lambda _: self.start_scan())
        btn_box.append(self.rescan_btn)

        self.clean_btn = Gtk.Button(label=tr("btn_clean"))
        self.clean_btn.add_css_class("suggested-action")
        self.clean_btn.connect("clicked", self._on_clean_clicked)
        btn_box.append(self.clean_btn)

        self.total_row.add_suffix(btn_box)
        self.summary_group.add(self.total_row)
        self.add(self.summary_group)

        # Группа элементов очистки
        self.items_group = Adw.PreferencesGroup()
        self.items_group.set_title(tr("categories_group_title"))
        self.add(self.items_group)

        # Первичное сканирование
        self.start_scan()

    def retranslate(self):
        """Обновляет все заголовки и строки списка при смене языка."""
        self.summary_group.set_title(tr("clean_title"))
        self.summary_group.set_description(tr("clean_desc"))
        self.total_row.set_title(tr("total_to_free"))
        self.rescan_btn.set_tooltip_text(tr("btn_rescan_tooltip"))
        self.clean_btn.set_label(tr("btn_clean"))
        self.items_group.set_title(tr("categories_group_title"))

        for item_id, row in self.rows.items():
            if item_id == "pacman_cache":
                row.set_title(tr("cat_pacman_title"))
                row.set_subtitle(tr("cat_pacman_desc"))
            elif item_id == "yay_cache":
                row.set_title(tr("cat_yay_title"))
                row.set_subtitle(tr("cat_yay_desc"))
            elif item_id == "journal":
                row.set_title(tr("cat_journal_title"))
                row.set_subtitle(tr("cat_journal_desc"))
            elif item_id == "orphans":
                count = self.items[item_id].count if item_id in self.items else 0
                row.set_title(tr("cat_orphans_title"))
                row.set_subtitle(tr("cat_orphans_desc", count=count))
            elif item_id == "thumbnails":
                row.set_title(tr("cat_thumbnails_title"))
                row.set_subtitle(tr("cat_thumbnails_desc"))
            elif item_id == "flatpak_unused":
                count = self.items[item_id].count if item_id in self.items else 0
                row.set_title(tr("cat_flatpak_title"))
                row.set_subtitle(tr("cat_flatpak_desc", count=count))

        self._update_total_summary()

    def start_scan(self):
        """Запускает фоновое сканирование объемов кэша."""
        if self.is_scanning:
            return
        self.is_scanning = True
        self.rescan_btn.set_sensitive(False)
        self.clean_btn.set_sensitive(False)
        self.total_row.set_subtitle(tr("status_scanning"))
        if self.on_status_change:
            self.on_status_change("scanning", "")

        def worker():
            scanned = scan_all_items()
            GLib.idle_add(self._on_scan_completed, scanned)

        threading.Thread(target=worker, daemon=True).start()

    def _on_scan_completed(self, scanned: Dict[str, CleanItem]):
        self.is_scanning = False
        self.rescan_btn.set_sensitive(True)
        self.clean_btn.set_sensitive(True)
        self.items = scanned

        # Перестраиваем строки списка, если они ещё не были созданы
        if not self.check_buttons:
            for item_id, item in scanned.items():
                row = Adw.ActionRow()
                row.set_title(item.title)
                row.set_subtitle(item.description)
                row.set_icon_name(item.icon_name)

                check = Gtk.CheckButton()
                check.set_active(item.enabled)
                check.connect("toggled", lambda _: self._update_total_summary())
                row.add_prefix(check)
                row.set_activatable_widget(check)
                self.check_buttons[item_id] = check
                self.rows[item_id] = row

                size_lbl = Gtk.Label(label=item.size_formatted)
                size_lbl.add_css_class("monospace")
                size_lbl.add_css_class("card")
                size_lbl.set_margin_start(8)
                size_lbl.set_margin_end(8)
                size_lbl.set_margin_top(4)
                size_lbl.set_margin_bottom(4)
                row.add_suffix(size_lbl)
                self.size_labels[item_id] = size_lbl

                self.items_group.add(row)
        else:
            # Обновляем существующие метки
            for item_id, item in scanned.items():
                if item_id in self.size_labels:
                    self.size_labels[item_id].set_text(item.size_formatted)
                if item_id in self.check_buttons:
                    # Если найдено 0 файлов, можно снять галочку
                    if item.size_bytes == 0 and item.count == 0:
                        self.check_buttons[item_id].set_active(False)

        self._update_total_summary()

    def _update_total_summary(self):
        total_bytes = 0
        selected_count = 0
        for item_id, check in self.check_buttons.items():
            if check.get_active() and item_id in self.items:
                total_bytes += self.items[item_id].size_bytes
                selected_count += 1

        formatted = format_size(total_bytes)
        self.total_row.set_subtitle(
            tr("status_selected_summary", count=selected_count, size=formatted)
        )
        self.clean_btn.set_sensitive(selected_count > 0)

        if self.on_status_change:
            self.on_status_change("scanned", formatted)

    def _on_clean_clicked(self, _btn):
        selected_ids = [
            item_id for item_id, check in self.check_buttons.items() if check.get_active()
        ]
        if not selected_ids:
            if self.on_toast:
                self.on_toast(tr("toast_no_selection"))
            return

        needs_root = any(self.items.get(i) and self.items[i].requires_root for i in selected_ids)
        if needs_root and os.geteuid() != 0:
            def on_pw_success(password: str):
                script = build_clean_script(selected_ids, has_sudo_pass=True)
                if self.on_start_clean:
                    self.on_start_clean(script, password)

            dlg = PasswordDialog(self.get_root(), on_success=on_pw_success)
            dlg.present_dialog()
        else:
            script = build_clean_script(selected_ids, has_sudo_pass=False)
            if self.on_start_clean:
                self.on_start_clean(script, None)

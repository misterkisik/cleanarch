"""
Модуль сканирования и очистки кэшей и мусора в Arch Linux.
"""

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class CleanItem:
    id: str
    title: str
    description: str
    size_bytes: int
    size_formatted: str
    count: int
    requires_root: bool
    enabled: bool
    icon_name: str

def format_size(size_bytes: int) -> str:
    """Форматирует байты в человекочитаемый вид."""
    if size_bytes <= 0:
        return "0 Б"
    units = ["Б", "КБ", "МБ", "ГБ", "ТБ"]
    idx = 0
    val = float(size_bytes)
    while val >= 1024.0 and idx < len(units) - 1:
        val /= 1024.0
        idx += 1
    return f"{val:.1f} {units[idx]}"

def get_dir_size(path: str) -> int:
    """Вычисляет размер каталога в байтах, игнорируя ошибки доступа."""
    total = 0
    if not os.path.exists(path):
        return 0
    try:
        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    total += os.path.getsize(fp)
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    return total

def get_journalctl_size() -> int:
    """Получает размер журнала systemd через journalctl --disk-usage."""
    try:
        proc = subprocess.run(
            ["journalctl", "--disk-usage"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        if proc.returncode == 0:
            match = re.search(r"([0-9.]+)\s*([KMGTPkmgtp]?[bB])", proc.stdout)
            if match:
                val = float(match.group(1))
                unit = match.group(2).upper()
                multipliers = {"B": 1, "K": 1024, "KB": 1024, "M": 1024**2, "MB": 1024**2, "G": 1024**3, "GB": 1024**3}
                for u, mult in multipliers.items():
                    if unit.startswith(u):
                        return int(val * mult)
    except Exception:
        pass
    return 0

def get_orphan_packages() -> List[str]:
    """Возвращает список неиспользуемых пакетов-зависимостей (orphans)."""
    try:
        proc = subprocess.run(
            ["pacman", "-Qtdq"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        if proc.returncode == 0:
            return [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    except Exception:
        pass
    return []

def get_flatpak_unused_count() -> int:
    """Проверяет количество неиспользуемых рантаймов Flatpak."""
    if not shutil.which("flatpak"):
        return 0
    try:
        proc = subprocess.run(
            ["flatpak", "list", "--unused"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        if proc.returncode == 0:
            return len([l for l in proc.stdout.splitlines() if l.strip()])
    except Exception:
        pass
    return 0

def scan_all_items() -> Dict[str, CleanItem]:
    """Сканирует все доступные категории очистки и возвращает их размеры."""
    items: Dict[str, CleanItem] = {}

    # 1. Кэш pacman
    pacman_cache_dir = "/var/cache/pacman/pkg"
    pacman_size = get_dir_size(pacman_cache_dir)
    items["pacman_cache"] = CleanItem(
        id="pacman_cache",
        title="Кэш пакетов pacman (полная очистка)",
        description="Удаляет все архивы пакетов (.pkg.tar.zst) из /var/cache/pacman/pkg (-Scc) и временные файлы",
        size_bytes=pacman_size,
        size_formatted=format_size(pacman_size),
        count=0,
        requires_root=True,
        enabled=True,
        icon_name="system-software-install-symbolic"
    )

    # 2. Кэш yay / AUR
    yay_cache_dir = os.path.expanduser("~/.cache/yay")
    yay_size = get_dir_size(yay_cache_dir)
    items["yay_cache"] = CleanItem(
        id="yay_cache",
        title="Кэш сборщика AUR (yay)",
        description="Кэшированные репозитории и собранные исходники в ~/.cache/yay",
        size_bytes=yay_size,
        size_formatted=format_size(yay_size),
        count=0,
        requires_root=False,
        enabled=True,
        icon_name="folder-download-symbolic"
    )

    # 3. Системный журнал systemd
    journal_size = get_journalctl_size()
    items["journal"] = CleanItem(
        id="journal",
        title="Системный журнал (journalctl)",
        description="Старые системные логи служб (будут сохранены логи за последние 3 дня)",
        size_bytes=journal_size,
        size_formatted=format_size(journal_size),
        count=0,
        requires_root=True,
        enabled=True,
        icon_name="utilities-system-monitor-symbolic"
    )

    # 4. Пакеты-сироты (orphans)
    orphans = get_orphan_packages()
    items["orphans"] = CleanItem(
        id="orphans",
        title="Пакеты-сироты (Orphans)",
        description=f"Неиспользуемые пакеты-зависимости, оставшиеся после удаления программ ({len(orphans)} шт.)",
        size_bytes=0,
        size_formatted=f"{len(orphans)} пакетов" if orphans else "0 пакетов",
        count=len(orphans),
        requires_root=True,
        enabled=bool(orphans),
        icon_name="edit-delete-symbolic"
    )

    # 5. Кэш миниатюр рабочего стола
    thumb_dir = os.path.expanduser("~/.cache/thumbnails")
    thumb_size = get_dir_size(thumb_dir)
    items["thumbnails"] = CleanItem(
        id="thumbnails",
        title="Кэш миниатюр изображений",
        description="Временные превью картинок и видео в ~/.cache/thumbnails",
        size_bytes=thumb_size,
        size_formatted=format_size(thumb_size),
        count=0,
        requires_root=False,
        enabled=True,
        icon_name="image-x-generic-symbolic"
    )

    # 6. Flatpak unused (если установлен)
    if shutil.which("flatpak"):
        fp_unused = get_flatpak_unused_count()
        items["flatpak_unused"] = CleanItem(
            id="flatpak_unused",
            title="Неиспользуемые рантаймы Flatpak",
            description=f"Библиотеки Flatpak, которые больше не нужны ни одному приложению ({fp_unused} шт.)",
            size_bytes=0,
            size_formatted=f"{fp_unused} шт." if fp_unused else "0 шт.",
            count=fp_unused,
            requires_root=False,
            enabled=bool(fp_unused),
            icon_name="application-x-executable-symbolic"
        )

    return items

def build_clean_script(selected_ids: List[str], has_sudo_pass: bool = False) -> str:
    """Генерирует bash-скрипт для последовательного выполнения выбранных задач очистки."""
    commands = []
    commands.append('echo "=== [CleanArch] Начинаем очистку системы ==="')

    # Проверяем наличие root-задач
    has_root_tasks = any(i in selected_ids for i in ("pacman_cache", "journal", "orphans"))
    if has_root_tasks and has_sudo_pass:
        # Валидируем sudo сессию один раз
        commands.append('printf "%s\\n" "$CLEANARCH_PASS" | sudo -S -v 2>/dev/null || true')
        commands.append('unset CLEANARCH_PASS')

    # Thumbnails (пользователь)
    if "thumbnails" in selected_ids:
        commands.append('echo ""')
        commands.append('echo "-> Очистка кэша миниатюр..."')
        commands.append('rm -rf ~/.cache/thumbnails/* && echo "✓ Кэш миниатюр очищен"')

    # yay cache (пользователь)
    if "yay_cache" in selected_ids:
        commands.append('echo ""')
        commands.append('echo "-> Очистка кэша yay..."')
        commands.append('if command -v yay &>/dev/null; then')
        commands.append('    printf "y\\ny\\n" | yay -Sc --noconfirm 2>/dev/null || true')
        commands.append('fi')
        commands.append('rm -rf ~/.cache/yay/* 2>/dev/null || true')
        commands.append('echo "✓ Кэш yay очищен"')

    # Flatpak unused (пользователь)
    if "flatpak_unused" in selected_ids and shutil.which("flatpak"):
        commands.append('echo ""')
        commands.append('echo "-> Удаление неиспользуемых рантаймов Flatpak..."')
        commands.append('flatpak uninstall --unused -y || true')
        commands.append('echo "✓ Flatpak очищен"')

    # Root tasks
    if has_root_tasks:
        commands.append('echo ""')
        commands.append('echo "-> Выполнение системных операций (права root)..."')

        if "pacman_cache" in selected_ids:
            commands.append('echo "-> Полная очистка кэша pacman (удаление всех архивов пакетов)..."')
            commands.append('sudo rm -rf /var/cache/pacman/pkg/download-* 2>/dev/null || true')
            commands.append('printf "y\\ny\\n" | sudo pacman -Scc --noconfirm 2>/dev/null || true')
            commands.append('echo "✓ Кэш pacman полностью очищен"')

        if "journal" in selected_ids:
            commands.append('echo "-> Сокращение системного журнала (до 3 дней)..."')
            commands.append('sudo journalctl --vacuum-time=3d || true')
            commands.append('echo "✓ Журнал очищен"')

        if "orphans" in selected_ids:
            commands.append('echo "-> Удаление пакетов-сирот..."')
            commands.append('orphans=$(pacman -Qtdq 2>/dev/null)')
            commands.append('if [ -n "$orphans" ]; then')
            commands.append('    echo "$orphans" | sudo pacman -Rns - --noconfirm || true')
            commands.append('    echo "✓ Пакеты-сироты удалены"')
            commands.append('else')
            commands.append('    echo "✓ Пакеты-сироты не найдены"')
            commands.append('fi')

    commands.append('echo ""')
    commands.append('echo "=== [CleanArch] Очистка успешно завершена! ✨ ==="')
    return "\n".join(commands)

def build_update_script(task: str, has_sudo_pass: bool = False) -> str:
    """Генерирует скрипт для обновления с поддержкой автоподстановки пароля."""
    commands = []
    if has_sudo_pass:
        commands.append('printf "%s\\n" "$CLEANARCH_PASS" | sudo -S -v 2>/dev/null || true')
        commands.append('unset CLEANARCH_PASS')

    if task == "full_update":
        commands.append('echo "=== [CleanArch] Обновление системы и AUR ==="')
        if shutil.which("yay"):
            commands.append('yay -Syu --noconfirm')
        else:
            commands.append('sudo pacman -Syu --noconfirm')
    elif task == "keyring":
        commands.append('echo "=== [CleanArch] Обновление ключей archlinux-keyring ==="')
        commands.append('sudo pacman -Sy archlinux-keyring --noconfirm')
    elif task == "flatpak":
        commands.append('echo "=== [CleanArch] Обновление пакетов Flatpak ==="')
        commands.append('flatpak update -y')

    commands.append('echo "=== [CleanArch] Процесс завершен! ==="')
    return "\n".join(commands)

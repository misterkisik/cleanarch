"""
Модуль интернационализации (i18n) для CleanArch.
Поддерживаемые языки: ru (Русский), en (English), es (Español), ja (日本語), fr (Français), zh (简体中文).
"""

import os
import json
import locale
from typing import Dict, Any

CONFIG_DIR = os.path.expanduser("~/.config/cleanarch")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

SUPPORTED_LANGUAGES: Dict[str, str] = {
    "ru": "Русский",
    "en": "English",
    "es": "Español",
    "ja": "日本語",
    "fr": "Français",
    "zh": "简体中文"
}

_current_lang = "ru"

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Общие
    "app_title": {
        "ru": "CleanArch",
        "en": "CleanArch",
        "es": "CleanArch",
        "ja": "CleanArch",
        "fr": "CleanArch",
        "zh": "CleanArch"
    },
    "app_subtitle": {
        "ru": "Очистка и оптимизация Arch Linux",
        "en": "Arch Linux cleaning and optimization",
        "es": "Limpieza y optimización de Arch Linux",
        "ja": "Arch Linuxのクリーンアップと最適化",
        "fr": "Nettoyage et optimisation d'Arch Linux",
        "zh": "Arch Linux 清理与优化"
    },
    "tab_clean": {
        "ru": "Очистка",
        "en": "Clean",
        "es": "Limpieza",
        "ja": "クリーン",
        "fr": "Nettoyage",
        "zh": "清理"
    },
    "tab_update": {
        "ru": "Обновление",
        "en": "Update",
        "es": "Actualización",
        "ja": "アップデート",
        "fr": "Mise à jour",
        "zh": "更新"
    },
    "tab_terminal": {
        "ru": "Консоль / Лог",
        "en": "Console / Log",
        "es": "Consola / Registro",
        "ja": "コンソール / ログ",
        "fr": "Console / Journal",
        "zh": "控制台 / 日志"
    },
    "menu_about": {
        "ru": "О программе",
        "en": "About",
        "es": "Acerca de",
        "ja": "このアプリについて",
        "fr": "À propos",
        "zh": "关于"
    },
    "menu_language": {
        "ru": "Язык (Language)",
        "en": "Language",
        "es": "Idioma",
        "ja": "言語 (Language)",
        "fr": "Langue",
        "zh": "语言 (Language)"
    },

    # Маскот
    "mascot_name": {
        "ru": "CleanArch Помощник",
        "en": "CleanArch Assistant",
        "es": "Asistente CleanArch",
        "ja": "CleanArch アシスタント",
        "fr": "Assistant CleanArch",
        "zh": "CleanArch 助手"
    },
    "mascot_idle": {
        "ru": "Привет! Пора навести чистоту в Arch Linux! Выберите кэши для очистки и нажмите кнопку запуска.",
        "en": "Hello! Time to clean up Arch Linux! Select caches to clean and press start.",
        "es": "¡Hola! ¡Es hora de limpiar Arch Linux! Seleccione las cachés para limpiar y presione inicio.",
        "ja": "こんにちは！Arch Linuxを綺麗にする時間です！消去するキャッシュを選んで開始を押してください。",
        "fr": "Bonjour ! Il est temps de nettoyer Arch Linux ! Sélectionnez les caches à vider et lancez le nettoyage.",
        "zh": "你好！是时候清理 Arch Linux 了！请选择要清理的缓存并点击开始。"
    },
    "mascot_idle_sub": {
        "ru": "Готова к работе",
        "en": "Ready to work",
        "es": "Listo para trabajar",
        "ja": "準備完了",
        "fr": "Prêt à travailler",
        "zh": "准备就绪"
    },
    "mascot_scanning": {
        "ru": "Сканирую диски... Проверяю размеры кэшей pacman, yay и системных журналов.",
        "en": "Scanning drives... Checking sizes of pacman, yay, and system logs.",
        "es": "Escaneando discos... Verificando tamaños de pacman, yay y registros.",
        "ja": "ドライブをスキャン中... pacman、yay、システムログのサイズを確認しています。",
        "fr": "Analyse des disques... Vérification de la taille de pacman, yay et des journaux système.",
        "zh": "正在扫描驱动器... 检查 pacman、yay 和系统日志的大小。"
    },
    "mascot_scanning_sub": {
        "ru": "Идет подсчет объемов мусора...",
        "en": "Calculating junk size...",
        "es": "Calculando tamaño de residuos...",
        "ja": "不要ファイルのサイズを計算中...",
        "fr": "Calcul de la taille des données inutiles...",
        "zh": "正在计算垃圾文件大小..."
    },
    "mascot_scanned": {
        "ru": "Сканирование завершено! Обнаружено мусора: {extra}. Готова освободить место!",
        "en": "Scanning complete! Found junk: {extra}. Ready to free space!",
        "es": "¡Escaneo completo! Residuos encontrados: {extra}. ¡Listo para liberar espacio!",
        "ja": "スキャン完了！不要ファイル: {extra} を発見しました。解放準備完了！",
        "fr": "Analyse terminée ! Données trouvées : {extra}. Prêt à libérer de l'espace !",
        "zh": "扫描完成！发现垃圾文件：{extra}。随时可以释放空间！"
    },
    "mascot_cleaning": {
        "ru": "Очищаю кэши и ненужные пакеты... Система будет работать быстрее и чище!",
        "en": "Cleaning caches and unneeded packages... The system will run faster and cleaner!",
        "es": "Limpiando cachés y paquetes innecesarios... ¡El sistema funcionará más rápido y limpio!",
        "ja": "キャッシュと不要なパッケージを消去中... システムがより快適になります！",
        "fr": "Nettoyage des caches et paquets inutiles... Le système sera plus rapide et propre !",
        "zh": "正在清理缓存和不需要的软件包... 系统运行将更轻快顺畅！"
    },
    "mascot_cleaning_sub": {
        "ru": "Выполняется очистка...",
        "en": "Cleaning in progress...",
        "es": "Limpieza en progreso...",
        "ja": "クリーンアップを実行中...",
        "fr": "Nettoyage en cours...",
        "zh": "正在清理..."
    },
    "mascot_done": {
        "ru": "Отличная работа! Очистка успешно завершена, диск свободен ✨",
        "en": "Great job! Cleaning completed successfully, disk space freed ✨",
        "es": "¡Buen trabajo! Limpieza completada con éxito, espacio en disco liberado ✨",
        "ja": "お疲れ様でした！クリーンアップが正常に完了し、空き容量が増えました ✨",
        "fr": "Super travail ! Nettoyage terminé avec succès, espace disque libéré ✨",
        "zh": "太棒了！清理成功完成，磁盘空间已释放 ✨"
    },
    "mascot_updating": {
        "ru": "Обновляю систему... Загружаю свежие версии пакетов Arch Linux!",
        "en": "Updating system... Downloading latest Arch Linux packages!",
        "es": "Actualizando sistema... ¡Descargando las últimas versiones de paquetes!",
        "ja": "システムを更新中... Arch Linuxの最新パッケージをダウンロードしています！",
        "fr": "Mise à jour du système... Téléchargement des derniers paquets Arch Linux !",
        "zh": "正在更新系统... 正在下载最新的 Arch Linux 软件包！"
    },
    "mascot_updating_sub": {
        "ru": "Идет процесс обновления...",
        "en": "Update in progress...",
        "es": "Actualización en progreso...",
        "ja": "更新処理中...",
        "fr": "Mise à jour en cours...",
        "zh": "正在更新中..."
    },
    "mascot_error": {
        "ru": "Ой! В процессе возникла ошибка. Перейдите во вкладку «Консоль / Лог», чтобы посмотреть подробности.",
        "en": "Oops! An error occurred. Check the 'Console / Log' tab for details.",
        "es": "¡Ups! Ocurrió un error. Revise la pestaña 'Consola / Registro' para ver detalles.",
        "ja": "おっと！エラーが発生しました。「コンソール / ログ」タブで詳細を確認してください。",
        "fr": "Oups ! Une erreur est survenue. Consultez l'onglet « Console / Journal » pour plus de détails.",
        "zh": "哎呀！过程中出现错误。请切换到“控制台 / 日志”标签页查看详情。"
    },

    # Страница Очистки
    "clean_title": {
        "ru": "Очистка дискового пространства",
        "en": "Disk Space Cleanup",
        "es": "Limpieza de espacio en disco",
        "ja": "ディスク容量の解放",
        "fr": "Nettoyage de l'espace disque",
        "zh": "磁盘空间清理"
    },
    "clean_desc": {
        "ru": "Выберите категории мусора и кэшей, которые хотите удалить. Системные операции автоматически запросят подтверждение.",
        "en": "Select cache and junk categories you want to remove. System tasks will request authorization automatically.",
        "es": "Seleccione las categorías de caché y residuos que desea eliminar. Las tareas del sistema solicitarán confirmación.",
        "ja": "削除するキャッシュや不要ファイルのカテゴリを選択してください。管理者権限が必要な処理は自動で確認されます。",
        "fr": "Sélectionnez les catégories de caches et déchets à supprimer. Les opérations système demanderont une autorisation.",
        "zh": "选择您想要删除的缓存和垃圾类别。涉及系统的操作将自动请求权限确认。"
    },
    "total_to_free": {
        "ru": "Всего можно освободить",
        "en": "Total space to free",
        "es": "Total a liberar",
        "ja": "解放可能な合計容量",
        "fr": "Total à libérer",
        "zh": "可释放的总空间"
    },
    "btn_clean": {
        "ru": "Очистить выбранное",
        "en": "Clean Selected",
        "es": "Limpiar seleccionados",
        "ja": "選択項目を削除",
        "fr": "Nettoyer la sélection",
        "zh": "清理所选项"
    },
    "btn_rescan_tooltip": {
        "ru": "Пересчитать размеры кэшей",
        "en": "Recalculate cache sizes",
        "es": "Recalcular tamaños de caché",
        "ja": "キャッシュサイズを再計算",
        "fr": "Recalculer les tailles de cache",
        "zh": "重新计算缓存大小"
    },
    "categories_group_title": {
        "ru": "Категории для очистки",
        "en": "Cleanup Categories",
        "es": "Categorías de limpieza",
        "ja": "クリーンアップカテゴリ",
        "fr": "Catégories de nettoyage",
        "zh": "清理类别"
    },

    # Категории
    "cat_pacman_title": {
        "ru": "Кэш пакетов pacman (полная очистка)",
        "en": "Pacman package cache (full clean)",
        "es": "Caché de paquetes pacman (completo)",
        "ja": "pacmanパッケージキャッシュ (完全消去)",
        "fr": "Cache des paquets pacman (complet)",
        "zh": "pacman 软件包缓存 (完全清理)"
    },
    "cat_pacman_desc": {
        "ru": "Удаляет все архивы пакетов (.pkg.tar.zst) из /var/cache/pacman/pkg (-Scc) и временные файлы",
        "en": "Removes all package archives (.pkg.tar.zst) from /var/cache/pacman/pkg (-Scc) and temp files",
        "es": "Elimina todos los archivos de paquetes (.pkg.tar.zst) de /var/cache/pacman/pkg (-Scc) y temporales",
        "ja": "/var/cache/pacman/pkg内のすべてのパッケージアーカイブ(.pkg.tar.zst)と一時ファイルを削除します (-Scc)",
        "fr": "Supprime toutes les archives de paquets (.pkg.tar.zst) de /var/cache/pacman/pkg (-Scc) et fichiers temporaires",
        "zh": "从 /var/cache/pacman/pkg 删除所有软件包归档 (.pkg.tar.zst) (-Scc) 及临时文件"
    },
    "cat_yay_title": {
        "ru": "Кэш сборщика AUR (yay)",
        "en": "AUR build cache (yay)",
        "es": "Caché de compilación AUR (yay)",
        "ja": "AURビルドキャッシュ (yay)",
        "fr": "Cache de construction AUR (yay)",
        "zh": "AUR 构建缓存 (yay)"
    },
    "cat_yay_desc": {
        "ru": "Кэшированные репозитории и собранные исходники в ~/.cache/yay",
        "en": "Cached repositories and build sources in ~/.cache/yay",
        "es": "Repositorios en caché y fuentes compiladas en ~/.cache/yay",
        "ja": "~/.cache/yay内のキャッシュされたリポジトリとビルドソース",
        "fr": "Dépôts en cache et sources compilées dans ~/.cache/yay",
        "zh": "~/.cache/yay 中缓存的代码仓库和编译源码"
    },
    "cat_journal_title": {
        "ru": "Системный журнал (journalctl)",
        "en": "System journal (journalctl)",
        "es": "Registro del sistema (journalctl)",
        "ja": "システムジャーナル (journalctl)",
        "fr": "Journal système (journalctl)",
        "zh": "系统日志 (journalctl)"
    },
    "cat_journal_desc": {
        "ru": "Старые системные логи служб (будут сохранены логи за последние 3 дня)",
        "en": "Old service logs (logs from the last 3 days will be preserved)",
        "es": "Registros antiguos de servicios (se conservan los últimos 3 días)",
        "ja": "古いサービスログ (直近3日間のログは保持されます)",
        "fr": "Anciens journaux des services (les 3 derniers jours sont conservés)",
        "zh": "旧的服务日志（将保留最近 3 天的日志）"
    },
    "cat_orphans_title": {
        "ru": "Пакеты-сироты (Orphans)",
        "en": "Orphan packages",
        "es": "Paquetes huérfanos",
        "ja": "孤立パッケージ (Orphans)",
        "fr": "Paquets orphelins",
        "zh": "孤立软件包 (Orphans)"
    },
    "cat_orphans_desc": {
        "ru": "Неиспользуемые пакеты-зависимости, оставшиеся после удаления программ ({count} шт.)",
        "en": "Unused dependencies left after uninstalling programs ({count} pkgs)",
        "es": "Dependencias no utilizadas tras desinstalar programas ({count} paqs)",
        "ja": "プログラム削除後に残った不要な依存パッケージ ({count} 個)",
        "fr": "Dépendances inutilisées après désinstallation ({count} paquets)",
        "zh": "卸载程序后残留的无用依赖包 ({count} 个)"
    },
    "cat_thumbnails_title": {
        "ru": "Кэш миниатюр изображений",
        "en": "Image thumbnails cache",
        "es": "Caché de miniaturas de imágenes",
        "ja": "サムネイルキャッシュ",
        "fr": "Cache des miniatures d'images",
        "zh": "缩略图缓存"
    },
    "cat_thumbnails_desc": {
        "ru": "Временные превью картинок и видео в ~/.cache/thumbnails",
        "en": "Temporary previews of images and videos in ~/.cache/thumbnails",
        "es": "Vistas previas temporales en ~/.cache/thumbnails",
        "ja": "~/.cache/thumbnails内の一時的な画像・動画プレビュー",
        "fr": "Aperçus temporaires d'images et vidéos dans ~/.cache/thumbnails",
        "zh": "~/.cache/thumbnails 中的图片和视频临时预览"
    },
    "cat_flatpak_title": {
        "ru": "Неиспользуемые рантаймы Flatpak",
        "en": "Unused Flatpak runtimes",
        "es": "Runtimes de Flatpak no utilizados",
        "ja": "未使用のFlatpakランタイム",
        "fr": "Runtimes Flatpak inutilisés",
        "zh": "未使用的 Flatpak 运行库"
    },
    "cat_flatpak_desc": {
        "ru": "Библиотеки Flatpak, которые больше не нужны ни одному приложению ({count} шт.)",
        "en": "Flatpak runtimes no longer required by any application ({count} items)",
        "es": "Bibliotecas Flatpak que ya no necesita ninguna aplicación ({count} elem.)",
        "ja": "どのアプリにも使用されていないFlatpakライブラリ ({count} 個)",
        "fr": "Bibliothèques Flatpak qui ne sont plus nécessaires ({count} éléments)",
        "zh": "任何应用程序都不再需要的 Flatpak 库 ({count} 个)"
    },

    # Страница Обновления
    "update_title": {
        "ru": "Обновление системы и репозиториев",
        "en": "System and Repository Update",
        "es": "Actualización del sistema y repositorios",
        "ja": "システムとリポジトリの更新",
        "fr": "Mise à jour du système et des dépôts",
        "zh": "系统与软件源更新"
    },
    "update_desc": {
        "ru": "Регулярное обновление обеспечивает безопасность и актуальность вашего ПО в Arch Linux.",
        "en": "Regular updates ensure your software remains secure and up-to-date in Arch Linux.",
        "es": "Las actualizaciones periódicas garantizan la seguridad y estabilidad en Arch Linux.",
        "ja": "定期的なアップデートにより、Arch Linuxのセキュリティと最新性を維持できます。",
        "fr": "Des mises à jour régulières assurent la sécurité et la stabilité de votre système Arch Linux.",
        "zh": "定期更新可确保 Arch Linux 系统中的软件保持安全和最新状态。"
    },
    "up_full_title": {
        "ru": "Полное обновление (pacman + AUR)",
        "en": "Full System Update (pacman + AUR)",
        "es": "Actualización completa (pacman + AUR)",
        "ja": "システム全体の完全更新 (pacman + AUR)",
        "fr": "Mise à jour complète (pacman + AUR)",
        "zh": "系统完全更新 (pacman + AUR)"
    },
    "up_full_desc": {
        "ru": "Синхронизирует репозитории и обновляет все пакеты системы и пользовательские программы AUR",
        "en": "Synchronizes mirrors and updates all system packages and AUR programs",
        "es": "Sincroniza repositorios y actualiza todos los paquetes del sistema y programas AUR",
        "ja": "ミラーを同期し、すべてのシステムパッケージおよびAURプログラムを更新します",
        "fr": "Synchronise les dépôts et met à jour tous les paquets du système et AUR",
        "zh": "同步镜像源并更新所有系统软件包及 AUR 程序"
    },
    "up_full_btn": {
        "ru": "Обновить систему",
        "en": "Update System",
        "es": "Actualizar sistema",
        "ja": "システムを更新",
        "fr": "Mettre à jour le système",
        "zh": "更新系统"
    },
    "up_keyring_title": {
        "ru": "Обновить ключи безопасности (archlinux-keyring)",
        "en": "Update Security Keys (archlinux-keyring)",
        "es": "Actualizar claves de seguridad (archlinux-keyring)",
        "ja": "セキュリティキーの更新 (archlinux-keyring)",
        "fr": "Mettre à jour les clés de sécurité (archlinux-keyring)",
        "zh": "更新安全密钥 (archlinux-keyring)"
    },
    "up_keyring_desc": {
        "ru": "Исправляет частые ошибки 'corrupted package / invalid PGP signature' перед обновлением",
        "en": "Fixes common 'corrupted package / invalid PGP signature' errors before updating",
        "es": "Corrige errores comunes de 'paquete dañado / firma PGP inválida' antes de actualizar",
        "ja": "更新前のよくある「破損したパッケージ / 無効なPGP署名」エラーを修正します",
        "fr": "Corrige les erreurs fréquentes de paquets corrompus ou signature PGP invalide",
        "zh": "在更新前修复常见的“软件包损坏 / 无效 PGP 签名”错误"
    },
    "up_keyring_btn": {
        "ru": "Обновить ключи",
        "en": "Update Keys",
        "es": "Actualizar claves",
        "ja": "キーを更新",
        "fr": "Mettre à jour les clés",
        "zh": "更新密钥"
    },
    "up_flatpak_title": {
        "ru": "Обновить приложения Flatpak",
        "en": "Update Flatpak Applications",
        "es": "Actualizar aplicaciones Flatpak",
        "ja": "Flatpakアプリの更新",
        "fr": "Mettre à jour les applications Flatpak",
        "zh": "更新 Flatpak 应用"
    },
    "up_flatpak_desc": {
        "ru": "Загружает последние версии установленных Flatpak программ и сред выполнения",
        "en": "Downloads the latest versions of installed Flatpak apps and runtimes",
        "es": "Descarga las últimas versiones de aplicaciones y runtimes Flatpak",
        "ja": "インストール済みFlatpakアプリおよびランタイムの最新版をダウンロードします",
        "fr": "Télécharge les dernières versions des applications et runtimes Flatpak installés",
        "zh": "下载已安装 Flatpak 应用程序和运行时的最新版本"
    },
    "up_flatpak_btn": {
        "ru": "Обновить Flatpak",
        "en": "Update Flatpak",
        "es": "Actualizar Flatpak",
        "ja": "Flatpakを更新",
        "fr": "Mettre à jour Flatpak",
        "zh": "更新 Flatpak"
    },

    # Консоль / Терминал
    "term_ready": {
        "ru": "=== Консоль CleanArch готова к выполнению задач ===\n",
        "en": "=== CleanArch console is ready for tasks ===\n",
        "es": "=== Consola CleanArch lista para tareas ===\n",
        "ja": "=== CleanArchコンソールはタスク実行の準備ができています ===\n",
        "fr": "=== La console CleanArch est prête pour les tâches ===\n",
        "zh": "=== CleanArch 控制台已准备好执行任务 ===\n"
    },
    "term_waiting": {
        "ru": "Ожидание задач...",
        "en": "Waiting for tasks...",
        "es": "Esperando tareas...",
        "ja": "タスク待機中...",
        "fr": "En attente de tâches...",
        "zh": "等待任务中..."
    },
    "term_running": {
        "ru": "Выполняется...",
        "en": "Running...",
        "es": "Ejecutando...",
        "ja": "実行中...",
        "fr": "En cours d'exécution...",
        "zh": "正在执行..."
    },
    "term_success": {
        "ru": "Успешно завершено! ✓",
        "en": "Completed successfully! ✓",
        "es": "¡Completado con éxito! ✓",
        "ja": "正常に完了しました！ ✓",
        "fr": "Terminé avec succès ! ✓",
        "zh": "已成功完成！ ✓"
    },
    "term_error": {
        "ru": "Завершено с ошибкой (код {code}) ✗",
        "en": "Finished with error (code {code}) ✗",
        "es": "Finalizado con error (código {code}) ✗",
        "ja": "エラーで終了しました (コード {code}) ✗",
        "fr": "Terminé avec erreur (code {code}) ✗",
        "zh": "执行出错（退出代码 {code}） ✗"
    },
    "term_stop_tooltip": {
        "ru": "Прервать выполнение",
        "en": "Abort execution",
        "es": "Interrumpir ejecución",
        "ja": "実行を中断",
        "fr": "Interrompre l'exécution",
        "zh": "中断执行"
    },
    "term_copy_tooltip": {
        "ru": "Скопировать весь лог",
        "en": "Copy entire log",
        "es": "Copiar registro completo",
        "ja": "ログ全体をコピー",
        "fr": "Copier tout le journal",
        "zh": "复制完整日志"
    },
    "term_clear_tooltip": {
        "ru": "Очистить вывод",
        "en": "Clear output",
        "es": "Limpiar salida",
        "ja": "出力をクリア",
        "fr": "Effacer la sortie",
        "zh": "清空输出"
    },

    # Диалог пароля
    "pw_title": {
        "ru": "Права администратора",
        "en": "Administrator Privileges",
        "es": "Privilegios de Administrador",
        "ja": "管理者権限",
        "fr": "Privilèges Administrateur",
        "zh": "管理员权限"
    },
    "pw_heading": {
        "ru": "Требуются права администратора",
        "en": "Administrator privileges required",
        "es": "Se requieren privilegios de administrador",
        "ja": "管理者権限が必要です",
        "fr": "Privilèges administrateur requis",
        "zh": "需要管理员权限"
    },
    "pw_body": {
        "ru": "Для очистки системных кэшей и логов введите пароль вашей учётной записи:",
        "en": "Enter your account password to clean system caches and logs:",
        "es": "Ingrese la contraseña de su cuenta para limpiar cachés y registros del sistema:",
        "ja": "システムキャッシュとログを消去するためにアカウントのパスワードを入力してください:",
        "fr": "Entrez le mot de passe de votre compte pour nettoyer les caches et journaux système :",
        "zh": "请输入您的用户密码以清理系统缓存和日志："
    },
    "pw_cancel": {
        "ru": "Отмена",
        "en": "Cancel",
        "es": "Cancelar",
        "ja": "キャンセル",
        "fr": "Annuler",
        "zh": "取消"
    },
    "pw_confirm": {
        "ru": "Подтвердить",
        "en": "Confirm",
        "es": "Confirmar",
        "ja": "確認",
        "fr": "Confirmer",
        "zh": "确认"
    },
    "pw_error_empty": {
        "ru": "Пожалуйста, введите пароль",
        "en": "Please enter your password",
        "es": "Por favor, ingrese su contraseña",
        "ja": "パスワードを入力してください",
        "fr": "Veuillez entrer votre mot de passe",
        "zh": "请输入密码"
    },
    "pw_error_invalid": {
        "ru": "❌ Неверный пароль. Попробуйте снова.",
        "en": "❌ Incorrect password. Try again.",
        "es": "❌ Contraseña incorrecta. Inténtelo de nuevo.",
        "ja": "❌ パスワードが正しくありません。再試行してください。",
        "fr": "❌ Mot de passe incorrect. Réessayez.",
        "zh": "❌ 密码错误。请重试。"
    },
    # Уведомления (Toasts)
    "toast_clean_done": {
        "ru": "Очистка успешно завершена!",
        "en": "Cleaning completed successfully!",
        "es": "¡Limpieza completada con éxito!",
        "ja": "クリーンアップが正常に完了しました！",
        "fr": "Nettoyage terminé avec succès !",
        "zh": "清理已成功完成！"
    },
    "toast_clean_error": {
        "ru": "Произошла ошибка при очистке!",
        "en": "An error occurred during cleanup!",
        "es": "¡Ocurrió un error durante la limpieza!",
        "ja": "クリーンアップ中にエラーが発生しました！",
        "fr": "Une erreur est survenue lors du nettoyage !",
        "zh": "清理过程中发生错误！"
    },
    "toast_update_done": {
        "ru": "Обновление завершено!",
        "en": "Update completed!",
        "es": "¡Actualización completada!",
        "ja": "更新が完了しました！",
        "fr": "Mise à jour terminée !",
        "zh": "更新已完成！"
    },
    "toast_update_error": {
        "ru": "Обновление прервано или завершилось с ошибкой!",
        "en": "Update aborted or failed with an error!",
        "es": "¡La actualización fue cancelada o falló!",
        "ja": "更新が中断されたか、エラーが発生しました！",
        "fr": "La mise à jour a échoué ou a été interrompue !",
        "zh": "更新已中止或失败！"
    },
    "toast_no_selection": {
        "ru": "Выберите хотя бы один пункт для очистки!",
        "en": "Select at least one category to clean!",
        "es": "¡Seleccione al menos una categoría para limpiar!",
        "ja": "消去する項目を少なくとも1つ選択してください！",
        "fr": "Sélectionnez au moins une catégorie à nettoyer !",
        "zh": "请至少选择一项要清理的内容！"
    },
    "toast_log_copied": {
        "ru": "Лог скопирован в буфер",
        "en": "Log copied to clipboard",
        "es": "Registro copiado al portapapeles",
        "ja": "ログをクリップボードにコピーしました",
        "fr": "Journal copié dans le presse-papiers",
        "zh": "日志已复制到剪贴板"
    },
    "toast_task_running": {
        "ru": "Предыдущая задача ещё выполняется!",
        "en": "Previous task is still running!",
        "es": "¡La tarea anterior aún se está ejecutando!",
        "ja": "前のタスクがまだ実行中です！",
        "fr": "La tâche précédente est toujours en cours !",
        "zh": "上一个任务仍在执行中！"
    },
    "toast_lang_changed": {
        "ru": "Язык интерфейса изменён",
        "en": "Interface language changed",
        "es": "Idioma de interfaz cambiado",
        "ja": "表示言語を変更しました",
        "fr": "Langue de l'interface modifiée",
        "zh": "界面语言已更改"
    },
    "status_calculating": {
        "ru": "Выполняется начальный подсчёт...",
        "en": "Initial calculation in progress...",
        "es": "Cálculo inicial en curso...",
        "ja": "初期計算を実行中...",
        "fr": "Calcul initial en cours...",
        "zh": "正在进行初始计算..."
    },
    "status_scanning": {
        "ru": "Сканирование каталогов и журналов...",
        "en": "Scanning directories and journals...",
        "es": "Escaneando directorios y registros...",
        "ja": "ディレクトリとジャーナルをスキャン中...",
        "fr": "Analyse des répertoires et journaux...",
        "zh": "正在扫描目录和日志..."
    },
    "status_selected_summary": {
        "ru": "Выбрано категорий: {count}. Будет освобождено около ~{size}",
        "en": "Selected categories: {count}. Will free approx ~{size}",
        "es": "Categorías seleccionadas: {count}. Se liberará aprox ~{size}",
        "ja": "選択された項目: {count} 件。解放予定: 約 ~{size}",
        "fr": "Catégories sélectionnées : {count}. Libérera environ ~{size}",
        "zh": "已选类别：{count} 个。预计释放空间：~{size}"
    },
    "status_log_cleared": {
        "ru": "Лог очищен",
        "en": "Log cleared",
        "es": "Registro limpiado",
        "ja": "ログを消去しました",
        "fr": "Journal effacé",
        "zh": "日志已清空"
    },
    "log_aborted_by_user": {
        "ru": "\n[Прервано пользователем]\n",
        "en": "\n[Aborted by user]\n",
        "es": "\n[Interrumpido por el usuario]\n",
        "ja": "\n[ユーザーによって中断されました]\n",
        "fr": "\n[Interrompu par l'utilisateur]\n",
        "zh": "\n[用户已中断]\n"
    },
    "mascot_ready": {
        "ru": "Готова к работе",
        "en": "Ready to work",
        "es": "Listo para trabajar",
        "ja": "準備完了",
        "fr": "Prêt à travailler",
        "zh": "准备就绪"
    },
    "mascot_scanned_sub": {
        "ru": "Найдено: {extra}",
        "en": "Found: {extra}",
        "es": "Encontrado: {extra}",
        "ja": "発見: {extra}",
        "fr": "Trouvé : {extra}",
        "zh": "发现：{extra}"
    },
    "mascot_done_sub": {
        "ru": "Система оптимизирована",
        "en": "System optimized",
        "es": "Sistema optimizado",
        "ja": "システム最適化完了",
        "fr": "Système optimisé",
        "zh": "系统已优化"
    },
    "mascot_error_sub": {
        "ru": "Требуется внимание",
        "en": "Attention required",
        "es": "Atención requerida",
        "ja": "確認が必要です",
        "fr": "Attention requise",
        "zh": "需要注意"
    },

    # Подробности О программе
    "about_comments": {
        "ru": (
            "CleanArch — современный графический центр оптимизации и очистки системы Arch Linux на базе GTK 4 и Libadwaita.\n\n"
            "✨ Основные возможности:\n"
            "• Полная и выборочная очистка кэшей pacman и сборщика yay (AUR)\n"
            "• Удаление неиспользуемых пакетов-зависимостей (orphans) и старых логов journalctl\n"
            "• Очистка пользовательских кэшей миниатюр и неиспользуемых рантаймов Flatpak\n"
            "• Безопасное выполнение через sudo с автоматической валидацией пароля\n"
            "• Быстрое обновление всей системы, ключей archlinux-keyring и Flatpak\n"
            "• Интерактивный персонаж-помощник с живыми статусами"
        ),
        "en": (
            "CleanArch is a modern system cleanup and optimization utility for Arch Linux powered by GTK 4 and Libadwaita.\n\n"
            "✨ Key features:\n"
            "• Full and selective cleanup of pacman and yay (AUR) build caches\n"
            "• Removal of orphan packages and systemd journalctl vacuuming\n"
            "• Clearing user thumbnail caches and unused Flatpak runtimes\n"
            "• Secure execution via sudo with one-time password verification\n"
            "• One-click system, archlinux-keyring, and Flatpak updates\n"
            "• Interactive mascot assistant with real-time status dialogues"
        ),
        "es": (
            "CleanArch es una moderna utilidad gráfica para la limpieza y optimización de Arch Linux basada en GTK 4 y Libadwaita.\n\n"
            "✨ Características principales:\n"
            "• Limpieza completa y selectiva de cachés de pacman y yay (AUR)\n"
            "• Eliminación de paquetes huérfanos y compactación de journalctl\n"
            "• Limpieza de miniaturas y runtimes de Flatpak no utilizados\n"
            "• Ejecución segura con sudo y verificación de contraseña única\n"
            "• Actualización rápida del sistema, archlinux-keyring y Flatpak\n"
            "• Mascota interactiva con diálogos de estado en tiempo real"
        ),
        "ja": (
            "CleanArchは、GTK 4とLibadwaitaを基盤とするArch Linux向けのモダンなシステムクリーンアップおよび最適化ユーティリティです。\n\n"
            "✨ 主な機能:\n"
            "• pacmanおよびyay (AUR) キャッシュの完全・選択的クリーンアップ\n"
            "• 孤立パッケージの削除とjournalctlログの短縮\n"
            "• サムネイルキャッシュと未使用Flatpakランタイムの削除\n"
            "• 1回のパスワード認証による安全なsudoバックグラウンド実行\n"
            "• システム全体、archlinux-keyring、Flatpakのワンクリック更新\n"
            "• リアルタイムで状況を案内するインタラクティブなマスコット"
        ),
        "fr": (
            "CleanArch est un utilitaire moderne d'optimisation et de nettoyage pour Arch Linux propulsé par GTK 4 et Libadwaita.\n\n"
            "✨ Fonctionnalités principales :\n"
            "• Nettoyage complet ou sélectif des caches pacman et yay (AUR)\n"
            "• Suppression des paquets orphelins et réduction des journaux systemd\n"
            "• Nettoyage des miniatures et des runtimes Flatpak inutilisés\n"
            "• Exécution sécurisée via sudo avec validation unique du mot de passe\n"
            "• Mise à jour rapide du système, du trousseau de clés et de Flatpak\n"
            "• Mascotte interactive avec dialogues de statut en temps réel"
        ),
        "zh": (
            "CleanArch 是一款基于 GTK 4 和 Libadwaita 构建的现代 Arch Linux 系统清理与优化图形工具。\n\n"
            "✨ 核心特性：\n"
            "• 彻底或有选择地清理 pacman 和 yay (AUR) 缓存\n"
            "• 智能移除孤立软件包并精简 systemd 日志\n"
            "• 清理用户缩略图缓存及未使用的 Flatpak 运行库\n"
            "• 一次输入密码即可安全执行 sudo 后台特权操作\n"
            "• 一键更新整个系统、archlinux-keyring 密钥库及 Flatpak\n"
            "• 伴随实时状态反馈的拟人化看板娘助手"
        )
    }
}

def load_saved_language() -> str:
    """Загружает сохранённый язык из конфигурации или определяет по системе."""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                lang = data.get("language")
                if lang in SUPPORTED_LANGUAGES:
                    return lang
    except Exception:
        pass

    # Определение по системной локали
    sys_lang = os.environ.get("LANG", "").split(".")[0].split("_")[0].lower()
    if sys_lang in SUPPORTED_LANGUAGES:
        return sys_lang

    return "ru"

def save_language(lang: str):
    """Сохраняет выбранный язык в конфигурационный файл."""
    global _current_lang
    if lang in SUPPORTED_LANGUAGES:
        _current_lang = lang
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump({"language": lang}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

def set_language(lang: str):
    """Устанавливает текущий активный язык."""
    global _current_lang
    if lang in SUPPORTED_LANGUAGES:
        _current_lang = lang
        save_language(lang)

def get_current_language() -> str:
    """Возвращает код текущего языка."""
    return _current_lang

def tr(key: str, **kwargs) -> str:
    """Получает переведённую строку по ключу для текущего языка с подстановкой параметров."""
    lang_dict = TRANSLATIONS.get(key)
    if not lang_dict:
        return key

    text = lang_dict.get(_current_lang) or lang_dict.get("en") or lang_dict.get("ru") or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

# Инициализация языка при импорте
_current_lang = load_saved_language()

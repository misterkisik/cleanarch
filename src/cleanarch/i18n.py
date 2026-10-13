"""
Модуль интернационализации (i18n) для CleanArch.
Поддерживаемые языки: ru (Русский), en (English), es (Español), fr (Français).
"""

import os
import json
from typing import Dict, Any

CONFIG_DIR = os.path.expanduser("~/.config/cleanarch")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

SUPPORTED_LANGUAGES: Dict[str, str] = {
    "ru": "Русский",
    "en": "English",
    "es": "Español",
    "fr": "Français"
}

_current_lang = "ru"

TRANSLATIONS: Dict[str, Dict[str, str]] = {   'app_title': {'ru': 'CleanArch', 'en': 'CleanArch', 'es': 'CleanArch', 'fr': 'CleanArch'},
    'app_subtitle': {   'ru': 'Очистка и оптимизация Arch Linux',
                        'en': 'Arch Linux cleaning and optimization',
                        'es': 'Limpieza y optimización de Arch Linux',
                        'fr': "Nettoyage et optimisation d'Arch Linux"},
    'tab_clean': {'ru': 'Очистка', 'en': 'Clean', 'es': 'Limpieza', 'fr': 'Nettoyage'},
    'tab_update': {'ru': 'Обновление', 'en': 'Update', 'es': 'Actualización', 'fr': 'Mise à jour'},
    'tab_terminal': {   'ru': 'Консоль / Лог',
                        'en': 'Console / Log',
                        'es': 'Consola / Registro',
                        'fr': 'Console / Journal'},
    'menu_about': {'ru': 'О программе', 'en': 'About', 'es': 'Acerca de', 'fr': 'À propos'},
    'menu_language': {'ru': 'Язык (Language)', 'en': 'Language', 'es': 'Idioma', 'fr': 'Langue'},
    'mascot_name': {   'ru': 'CleanArch Помощник',
                       'en': 'CleanArch Assistant',
                       'es': 'Asistente CleanArch',
                       'fr': 'Assistant CleanArch'},
    'mascot_idle': {   'ru': 'Привет! Пора навести чистоту в Arch Linux! Выберите кэши для очистки и нажмите кнопку '
                             'запуска.',
                       'en': 'Hello! Time to clean up Arch Linux! Select caches to clean and press start.',
                       'es': '¡Hola! ¡Es hora de limpiar Arch Linux! Seleccione las cachés para limpiar y presione '
                             'inicio.',
                       'fr': 'Bonjour ! Il est temps de nettoyer Arch Linux ! Sélectionnez les caches à vider et '
                             'lancez le nettoyage.'},
    'mascot_idle_sub': {   'ru': 'Готова к работе',
                           'en': 'Ready to work',
                           'es': 'Listo para trabajar',
                           'fr': 'Prêt à travailler'},
    'mascot_scanning': {   'ru': 'Сканирую диски... Проверяю размеры кэшей pacman, yay и системных журналов.',
                           'en': 'Scanning drives... Checking sizes of pacman, yay, and system logs.',
                           'es': 'Escaneando discos... Verificando tamaños de pacman, yay y registros.',
                           'fr': 'Analyse des disques... Vérification de la taille de pacman, yay et des journaux '
                                 'système.'},
    'mascot_scanning_sub': {   'ru': 'Идет подсчет объемов мусора...',
                               'en': 'Calculating junk size...',
                               'es': 'Calculando tamaño de residuos...',
                               'fr': 'Calcul de la taille des données inutiles...'},
    'mascot_scanned': {   'ru': 'Сканирование завершено! Обнаружено мусора: {extra}. Готова освободить место!',
                          'en': 'Scanning complete! Found junk: {extra}. Ready to free space!',
                          'es': '¡Escaneo completo! Residuos encontrados: {extra}. ¡Listo para liberar espacio!',
                          'fr': "Analyse terminée ! Données trouvées : {extra}. Prêt à libérer de l'espace !"},
    'mascot_cleaning': {   'ru': 'Очищаю кэши и ненужные пакеты... Система будет работать быстрее и чище!',
                           'en': 'Cleaning caches and unneeded packages... The system will run faster and cleaner!',
                           'es': 'Limpiando cachés y paquetes innecesarios... ¡El sistema funcionará más rápido y '
                                 'limpio!',
                           'fr': 'Nettoyage des caches et paquets inutiles... Le système sera plus rapide et propre !'},
    'mascot_cleaning_sub': {   'ru': 'Выполняется очистка...',
                               'en': 'Cleaning in progress...',
                               'es': 'Limpieza en progreso...',
                               'fr': 'Nettoyage en cours...'},
    'mascot_done': {   'ru': 'Отличная работа! Очистка успешно завершена, диск свободен ✨',
                       'en': 'Great job! Cleaning completed successfully, disk space freed ✨',
                       'es': '¡Buen trabajo! Limpieza completada con éxito, espacio en disco liberado ✨',
                       'fr': 'Super travail ! Nettoyage terminé avec succès, espace disque libéré ✨'},
    'mascot_updating': {   'ru': 'Обновляю систему... Загружаю свежие версии пакетов Arch Linux!',
                           'en': 'Updating system... Downloading latest Arch Linux packages!',
                           'es': 'Actualizando sistema... ¡Descargando las últimas versiones de paquetes!',
                           'fr': 'Mise à jour du système... Téléchargement des derniers paquets Arch Linux !'},
    'mascot_updating_sub': {   'ru': 'Идет процесс обновления...',
                               'en': 'Update in progress...',
                               'es': 'Actualización en progreso...',
                               'fr': 'Mise à jour en cours...'},
    'mascot_error': {   'ru': 'Ой! В процессе возникла ошибка. Перейдите во вкладку «Консоль / Лог», чтобы посмотреть '
                              'подробности.',
                        'en': "Oops! An error occurred. Check the 'Console / Log' tab for details.",
                        'es': "¡Ups! Ocurrió un error. Revise la pestaña 'Consola / Registro' para ver detalles.",
                        'fr': "Oups ! Une erreur est survenue. Consultez l'onglet « Console / Journal » pour plus de "
                              'détails.'},
    'clean_title': {   'ru': 'Очистка дискового пространства',
                       'en': 'Disk Space Cleanup',
                       'es': 'Limpieza de espacio en disco',
                       'fr': "Nettoyage de l'espace disque"},
    'clean_desc': {   'ru': 'Выберите категории мусора и кэшей, которые хотите удалить. Системные операции '
                            'автоматически запросят подтверждение.',
                      'en': 'Select cache and junk categories you want to remove. System tasks will request '
                            'authorization automatically.',
                      'es': 'Seleccione las categorías de caché y residuos que desea eliminar. Las tareas del sistema '
                            'solicitarán confirmación.',
                      'fr': 'Sélectionnez les catégories de caches et déchets à supprimer. Les opérations système '
                            'demanderont une autorisation.'},
    'total_to_free': {   'ru': 'Всего можно освободить',
                         'en': 'Total space to free',
                         'es': 'Total a liberar',
                         'fr': 'Total à libérer'},
    'btn_clean': {   'ru': 'Очистить выбранное',
                     'en': 'Clean Selected',
                     'es': 'Limpiar seleccionados',
                     'fr': 'Nettoyer la sélection'},
    'btn_rescan_tooltip': {   'ru': 'Пересчитать размеры кэшей',
                              'en': 'Recalculate cache sizes',
                              'es': 'Recalcular tamaños de caché',
                              'fr': 'Recalculer les tailles de cache'},
    'categories_group_title': {   'ru': 'Категории для очистки',
                                  'en': 'Cleanup Categories',
                                  'es': 'Categorías de limpieza',
                                  'fr': 'Catégories de nettoyage'},
    'cat_pacman_title': {   'ru': 'Кэш пакетов pacman (полная очистка)',
                            'en': 'Pacman package cache (full clean)',
                            'es': 'Caché de paquetes pacman (completo)',
                            'fr': 'Cache des paquets pacman (complet)'},
    'cat_pacman_desc': {   'ru': 'Удаляет все архивы пакетов (.pkg.tar.zst) из /var/cache/pacman/pkg (-Scc) и '
                                 'временные файлы',
                           'en': 'Removes all package archives (.pkg.tar.zst) from /var/cache/pacman/pkg (-Scc) and '
                                 'temp files',
                           'es': 'Elimina todos los archivos de paquetes (.pkg.tar.zst) de /var/cache/pacman/pkg '
                                 '(-Scc) y temporales',
                           'fr': 'Supprime toutes les archives de paquets (.pkg.tar.zst) de /var/cache/pacman/pkg '
                                 '(-Scc) et fichiers temporaires'},
    'cat_yay_title': {   'ru': 'Кэш сборщика AUR (yay)',
                         'en': 'AUR build cache (yay)',
                         'es': 'Caché de compilación AUR (yay)',
                         'fr': 'Cache de construction AUR (yay)'},
    'cat_yay_desc': {   'ru': 'Кэшированные репозитории и собранные исходники в ~/.cache/yay',
                        'en': 'Cached repositories and build sources in ~/.cache/yay',
                        'es': 'Repositorios en caché y fuentes compiladas en ~/.cache/yay',
                        'fr': 'Dépôts en cache et sources compilées dans ~/.cache/yay'},
    'cat_journal_title': {   'ru': 'Системный журнал (journalctl)',
                             'en': 'System journal (journalctl)',
                             'es': 'Registro del sistema (journalctl)',
                             'fr': 'Journal système (journalctl)'},
    'cat_journal_desc': {   'ru': 'Старые системные логи служб (будут сохранены логи за последние 3 дня)',
                            'en': 'Old service logs (logs from the last 3 days will be preserved)',
                            'es': 'Registros antiguos de servicios (se conservan los últimos 3 días)',
                            'fr': 'Anciens journaux des services (les 3 derniers jours sont conservés)'},
    'cat_orphans_title': {   'ru': 'Пакеты-сироты (Orphans)',
                             'en': 'Orphan packages',
                             'es': 'Paquetes huérfanos',
                             'fr': 'Paquets orphelins'},
    'cat_orphans_desc': {   'ru': 'Неиспользуемые пакеты-зависимости, оставшиеся после удаления программ ({count} шт.)',
                            'en': 'Unused dependencies left after uninstalling programs ({count} pkgs)',
                            'es': 'Dependencias no utilizadas tras desinstalar programas ({count} paqs)',
                            'fr': 'Dépendances inutilisées après désinstallation ({count} paquets)'},
    'cat_thumbnails_title': {   'ru': 'Кэш миниатюр изображений',
                                'en': 'Image thumbnails cache',
                                'es': 'Caché de miniaturas de imágenes',
                                'fr': "Cache des miniatures d'images"},
    'cat_thumbnails_desc': {   'ru': 'Временные превью картинок и видео в ~/.cache/thumbnails',
                               'en': 'Temporary previews of images and videos in ~/.cache/thumbnails',
                               'es': 'Vistas previas temporales en ~/.cache/thumbnails',
                               'fr': "Aperçus temporaires d'images et vidéos dans ~/.cache/thumbnails"},
    'cat_flatpak_title': {   'ru': 'Неиспользуемые рантаймы Flatpak',
                             'en': 'Unused Flatpak runtimes',
                             'es': 'Runtimes de Flatpak no utilizados',
                             'fr': 'Runtimes Flatpak inutilisés'},
    'cat_flatpak_desc': {   'ru': 'Библиотеки Flatpak, которые больше не нужны ни одному приложению ({count} шт.)',
                            'en': 'Flatpak runtimes no longer required by any application ({count} items)',
                            'es': 'Bibliotecas Flatpak que ya no necesita ninguna aplicación ({count} elem.)',
                            'fr': 'Bibliothèques Flatpak qui ne sont plus nécessaires ({count} éléments)'},
    'update_title': {   'ru': 'Обновление системы и репозиториев',
                        'en': 'System and Repository Update',
                        'es': 'Actualización del sistema y repositorios',
                        'fr': 'Mise à jour du système et des dépôts'},
    'update_desc': {   'ru': 'Регулярное обновление обеспечивает безопасность и актуальность вашего ПО в Arch Linux.',
                       'en': 'Regular updates ensure your software remains secure and up-to-date in Arch Linux.',
                       'es': 'Las actualizaciones periódicas garantizan la seguridad y estabilidad en Arch Linux.',
                       'fr': 'Des mises à jour régulières assurent la sécurité et la stabilité de votre système Arch '
                             'Linux.'},
    'up_full_title': {   'ru': 'Полное обновление (pacman + AUR)',
                         'en': 'Full System Update (pacman + AUR)',
                         'es': 'Actualización completa (pacman + AUR)',
                         'fr': 'Mise à jour complète (pacman + AUR)'},
    'up_full_desc': {   'ru': 'Синхронизирует репозитории и обновляет все пакеты системы и пользовательские программы '
                              'AUR',
                        'en': 'Synchronizes mirrors and updates all system packages and AUR programs',
                        'es': 'Sincroniza repositorios y actualiza todos los paquetes del sistema y programas AUR',
                        'fr': 'Synchronise les dépôts et met à jour tous les paquets du système et AUR'},
    'up_full_btn': {   'ru': 'Обновить систему',
                       'en': 'Update System',
                       'es': 'Actualizar sistema',
                       'fr': 'Mettre à jour le système'},
    'up_keyring_title': {   'ru': 'Обновить ключи безопасности (archlinux-keyring)',
                            'en': 'Update Security Keys (archlinux-keyring)',
                            'es': 'Actualizar claves de seguridad (archlinux-keyring)',
                            'fr': 'Mettre à jour les clés de sécurité (archlinux-keyring)'},
    'up_keyring_desc': {   'ru': "Исправляет частые ошибки 'corrupted package / invalid PGP signature' перед "
                                 'обновлением',
                           'en': "Fixes common 'corrupted package / invalid PGP signature' errors before updating",
                           'es': "Corrige errores comunes de 'paquete dañado / firma PGP inválida' antes de actualizar",
                           'fr': 'Corrige les erreurs fréquentes de paquets corrompus ou signature PGP invalide'},
    'up_keyring_btn': {   'ru': 'Обновить ключи',
                          'en': 'Update Keys',
                          'es': 'Actualizar claves',
                          'fr': 'Mettre à jour les clés'},
    'up_flatpak_title': {   'ru': 'Обновить приложения Flatpak',
                            'en': 'Update Flatpak Applications',
                            'es': 'Actualizar aplicaciones Flatpak',
                            'fr': 'Mettre à jour les applications Flatpak'},
    'up_flatpak_desc': {   'ru': 'Загружает последние версии установленных Flatpak программ и сред выполнения',
                           'en': 'Downloads the latest versions of installed Flatpak apps and runtimes',
                           'es': 'Descarga las últimas versiones de aplicaciones y runtimes Flatpak',
                           'fr': 'Télécharge les dernières versions des applications et runtimes Flatpak installés'},
    'up_flatpak_btn': {   'ru': 'Обновить Flatpak',
                          'en': 'Update Flatpak',
                          'es': 'Actualizar Flatpak',
                          'fr': 'Mettre à jour Flatpak'},
    'term_ready': {   'ru': '=== Консоль CleanArch готова к выполнению задач ===\n',
                      'en': '=== CleanArch console is ready for tasks ===\n',
                      'es': '=== Consola CleanArch lista para tareas ===\n',
                      'fr': '=== La console CleanArch est prête pour les tâches ===\n'},
    'term_waiting': {   'ru': 'Ожидание задач...',
                        'en': 'Waiting for tasks...',
                        'es': 'Esperando tareas...',
                        'fr': 'En attente de tâches...'},
    'term_running': {   'ru': 'Выполняется...',
                        'en': 'Running...',
                        'es': 'Ejecutando...',
                        'fr': "En cours d'exécution..."},
    'term_success': {   'ru': 'Успешно завершено! ✓',
                        'en': 'Completed successfully! ✓',
                        'es': '¡Completado con éxito! ✓',
                        'fr': 'Terminé avec succès ! ✓'},
    'term_error': {   'ru': 'Завершено с ошибкой (код {code}) ✗',
                      'en': 'Finished with error (code {code}) ✗',
                      'es': 'Finalizado con error (código {code}) ✗',
                      'fr': 'Terminé avec erreur (code {code}) ✗'},
    'term_stop_tooltip': {   'ru': 'Прервать выполнение',
                             'en': 'Abort execution',
                             'es': 'Interrumpir ejecución',
                             'fr': "Interrompre l'exécution"},
    'term_copy_tooltip': {   'ru': 'Скопировать весь лог',
                             'en': 'Copy entire log',
                             'es': 'Copiar registro completo',
                             'fr': 'Copier tout le journal'},
    'term_clear_tooltip': {   'ru': 'Очистить вывод',
                              'en': 'Clear output',
                              'es': 'Limpiar salida',
                              'fr': 'Effacer la sortie'},
    'pw_title': {   'ru': 'Права администратора',
                    'en': 'Administrator Privileges',
                    'es': 'Privilegios de Administrador',
                    'fr': 'Privilèges Administrateur'},
    'pw_heading': {   'ru': 'Требуются права администратора',
                      'en': 'Administrator privileges required',
                      'es': 'Se requieren privilegios de administrador',
                      'fr': 'Privilèges administrateur requis'},
    'pw_body': {   'ru': 'Для очистки системных кэшей и логов введите пароль вашей учётной записи:',
                   'en': 'Enter your account password to clean system caches and logs:',
                   'es': 'Ingrese la contraseña de su cuenta para limpiar cachés y registros del sistema:',
                   'fr': 'Entrez le mot de passe de votre compte pour nettoyer les caches et journaux système :'},
    'pw_cancel': {'ru': 'Отмена', 'en': 'Cancel', 'es': 'Cancelar', 'fr': 'Annuler'},
    'pw_confirm': {'ru': 'Подтвердить', 'en': 'Confirm', 'es': 'Confirmar', 'fr': 'Confirmer'},
    'pw_error_empty': {   'ru': 'Пожалуйста, введите пароль',
                          'en': 'Please enter your password',
                          'es': 'Por favor, ingrese su contraseña',
                          'fr': 'Veuillez entrer votre mot de passe'},
    'pw_error_invalid': {   'ru': '❌ Неверный пароль. Попробуйте снова.',
                            'en': '❌ Incorrect password. Try again.',
                            'es': '❌ Contraseña incorrecta. Inténtelo de nuevo.',
                            'fr': '❌ Mot de passe incorrect. Réessayez.'},
    'toast_clean_done': {   'ru': 'Очистка успешно завершена!',
                            'en': 'Cleaning completed successfully!',
                            'es': '¡Limpieza completada con éxito!',
                            'fr': 'Nettoyage terminé avec succès !'},
    'toast_clean_error': {   'ru': 'Произошла ошибка при очистке!',
                             'en': 'An error occurred during cleanup!',
                             'es': '¡Ocurrió un error durante la limpieza!',
                             'fr': 'Une erreur est survenue lors du nettoyage !'},
    'toast_update_done': {   'ru': 'Обновление завершено!',
                             'en': 'Update completed!',
                             'es': '¡Actualización completada!',
                             'fr': 'Mise à jour terminée !'},
    'toast_update_error': {   'ru': 'Обновление прервано или завершилось с ошибкой!',
                              'en': 'Update aborted or failed with an error!',
                              'es': '¡La actualización fue cancelada o falló!',
                              'fr': 'La mise à jour a échoué ou a été interrompue !'},
    'toast_no_selection': {   'ru': 'Выберите хотя бы один пункт для очистки!',
                              'en': 'Select at least one category to clean!',
                              'es': '¡Seleccione al menos una categoría para limpiar!',
                              'fr': 'Sélectionnez au moins une catégorie à nettoyer !'},
    'toast_log_copied': {   'ru': 'Лог скопирован в буфер',
                            'en': 'Log copied to clipboard',
                            'es': 'Registro copiado al portapapeles',
                            'fr': 'Journal copié dans le presse-papiers'},
    'toast_task_running': {   'ru': 'Предыдущая задача ещё выполняется!',
                              'en': 'Previous task is still running!',
                              'es': '¡La tarea anterior aún se está ejecutando!',
                              'fr': 'La tâche précédente est toujours en cours !'},
    'toast_lang_changed': {   'ru': 'Язык интерфейса изменён',
                              'en': 'Interface language changed',
                              'es': 'Idioma de interfaz cambiado',
                              'fr': "Langue de l'interface modifiée"},
    'status_calculating': {   'ru': 'Выполняется начальный подсчёт...',
                              'en': 'Initial calculation in progress...',
                              'es': 'Cálculo inicial en curso...',
                              'fr': 'Calcul initial en cours...'},
    'status_scanning': {   'ru': 'Сканирование каталогов и журналов...',
                           'en': 'Scanning directories and journals...',
                           'es': 'Escaneando directorios y registros...',
                           'fr': 'Analyse des répertoires et journaux...'},
    'status_selected_summary': {   'ru': 'Выбрано категорий: {count}. Будет освобождено около ~{size}',
                                   'en': 'Selected categories: {count}. Will free approx ~{size}',
                                   'es': 'Categorías seleccionadas: {count}. Se liberará aprox ~{size}',
                                   'fr': 'Catégories sélectionnées : {count}. Libérera environ ~{size}'},
    'status_log_cleared': {'ru': 'Лог очищен', 'en': 'Log cleared', 'es': 'Registro limpiado', 'fr': 'Journal effacé'},
    'log_aborted_by_user': {   'ru': '\n[Прервано пользователем]\n',
                               'en': '\n[Aborted by user]\n',
                               'es': '\n[Interrumpido por el usuario]\n',
                               'fr': "\n[Interrompu par l'utilisateur]\n"},
    'mascot_ready': {   'ru': 'Готова к работе',
                        'en': 'Ready to work',
                        'es': 'Listo para trabajar',
                        'fr': 'Prêt à travailler'},
    'mascot_scanned_sub': {   'ru': 'Найдено: {extra}',
                              'en': 'Found: {extra}',
                              'es': 'Encontrado: {extra}',
                              'fr': 'Trouvé : {extra}'},
    'mascot_done_sub': {   'ru': 'Система оптимизирована',
                           'en': 'System optimized',
                           'es': 'Sistema optimizado',
                           'fr': 'Système optimisé'},
    'mascot_error_sub': {   'ru': 'Требуется внимание',
                            'en': 'Attention required',
                            'es': 'Atención requerida',
                            'fr': 'Attention requise'},
    'about_comments': {   'ru': 'CleanArch — современный графический центр оптимизации и очистки системы Arch Linux на '
                                'базе GTK 4 и Libadwaita.\n'
                                '\n'
                                '✨ Основные возможности:\n'
                                '• Полная и выборочная очистка кэшей pacman и сборщика yay (AUR)\n'
                                '• Удаление неиспользуемых пакетов-зависимостей (orphans) и старых логов journalctl\n'
                                '• Очистка пользовательских кэшей миниатюр и неиспользуемых рантаймов Flatpak\n'
                                '• Безопасное выполнение через sudo с автоматической валидацией пароля\n'
                                '• Быстрое обновление всей системы, ключей archlinux-keyring и Flatpak\n'
                                '• Интерактивный персонаж-помощник с живыми статусами',
                          'en': 'CleanArch is a modern system cleanup and optimization utility for Arch Linux powered '
                                'by GTK 4 and Libadwaita.\n'
                                '\n'
                                '✨ Key features:\n'
                                '• Full and selective cleanup of pacman and yay (AUR) build caches\n'
                                '• Removal of orphan packages and systemd journalctl vacuuming\n'
                                '• Clearing user thumbnail caches and unused Flatpak runtimes\n'
                                '• Secure execution via sudo with one-time password verification\n'
                                '• One-click system, archlinux-keyring, and Flatpak updates\n'
                                '• Interactive mascot assistant with real-time status dialogues',
                          'es': 'CleanArch es una moderna utilidad gráfica para la limpieza y optimización de Arch '
                                'Linux basada en GTK 4 y Libadwaita.\n'
                                '\n'
                                '✨ Características principales:\n'
                                '• Limpieza completa y selectiva de cachés de pacman y yay (AUR)\n'
                                '• Eliminación de paquetes huérfanos y compactación de journalctl\n'
                                '• Limpieza de miniaturas y runtimes de Flatpak no utilizados\n'
                                '• Ejecución segura con sudo y verificación de contraseña única\n'
                                '• Actualización rápida del sistema, archlinux-keyring y Flatpak\n'
                                '• Mascota interactiva con diálogos de estado en tiempo real',
                          'fr': "CleanArch est un utilitaire moderne d'optimisation et de nettoyage pour Arch Linux "
                                'propulsé par GTK 4 et Libadwaita.\n'
                                '\n'
                                '✨ Fonctionnalités principales :\n'
                                '• Nettoyage complet ou sélectif des caches pacman et yay (AUR)\n'
                                '• Suppression des paquets orphelins et réduction des journaux systemd\n'
                                '• Nettoyage des miniatures et des runtimes Flatpak inutilisés\n'
                                '• Exécution sécurisée via sudo avec validation unique du mot de passe\n'
                                '• Mise à jour rapide du système, du trousseau de clés et de Flatpak\n'
                                '• Mascotte interactive avec dialogues de statut en temps réel'},
    'welcome_title': {   'ru': 'Добро пожаловать в CleanArch',
                         'en': 'Welcome to CleanArch',
                         'es': 'Bienvenido a CleanArch',
                         'fr': 'Bienvenue dans CleanArch'},
    'welcome_heading': {   'ru': 'Выберите язык',
                           'en': 'Select Language',
                           'es': 'Seleccionar idioma',
                           'fr': 'Choisir la langue'},
    'welcome_subtitle': {   'ru': 'Пожалуйста, выберите предпочитаемый язык интерфейса для продолжения работы с '
                                  'программой.',
                            'en': 'Please choose your preferred interface language to continue.',
                            'es': 'Por favor, elija su idioma de interfaz preferido para continuar.',
                            'fr': "Veuillez choisir votre langue d'interface préférée pour continuer."},
    'btn_continue': {'ru': 'Продолжить', 'en': 'Continue', 'es': 'Continuar', 'fr': 'Continuer'}}

def is_first_run() -> bool:
    """Проверяет, завершена ли первоначальная настройка языка."""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return not data.get("first_run_done", False)
    except Exception:
        pass
    return True

def mark_first_run_done():
    """Отмечает, что выбор языка при первом запуске выполнен."""
    global _current_lang
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        data = {}
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        data["language"] = _current_lang
        data["first_run_done"] = True
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

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

def save_language(lang: str, first_run_done: bool = True):
    """Сохраняет выбранный язык в конфигурационный файл."""
    global _current_lang
    if lang in SUPPORTED_LANGUAGES:
        _current_lang = lang
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            data = {}
            if os.path.exists(CONFIG_PATH):
                try:
                    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    pass
            data["language"] = lang
            if first_run_done:
                data["first_run_done"] = True
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

def set_language(lang: str, first_run_done: bool = True):
    """Устанавливает текущий активный язык."""
    global _current_lang
    if lang in SUPPORTED_LANGUAGES:
        _current_lang = lang
        save_language(lang, first_run_done=first_run_done)

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

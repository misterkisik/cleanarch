# CleanArch 🧹✨

**CleanArch** — графическая утилита для очистки дискового пространства, кэшей и обновления системы в **Arch Linux** (Manjaro, EndeavourOS и др.) на базе **GTK 4 / Libadwaita**.

В левой части окна вас встречает персонаж-помощник (маскот) с живыми диалогами и подсказками, а в правой — инструменты анализа, очистки и встроенная консоль выполнения.

---

## Возможности

1. 🧽 **Очистка кэшей и освобождение диска**:
   * **Кэш pacman** (`/var/cache/pacman/pkg`) — безопасная очистка старых версий пакетов (сохраняются 2 последние версии на случай отката).
   * **Кэш сборщика AUR (yay)** (`~/.cache/yay`) — удаление временных файлов сборки и исходников.
   * **Системный журнал** (`systemd-journald`) — сокращение старых логов с сохранением журналов за последние 3 дня.
   * **Пакеты-сироты (Orphans)** — поиск и удаление неиспользуемых библиотек-зависимостей.
   * **Кэш миниатюр** (`~/.cache/thumbnails`) — очистка временных превью картинок и видео.
   * **Flatpak** — удаление неиспользуемых рантаймов (`flatpak uninstall --unused`).
   * **Подсчёт размера**: приложение автоматически вычисляет объём освобождаемого места в реальном времени.

2. 🚀 **Обновление системы**:
   * Полное обновление системы и пакетов AUR в один клик (`yay -Syu` / `pacman -Syu`).
   * Обновление связки ключей `archlinux-keyring` (устраняет ошибки битых PGP-подписей).
   * Обновление изолированных приложений Flatpak.

3. 💻 **Встроенная консоль**:
   * Просмотр логов выполнения команд в реальном времени прямо в окне программы.
   * Кнопки копирования лога, очистки и прерывания процесса.

4. 👧 **Персонаж-маскот слева**:
   * Отображает статус системы, комментирует процесс сканирования, очистки и обновления через диалоговое облачко.

---

## 🏃 Быстрый запуск

### Из любого терминала:
```bash
cleanarch
```
*(или `cleanarch & disown`, чтобы сразу освободить терминал)*

### Из меню приложений GNOME:
Найдите **CleanArch** в списке программ.

---

## 📦 Сборка и установка через makepkg

Собрать официальный пакет Arch Linux локально:
```bash
cd /home/misterkisik/.gemini/antigravity/scratch/cleanarch
makepkg -p PKGBUILD.local -si
```
Пакет будет установлен в систему со всеми ярлыками и иконками в `/usr/bin/cleanarch`.

---

## 🌐 Как выложить в AUR, чтобы работало `yay -S cleanarch`

### Шаг 1: Загрузка на GitHub
1. Создайте публичный репозиторий `https://github.com/misterkisik/cleanarch`.
2. Загрузите код:
   ```bash
   cd /home/misterkisik/.gemini/antigravity/scratch/cleanarch
   git init
   git add .
   git commit -m "feat: initial release 1.0.0"
   git branch -M main
   git remote add origin https://github.com/misterkisik/cleanarch.git
   git push -u origin main
   ```
3. Создайте тег релиза:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

### Шаг 2: Создание пакета в AUR
1. Зарегистрируйтесь на [aur.archlinux.org](https://aur.archlinux.org/) и добавьте SSH-ключ в профиль.
2. Склонируйте репозиторий пакета:
   ```bash
   git clone ssh://aur@aur.archlinux.org/cleanarch.git ~/aur-cleanarch
   cd ~/aur-cleanarch
   ```
3. Скопируйте файл `PKGBUILD`:
   ```bash
   cp /home/misterkisik/.gemini/antigravity/scratch/cleanarch/PKGBUILD .
   ```
4. Сгенерируйте файл `.SRCINFO`:
   ```bash
   makepkg --printsrcinfo > .SRCINFO
   ```
5. Отправьте пакет в AUR:
   ```bash
   git add PKGBUILD .SRCINFO
   git commit -m "feat: initial import 1.0.0"
   git push origin master
   ```

Теперь любой пользователь в мире сможет установить вашу утилиту:
```bash
yay -S cleanarch
```
И запускать её одной командой:
```bash
cleanarch
```

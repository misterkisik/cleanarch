# Maintainer: MisterKisik

pkgname=cleanarch
pkgver=1.0.0
pkgrel=1
pkgdesc="Графическая утилита очистки кэшей pacman/yay, системных логов и обновления Arch Linux (GTK 4 / Libadwaita)"
arch=('any')
url="https://github.com/misterkisik/cleanarch"
license=('GPL-3.0-or-later')
depends=(
    'python'
    'python-gobject'
    'gtk4'
    'libadwaita'
)
makedepends=(
    'python-build'
    'python-installer'
    'python-wheel'
    'python-setuptools'
)
optdepends=(
    'yay: для очистки кэша AUR и обновления сторонних пакетов'
    'pacman-contrib: утилита paccache для умной очистки кэша pacman'
    'polkit: графический запрос пароля суперпользователя (pkexec)'
    'flatpak: для очистки и обновления Flatpak'
)
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl

    # Ярлык приложения
    install -Dm644 data/cleanarch.desktop "$pkgdir/usr/share/applications/cleanarch.desktop"

    # Иконка приложения (PNG и SVG)
    install -Dm644 data/cleanarch.png "$pkgdir/usr/share/icons/hicolor/512x512/apps/cleanarch.png"
    install -Dm644 data/cleanarch.png "$pkgdir/usr/share/pixmaps/cleanarch.png"
    install -Dm644 data/cleanarch.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/cleanarch.svg"

    # Изображение маскота-персонажа
    install -Dm644 data/mascot.png "$pkgdir/usr/share/cleanarch/mascot.png"
}

"""
Основное приложение Adw.Application для CleanArch.
"""

import sys
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio
from cleanarch import __app_id__
from cleanarch.window import CleanArchWindow

class CleanArchApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id=__app_id__,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = CleanArchWindow(application=self)
        self.window.present()

def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv
    app = CleanArchApplication()
    return app.run(argv)

if __name__ == "__main__":
    sys.exit(main())

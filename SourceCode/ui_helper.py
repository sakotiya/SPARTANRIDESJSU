from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer

def show_flash(dialog, text="Each ride costs $2.00", duration_ms=3000):
    """
    Pop up a non-modal banner in the top-centre of `dialog` for `duration_ms`ms.
    """
    flash = QLabel(text, dialog)
    flash.setStyleSheet("""
        background-color: #fffa8c;
        color: #333;
        border: 1px solid #aaa;
        padding: 4px;
        font-weight: bold;
    """)
    # center it at the top
    w = dialog.width()
    flash.adjustSize()
    flash.move((w - flash.width())//2, 10)
    flash.show()

    # auto-hide after duration
    QTimer.singleShot(duration_ms, flash.hide)

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QAction
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QGraphicsDropShadowEffect
)
import sys
import ast
import operator as op

# Operaciones validas jsakjsksj
OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def safe_eval(expr: str):
    s = (expr.replace("×", "*")
              .replace("÷", "/")
              .replace("−", "-")
              .replace("^", "**"))
    node = ast.parse(s, mode="eval").body

    def _ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.Num):
            return n.n
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](_ev(n.left), _ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in OPS:
            return OPS[type(n.op)](_ev(n.operand))
        raise ValueError("Expresión inválida")

    return _ev(node)

# LA PUTA CALCULADORA
BUTTONS = [
    ["AC", "⌫", "(", ")"],
    ["7",  "8",  "9",  "÷"],
    ["4",  "5",  "6",  "×"],
    ["1",  "2",  "3",  "−"],
    [".",  "0",  "%",  "+"],
]

class Calculadora(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora :)")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(380, 560)
        self.setMinimumSize(340, 480)

        self.expr = ""
        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # la raíz del putisimo layout
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)

        # Contenedor principal asaakaj
        self.card = QFrame()
        self.card.setObjectName("Card")
        self.card.setContentsMargins(0, 0, 0, 0)

        # Sombras jakjak
        shadow = QGraphicsDropShadowEffect(self.card)
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 14)
        shadow.setColor(Qt.black)
        self.card.setGraphicsEffect(shadow)

        card_v = QVBoxLayout(self.card)
        card_v.setContentsMargins(18, 18, 18, 18)
        card_v.setSpacing(12)

        # Expresion y resultado
        self.exprLabel = QLabel("")
        self.exprLabel.setObjectName("Expr")
        self.exprLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.resultEdit = QLineEdit("0")
        self.resultEdit.setObjectName("Result")
        self.resultEdit.setReadOnly(True)
        self.resultEdit.setAlignment(Qt.AlignRight)
        self.resultEdit.setCursorPosition(0)  # cursor al inicio

        card_v.addWidget(self.exprLabel)
        card_v.addWidget(self.resultEdit)

        # Cuadricula rechulona de botones
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        for r, row in enumerate(BUTTONS):
            for c, label in enumerate(row):
                btn = self._make_btn(label, cls=self._btn_style(label))
                grid.addWidget(btn, r, c)

        # Un igual bien grande sisisi
        equals = self._make_btn("=", cls="Accent")
        equals.setMinimumHeight(56)
        equals.clicked.connect(self.equals)
        card_v.addLayout(grid)
        card_v.addWidget(equals)

        root.addWidget(self.card)

        self._apply_style()

    def _apply_style(self):

        self.setStyleSheet("""
            QWidget {
                background: transparent;
                font-family: -apple-system, BlinkMacSystemFont, "SF Pro", "Segoe UI", Roboto, system-ui, sans-serif;
            }
            #Card {
                background: rgba(255,255,255,0.08); /* glass panel */
                border: 1px solid rgba(255,255,255,0.25);
                border-radius: 24px;
            }
            #Expr {
                color: rgba(255,255,255,0.75);
                font-size: 14px;
                padding: 6px 10px 2px 10px;
            }
            #Result {
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 14px;
                color: #ffffff;
                font-size: 28px;
                padding: 14px 16px;
                selection-background-color: rgba(255,255,255,0.18);
                selection-color: #fff;
            }
            QPushButton {
                background: rgba(255,255,255,0.10);
                border: 1px solid rgba(255,255,255,0.20);
                border-radius: 16px;
                color: #eef2ff;
                padding: 12px;
                font-size: 18px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.14);
            }
            QPushButton:pressed {
                background: rgba(255,255,255,0.18);
            }
            QPushButton[class="Op"] {
                color: #b7d1ff;
                background: rgba(255,255,255,0.08);
            }
            QPushButton[class="Warn"] {
                color: #ff9cc2;
                background: rgba(255,255,255,0.06);
            }
            QPushButton[class="Accent"] {
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(118,161,255,0.9),
                    stop:1 rgba(82,136,255,0.9));
                border: 1px solid rgba(255,255,255,0.35);
            }
        """)

       
        self._set_backdrop()

    def _set_backdrop(self):

        self.setAutoFillBackground(True)
        pal = self.palette()

        from PySide6.QtGui import QLinearGradient, QBrush, QColor
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor("#0f1116"))
        grad.setColorAt(1.0, QColor("#151925"))
        pal.setBrush(self.backgroundRole(), QBrush(grad))
        self.setPalette(pal)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._set_backdrop()

    # Botones
    def _btn_style(self, label: str) -> str:
        if label in ["÷", "×", "−", "+", "%", "(", ")"]:
            return "Op"
        if label in ["AC", "⌫"]:
            return "Warn"
        return ""  # Defecto o yo que sé
    def _make_btn(self, text: str, cls: str = "") -> QPushButton:
        b = QPushButton(text)
        if cls:
            b.setProperty("class", cls)
        b.setMinimumSize(QSize(64, 48))
        b.clicked.connect(lambda: self.on_button(text))
        return b

    def on_button(self, label: str):
        if label == "AC":
            self.expr = ""
            self.exprLabel.setText("")
            self.resultEdit.setText("0")
            return
        if label == "⌫":
            self.expr = self.expr[:-1]
            self.exprLabel.setText(self.expr)
            return
        if label == "%":
            
            tail = self._last_number(self.expr)
            if tail is not None and tail != "":
                try:
                    v = float(tail) / 100.0
                    self.expr = self.expr[:-len(tail)] + str(v)
                except:
                    pass
            self.exprLabel.setText(self.expr)
            return
        if label == "=":
            self.equals()
            return
      
        self.expr += label
        self.exprLabel.setText(self.expr)

    def _last_number(self, s: str):
        if not s: return ""
        i = len(s) - 1
        digits = "0123456789."
        while i >= 0 and s[i] in digits:
            i -= 1
        return s[i+1:]

    def equals(self):
        s = self.expr.strip()
        if not s:
            self.resultEdit.setText("0")
            return
        try:
            val = safe_eval(s)
            if isinstance(val, float) and val.is_integer():
                val = int(val)
            self.resultEdit.setText(str(val))
        except Exception:
            self.resultEdit.setText("Error")

    # TECLADO
    def _bind_keys(self):
        self.resultEdit.installEventFilter(self)
        self.grabKeyboard()

    def keyPressEvent(self, e):
        k = e.key()
        ch = e.text()
        if k in (Qt.Key_Return, Qt.Key_Enter):
            self.equals(); return
        if k == Qt.Key_Escape:
            self.expr = ""; self.exprLabel.setText(""); self.resultEdit.setText("0"); return
        if k == Qt.Key_Backspace:
            self.on_button("⌫"); return

        allowed = "0123456789.+-*/()%^"
        if ch in allowed:
            pretty = ch
            if ch == "*": pretty = "×"
            if ch == "/": pretty = "÷"
            if ch == "-": pretty = "−"
            self.expr += pretty
            self.exprLabel.setText(self.expr)

        e.accept()

def main():
    app = QApplication(sys.argv)

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    w = Calculadora()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

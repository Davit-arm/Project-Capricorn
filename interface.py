import sys
import os
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout,QHBoxLayout, QWidget,QLabel,QPlainTextEdit,QScrollArea,QFrame
from PySide6.QtCore import Qt,QPoint,Signal, QEvent
from PySide6.QtGui import QPainter, QPolygon, QColor, QPen, QFontDatabase, QPixmap
from logic import generate_response



class TitleBar(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        main_layout = QVBoxLayout(self)
        main_layout.setObjectName("titleBar")
        title_layout = QHBoxLayout()
        title_layout.setSpacing(0)
        title_layout.setContentsMargins(0,0,0,0)
        logo = QLabel("<span style='font-size:15px; color:cyan'>▌</span> CAPRI")
        logo.setObjectName("logo")
        status = QLabel("  •  ONLINE")
        status.setObjectName("status")
        close_button = QPushButton("x")
        close_button.setFixedSize(40,30)
        close_button.clicked.connect(self.main_window.close)
        close_button.setObjectName("closeButton")
        minimize_button = QPushButton("-")
        minimize_button.clicked.connect(self.main_window.showMinimized)
        minimize_button.setFixedSize(40,30)
        minimize_button.setObjectName("minButton")
        line = QFrame()
        line.setFixedHeight(3)
        line.setStyleSheet("background-color:cyan;")
        title_layout.addWidget(logo)
        title_layout.addStretch()
        title_layout.addWidget(status)
        title_layout.addWidget(minimize_button)
        title_layout.addWidget(close_button)
        main_layout.addLayout(title_layout)
        main_layout.addWidget(line)
        self.setStyleSheet("""

        #titleBar {
            background-color:blue;    
        }

        QLabel#logo {
            color: #f5f7ff;
            font-size:15px;
            font-weight:bold;
            font-family: 'Orbitron';
            background:transparent;
        }

        #status {
            padding-left:10px;
            background:transparent;
        }

        #closeButton, #minButton {
            border:none;
            background-color: rgba(0, 0, 0, 1%);
            font-size:15px;
            min-height:30px;
            min-width:30px;
            font-weight:bold;

        }

        #minButton {
            font-size:30px;
        }

        #closeButton:hover {
            color:red;
        }

        #minButton:hover {
            color:cyan;
            }

""")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.main_window.windowHandle().startSystemMove()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0,0,0,5))

class RPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.panel_layout = QVBoxLayout(self)
        self.panel_layout.setSpacing(0)
        self.user_prompt = QLabel('YOU: something')
        self.user_prompt.setObjectName('userPrompt')
        title = QLabel('<span style="color:#ff477e; font-size:14px;">Capri    </span>   / ')
        title.setObjectName('title')
        self.response = QLabel('Dont her me buddy,just call me Capri')
        self.response.setObjectName('resp')
        self.response.setMinimumHeight(50)
        self.response.setMaximumHeight(100)
        self.response.setWordWrap(True)
        scroll = QScrollArea()
        scroll.setObjectName('Scroll')
        scroll.setWidget(self.response)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.panel_layout.addWidget(self.user_prompt)
        self.panel_layout.addWidget(title)
        self.panel_layout.addWidget(scroll)
        self.panel_layout.addStretch()
        self.setStyleSheet('''



        QLabel#userPrompt {
            font-size:10px;
            color:grey;
            font-weight:bold;
            font-family: 'Orbitron';
            background:transparent;
            padding-bottom:2px;
            padding-left:3px;
        }

        QLabel#title {
            font-size:14px;
            color:cyan;
            font-family:  'Orbitron';
            font-weight:bold;
            padding-bottom:5px;
            background:transparent;
        }

        #Scroll {
            background:transparent;
            border:none;
        }

        #Scroll QScrollBar:vertical{
            background:transparent;
            width:3px;
            margin:0;
        }

        #Scroll QScrollBar::handle:vertical {
            background:cyan;
            border-radius:4px;
            min-height:10px;
        }

        #Scroll QScrollBar::add-page:vertical, #Scroll QScrollBar::sub-page:vertical {
            height:0;
            background:transparent;
        }

        #Scroll QScrollBar::add-line:vertical, #Scroll QScrollBar::sub-line:vertical {
            background:transparent;
        }

        QLabel#resp {

            font-size:16px;
            color:white;
            font-family:  'Orbitron';
            font-weight:bold;
            background:transparent;
            qproperty-alignment: 'AlignTop | AlignLeft';
        }
''')
    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        points = QPolygon([
            QPoint(15,0),
            QPoint(self.width(),0),
            QPoint(self.width(),self.height()-17),
            QPoint(self.width()-17,self.height()),
            QPoint(0,self.height()),
            QPoint(0,15)
        ])
        painter.setBrush(QColor(10, 14, 20, 230))
        pen=QPen(QColor('cyan'),2)
        painter.setPen(pen)
        painter.drawPolygon(points)


class IPanel(QWidget):
    message_sent = Signal(str)
    def __init__(self):
        super().__init__()
        self.panel_layout = QHBoxLayout(self)
        self.panel_layout.setSpacing(0)
        line = QLabel('▌')
        line.setObjectName('line')
        self.user_input = QPlainTextEdit()
        self.user_input.setPlaceholderText("ask Capri something...")
        self.user_input.setObjectName('input')
        self.user_input.setMinimumHeight(50)
        self.user_input.installEventFilter(self)
        send_button = QPushButton('↵')
        send_button.clicked.connect(self.send_message)
        mic_button = QPushButton('\U0001F3A4\uFE0E')
        self.panel_layout.addWidget(line, alignment=Qt.AlignmentFlag.AlignTop)
        self.panel_layout.addWidget(self.user_input)
        self.panel_layout.addWidget(send_button)
        self.panel_layout.addWidget(mic_button)
        self.setStyleSheet('''
        IPanel {
            max-height:65px;
        }

        #line {
            color:red;
            padding-right:10px;
            padding-top:14px;
            background:transparent;
        }
        #input {
            font-family:'Orbitron';
            font-size:11px;
            font-weight:bold;
            border:none;
            padding:12px;
            color:white;
            background:transparent
        }

        #input QScrollBar:vertical {
            background:transparent;
            width:5px;
            margin:0;
        }

        #input QScrollBar::handle:vertical {
            background:cyan;
            border-radius:2px;
            min-height:20px;
        }

        #input QScrollBar::add-line:vertical,
        #input QScrollBar::sub-line:vertical {
            height:0;
        }

        #input QScrollBar::add-page:vertical,
        #input QScrollBar::sub-page:vertocal{
            background:transparent;
        }

        QPushButton {
            font-size:15px;
            border:none;
            width:20px;
            height:20px;
            padding:10px;
            background:transparent;
            font-weight:bold;
        }

        QPushButton:hover {
            background-color:#24404a
        }
        
    
''')
    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        points = QPolygon([
            QPoint(self.width() - 15, 0),
            QPoint(0, 0), 
            QPoint(0, self.height() - 15), 
            QPoint(15,self.height()), 
            QPoint(self.width(),self.height()),
            QPoint(self.width(), 16),
        ])
        painter.setBrush(QColor(10, 14, 20, 230))
        pen=QPen(QColor('cyan'),2)
        painter.setPen(pen)
        painter.drawPolygon(points)

    def eventFilter(self, obj, event):
        if obj == self.user_input and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                self.send_message()
                return True
        return super().eventFilter(obj, event)

    def send_message(self):
        user_input = self.user_input.toPlainText().strip()
        self.message_sent.emit(user_input)
        self.user_input.clear()

class CapriInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capri Interface")
        self.resize(400, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10,10,10,10)
        main_layout.setSpacing(30)


        title_bar = TitleBar(self)
        main_layout.addWidget(title_bar)

        response_block = QVBoxLayout()
        response_block.setSpacing(10)
        main_layout.addLayout(response_block)

        self.response_panel = RPanel()
        self.response_panel.setMinimumHeight(100)
        self.response_panel.setMaximumHeight(300)
        response_block.addWidget(self.response_panel,stretch=1)

        capri = QLabel()
        pixmap = QPixmap('imgs/idle.png').scaled(400,700,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        capri.setPixmap(pixmap)
        capri.setAlignment(Qt.AlignmentFlag.AlignCenter)
        capri.setMaximumHeight(400)
        capri.setMinimumHeight(200)
        capri.setStyleSheet("""
        background-color: #101722;
        border:2px solid #ff477e;
        """)
        main_layout.addWidget(capri)

        # input_panel = QHBoxLayout()
        # self.input_field = QLineEdit()
        # self.input_field.setPlaceholderText("ask Capri something...")
        # #enter part
        # send_button = QPushButton("Send")
        # #click part
        # mic_button = QPushButton("Mic")
        # #click part
        # input_panel.addWidget(self.input_field, stretch=1)
        # input_panel.addWidget(send_button)
        # input_panel.addWidget(mic_button)
        # main_layout.addLayout(input_panel)

        self.input_panel = IPanel()
        self.input_panel.message_sent.connect(self.process_user_input)
        main_layout.addWidget(self.input_panel)
    

        self.setStyleSheet("""
        QWidget {
            background-color: #0b1019;
            color: #e8faff;
            font-family: Segoe UI;
            font-size: 14px;
        }
        QFrame#Rpanel {
            background-color: #111a25;
            border: 2px solid #43e8df;
            border-radius: 10px;
        }

        QLabel#logo {
            color: #f5f7ff;
            font-size:20px;
            font-weight:bold;
        } 
        QLabel#status {
            color:#ff477e;
            font-weight:bold;
        }
        QLineEdit {
            background-color:#151e2a;
            border: 1px solid #43e8df;
            border-radius:6px;
            padding:12px;
            color:white;
        }
        

        """)

    def process_user_input(self, message):
        self.response_panel.user_prompt.setText(f'YOU: {message}')
        QApplication.processEvents()
        response = generate_response(message)
        self.response_panel.response.setText(response)


# QPushButton {
#             background-color: #172633;
#             border: 1px solid #43e8df;
#             padding: 10px 16px;
#             color:white;
#         }

#         QPushButton:hover{
#             background-color:#24404a;
#         }


app = QApplication(sys.argv)
font_path = os.path.join(os.path.dirname(__file__),'fonts','Orbitron-VariableFont_wght.ttf')
font_id = QFontDatabase.addApplicationFont(font_path)
window = CapriInterface()
window.show()
sys.exit(app.exec())
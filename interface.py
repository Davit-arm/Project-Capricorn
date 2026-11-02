import sys
import os
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout,QHBoxLayout, QWidget,QLabel,QPlainTextEdit,QScrollArea,QFrame
from PySide6.QtCore import Qt,QPoint,Signal, QEvent
from PySide6.QtGui import QPainter, QPolygon, QColor, QPen, QFontDatabase, QPixmap
import threading
from logic import Brain


class IPanel(QWidget):
    message_sent = Signal(str)
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint)
        
        self.panel_layout = QHBoxLayout(self)
        self.panel_layout.setSpacing(0)
        line = QLabel('▌')
        line.setObjectName('line')
        self.user_input = QPlainTextEdit()
        self.user_input.setPlaceholderText("ask Capri something...")
        self.user_input.setObjectName('input')
        self.user_input.setMinimumHeight(50)
        self.setMaximumWidth(365)
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
        #input QScrollBar::sub-page:vertical{
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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.windowHandle().startSystemMove()





class TitleBar(QWidget):
    def __init__(self,main_window,input_panel):
        super().__init__()
        self.input_panel = input_panel
        self.main_window = main_window
        main_layout = QVBoxLayout(self)
        self.setObjectName("titleBar")
        title_layout = QHBoxLayout()
        title_layout.setSpacing(0)
        title_layout.setContentsMargins(0,0,0,0)
        logo = QLabel("<span style='font-size:15px; color:cyan'>▌</span> CAPRI")
        logo.setObjectName("logo")
        input_button = QPushButton('💬')
        input_button.setObjectName('InputToggle')
        input_button.setCheckable(True)
        self.input_button_on = False
        input_button.clicked.connect(self.open_input_panel)
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
        title_layout.addWidget(input_button)
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

        #closeButton, #minButton, #InputToggle {
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

        #InputToggle {
        
        }

        #InputToggle:hover {
            background-color:#ff477e
        }

        #InputToggle:checked {
            background-color:cyan;
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

    def open_input_panel(self):
        if self.input_panel.isVisible():
            self.input_panel.hide()
        else:
            self.input_panel.move(self.main_window.mapToGlobal(QPoint(5,self.main_window.height()+10)))
            self.input_panel.show()

class RPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.panel_layout = QVBoxLayout(self)
        self.panel_layout.setSpacing(0)
        self.user_prompt = QLabel('YOU: something')
        self.user_prompt.setObjectName('userPrompt')
        title = QLabel('<span style="color:#ff477e; font-size:14px;">Capri    </span>   / ')
        title.setObjectName('title')
        self.response = QLabel('Dont her me buddy, just call me Capri')
        self.response.setObjectName('resp')
        # self.response.setMinimumHeight(50)
        # self.response.setMaximumHeight(100)
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





# class IBlock(QWidget):
#     message_sent = Signal(str)
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout(self)
#         close_button = QPushButton("x")
#         close_button.setObjectName("closeButton")
#         layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)
#         close_button.clicked.connect(self.close)
#         self.input_panel = IPanel()
#         self.input_panel.message_sent.connect(self.message_sent)
#         layout.addWidget(self.input_panel)
#         self.setStyleSheet('''
#         #closeButton {
#             border:none;
#             background-color: rgba(0, 0, 0, 1%);
#             font-size:15px;
#             min-height:30px;
#             min-width:30px;
#             font-weight:bold;
#         }
# ''')

#     def mousePressEvent(self, event):
#         if event.button() == Qt.MouseButton.LeftButton:
#             self.window().windowHandle().startSystemMove()

    


class CapriInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capri Interface")
        self.resize(300, 400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10,10,10,10)
        main_layout.setSpacing(30)
        self.ai = Brain()
        self.busy = False
        self.ai.status.connect(self.change_expression)
        self.ai.response.connect(self.display_response)
        self.expressions = {
            'open_app':'imgs/looking.png',
            'search_web':'imgs/searching.png',
            'idle':'imgs/idle.png'
        }

        

        response_block = QVBoxLayout()
        response_block.setSpacing(10)
        

        self.response_panel = RPanel()
        self.response_panel.setMinimumHeight(100)
        self.response_panel.setMaximumHeight(300)


        self.capri = QLabel()
        self.pixmap = QPixmap('imgs/idle.png').scaled(350,700,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.capri.setPixmap(self.pixmap)
        self.capri.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.capri.setMaximumHeight(300)
        self.capri.setMinimumHeight(200)
        self.capri.setStyleSheet("""
        background-color: #101722;
        border:2px solid #ff477e;
        """)


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
        title_bar = TitleBar(self,self.input_panel)
        self.input_panel.message_sent.connect(self.process_user_input)
        # main_layout.addWidget(self.input_panel)

        main_layout.addWidget(title_bar)
        response_block.addWidget(self.response_panel) #stretch=1
        main_layout.addLayout(response_block)
        main_layout.addWidget(self.capri)

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

    def change_expression(self,status):
        if status not in self.expressions:
            return
        self.pixmap = QPixmap(self.expressions[status]).scaled(400,700,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.capri.setPixmap(self.pixmap)


    def display_response(self,response):
        self.response_panel.response.setText(response)
        self.busy = False

    def process_user_input(self, message):
        if self.busy:
            return
        self.busy = True
        self.response_panel.user_prompt.setText(f'YOU: {message}')
        threading.Thread(target=self.ai.generate_response,args=(message,), daemon=True).start()
        
        
        # self.response_panel.response.setText(response)


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
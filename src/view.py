from PySide6.QtWidgets import (
    QWidget, QSystemTrayIcon, QMenu, QLabel, QTextEdit,
    QTableWidgetItem, QVBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QMessageBox
)
from PySide6.QtGui import (
    QIcon, QAction, 
    QMouseEvent, QCursor, 
    QFont, QClipboard
)
from PySide6.QtCore import Qt, Signal, QSize, QPoint, QRect, QEvent, QTimer, Slot
from src.form_ui import Ui_Widget
from src.settings import Settings, SetUI
from typing import List
import keyboard


# Preset Widget attrubutes
MARGIN = 8
MIN_WIDTH = 350
MIN_HEIGHT = 400
DRAGGING_AREA_HEIGHT = 40


class TrayIcon(QSystemTrayIcon):
    def __init__(self, icon, quit_action):
        super().__init__(icon)
        
        self.setToolTip("Press Ctrl+Alt+Q to show/hide widget.")
        
        self.menu = QMenu()
        self.quit_action = QAction("Quit", self.menu)
        self.quit_action.triggered.connect(quit_action)
        self.menu.addAction(self.quit_action)
        self.setContextMenu(self.menu)
        

class MessageComponent(QLabel):
    edited_msg = Signal(str)
    copied = Signal()
    def __init__(self, role: str, content: str, id: int):
        super(MessageComponent, self).__init__()  
        self.role = role
        self.content = content
        self.id = id
        self.setup_ui()
        self.msg_editor = None
        self.clipboard = QClipboard()
        
    def setup_ui(self):
        # Set message component attributes
        self.setTextFormat(Qt.TextFormat.MarkdownText)
        self.setWordWrap(True)
        self.setText(self.content)
        self.setMinimumWidth(80)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.setOpenExternalLinks(True)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
        
        if self.role == "user":
            self.load_stylesheet("user_message.qss")
        else:
            self.load_stylesheet("assistant_message.qss")
        self.set_font(self)

    def set_font(self, object):
        # Set font
        font = object.font()
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        font.setWeight(QFont.Weight(540))
        font.setPointSize(11)
        object.setFont(font)
        
    def mouseDoubleClickEvent(self, event):
        # Double click to edit
        # Convert to line edit
        self.enable_edit()
        
    def enable_edit(self):
        if self.msg_editor is None:
            self.msg_editor = QTextEdit(self)
            self.set_font(self.msg_editor)
            self.msg_editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.msg_editor.setObjectName("editor")
            self.msg_editor.setFixedSize(self.size())
            self.msg_editor.setPlainText(self.content)
            self.msg_editor.focusOutEvent = self.submit_edit
            self.msg_editor.selectAll()
            self.msg_editor.setFocus()
            self.msg_editor.show()
            self.pre_size_policy = self.sizePolicy()
            self.setFixedSize(self.size())
            self.setText("")

    def submit_edit(self, event = None):
        self.content = self.msg_editor.toPlainText()
        self.setText(self.content)
        self.msg_editor.hide()
        self.msg_editor.deleteLater()
        self.msg_editor = None
        self.setMaximumSize(999999, 999999)
        self.setMinimumSize(5, 5)
        self.setSizePolicy(self.pre_size_policy)
        self.edited_msg.emit(self.text())
        
                
    def load_stylesheet(self, style_sheet: str):
        # Load stylesheet
        with open("styles/"+ style_sheet, 'r') as qss:
            style_sheet = qss.read()
        self.setStyleSheet(style_sheet)

    def append_word(self, word: str):
        self.content += word
        self.setText(self.content)
        
    # def append_copy_btn(self):
    #     self.cpy_btn = QPushButton(self)
    #     self.cpy_btn.setText("Copy")
    #     self.cpy_btn.clicked.connect(lambda: self.clipboard.setText(self.content))
    #     self.cpy_btn.setFixedSize(40, 40)
    #     self.spacer = QSpacerItem(0,0, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
    #     self.layout = QVBoxLayout(self)
    #     self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
    #     self.layout.addSpacerItem(self.spacer)
    #     self.layout.addWidget(self.cpy_btn)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clipboard.setText(self.content)
        self.copied.emit()
        
class ChatView(QWidget):
    # Signals(message_sent, query_session_id), 
    # -1    new session; 
    # 0     continue current session; 
    # 1+    query session id 
    msg_submit = Signal(str, int) 
    switch_session = Signal(int)
    save_settings = Signal()

    def __init__(self):
        super().__init__()
        
        
        # Variables
        self.components: List[MessageComponent] = []  # Components added in message area
        self.auto_scroll = True
        self.title = "Chat"
        self.settings = Settings()
        
        # UI init
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setup_ui()

        # Events init
        self.setup_window_events()

        # Connect signals and slots
        self.ui.set_btn.clicked.connect(self.show_settings)
        self.ui.submit_btn.clicked.connect(self.submit_message)
        self.ui.full_screen_btn.clicked.connect(self.toggle_maximize)
        self.ui.clear_btn.clicked.connect(self.new_session)
        self.ui.quit_btn.clicked.connect(self.hide)
        self.tray.activated.connect(self.toggle_visibility)
        self.ui.chat_display.verticalScrollBar().valueChanged.connect(self.update_auto_scroll)
        self.ui.tableWidget.cellClicked.connect(self.table_cell_clicked) 
        
        
    def setup_ui(self):

        # Overall form
        self.load_stylesheet()
        self.ui.title_label.setText(self.title)
        self.tray = TrayIcon(QIcon("pics/icon.ico"), self.close)
        self.tray.show()
        self.set_icons()
        self.set_window_flags()
        self.setGeometry(self.settings.get_geometry())
        
        # Message area
        self.void_widget = QWidget()
        self.void_widget.setStyleSheet("background-color: transparent;")
        self.chat_display_layout = QVBoxLayout(self.void_widget)
        self.chat_display_layout.setSpacing(6)
        self.chat_display_layout.setContentsMargins(0, 0, 6, 0)
        self.chat_display_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ui.chat_display.setWidget(self.void_widget)
        
        # Table style
        self.update_table_style()
        
        # Splitter
        self.ui.display_splitter.setSizes([self.width() - 100, 100])
        self.ui.body_splitter.setSizes([100, self.height() - 100])
        
    @Slot()
    def table_cell_clicked(self, row, column):
        session_id = int(self.ui.tableWidget.item(row, column).text()[:3])
        self.switch_session.emit(session_id)
        
    def toggle_input(self, action = True):
        self.ui.input_text.setEnabled(action)
        self.ui.submit_btn.setEnabled(action)
        self.ui.input_text.setFocus()
        
    def show_settings(self):
        self.toggle_input(False)
        self.setUi = SetUI(self)
        self.setUi.show()
        self.setUi.api_key.textChanged.connect(lambda: self.settings.set_api_key(self.setUi.api_key.text()))
        self.setUi.base_url.textChanged.connect(lambda: self.settings.set_base_url(self.setUi.base_url.text()))
        self.setUi.model.textChanged.connect(lambda: self.settings.set_model(self.setUi.model.text()))
        self.setUi.system_prompt.textChanged.connect(lambda: self.settings.set_system_prompt(self.setUi.system_prompt.text()))
        self.setUi.temperature.valueChanged.connect(lambda: self.settings.set_temperature(self.setUi.temperature.value()/10))
        self.setUi.close_btn.clicked.connect(self.save_settings.emit)    
        self.setUi.close_btn.clicked.connect(self.ui.clear_btn.click)    
        self.setUi.close_btn.clicked.connect(lambda: self.toggle_input(True))
        
    def update_table_style(self):
        table_width = self.ui.tableWidget.width()
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(table_width)

    def load_stylesheet(self, style_sheet: str = "form_styles.qss"):
        with open("styles/"+style_sheet, 'r') as qss:
            style_sheet = qss.read()
        self.setStyleSheet(style_sheet)

    def set_icons(self):
        # In-app Icons
        self.ui.clear_btn.setIcon(QIcon("pics/clear.svg"))
        self.ui.submit_btn.setIcon(QIcon("pics/submit.svg"))
        self.ui.submit_btn.setIconSize(QSize(20, 20))
        self.ui.quit_btn.setIcon(QIcon("pics/close.svg"))
        self.ui.full_screen_btn.setIcon(QIcon("pics/full.svg"))
        self.ui.set_btn.setIcon(QIcon("pics/settings.svg"))
        # Window Icon
        self.setWindowIcon(QIcon("pics/icon.ico"))

    def set_window_flags(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def setup_window_events(self):
        self.ui.input_text.setFocus()
        self.ui.parent_box.setMouseTracking(True)       # Enable recieving mouse position even if mouse's not pressed
        self.mouse_drag = mouseDrag()
        self.ui.parent_box.mousePressEvent = self.ui_mouse_press_event
        self.ui.parent_box.mouseMoveEvent = self.ui_mouse_move_event
        self.ui.parent_box.mouseReleaseEvent = self.ui_mouse_release_event
        self.ui.parent_box.mouseDoubleClickEvent = self.ui_mouse_double_click_event

    @Slot()
    def clear_screen(self):
        # Clear all messages in the message area
        for component in self.components:
            self.chat_display_layout.removeWidget(component)
            component.deleteLater()
        self.components.clear()
        
    @Slot()
    def new_session(self):
        self.clear_screen()
        # New session
        self.msg_submit.emit("", -1)
        self.ui.input_text.setFocus()
        self.ui.input_text.selectAll()

    @Slot()
    def enter_pressed(self):
        if self.ui.input_text.hasFocus():
            self.submit_message()
        else:
            self.ui.input_text.setFocus()
            self.ui.input_text.selectAll()

    def self_has_focus(self, widget: QWidget = None):
        if not widget:
            widget = self
        # Recursively check
        try:
            if widget.hasFocus():
                return True
        except:
            return False
        
        if widget.children() == []:
            return False
        for child in widget.children():
            if self.self_has_focus(child):
                return True
        return False
            
    @Slot()
    def submit_message(self, query_session = 0):
        # Check if the input is empty
        if self.ui.input_text.toPlainText().strip(" \n") == "":
            self.ui.input_text.setFocus()
            return
        # Send input to controller
        content = self.ui.input_text.toPlainText()
        self.msg_submit.emit(content, query_session)
        self.ui.input_text.clear()

    # Auto-scroll to bottom
    @Slot()
    def update_auto_scroll(self):
        # Get current vertical position and maximum position
        vertical_position = self.ui.chat_display.verticalScrollBar().value()
        max_position = self.ui.chat_display.verticalScrollBar().maximum()

        # Check if the widget is scrolled to the bottom
        if vertical_position >= max_position - 150:
            self.auto_scroll = True
        else:
            self.auto_scroll = False

    def append_word(self, word: str):
        '''
        Append a word to the last message.
        '''
        try:
            last_msg: MessageComponent = self.components[-1]
            last_msg.append_word(word)
        except IndexError:
            print("No message to append word to.")
            return
        if self.auto_scroll:
            self.scroll_to_bottom()

    def append_msg(self, role: str, content: str, id: int):
        '''
        Create a new message component.
        And append it to the message area.
        '''
        # Prevent redundently adding messages. 
        for msg in self.components:
            if msg.id == id:
                return
        # Create a new message component
        msg_component = MessageComponent(role, content, id)
        msg_component.copied.connect(self.show_copied_msg)
        self.components.append(msg_component)
        self.chat_display_layout.addWidget(msg_component)
        self.scroll_to_bottom()
    
    def show_copied_msg(self):
        self.ui.title_label.setText("""<div style="font-siz:18px;">COPIED!</div>""")
        QTimer.singleShot(600, lambda: self.ui.title_label.setText(self.title))
    
    def scroll_to_bottom(self):
        QTimer.singleShot(
            10,
            lambda: self.ui.chat_display.verticalScrollBar().setValue(self.ui.chat_display.verticalScrollBar().maximum())
        )
    
    @Slot()
    def toggle_visibility(self, reason=0):
        if reason == 0 or reason != QSystemTrayIcon.ActivationReason.Context:
            self.ui.input_text.setEnabled(False)
            if not self.isHidden():
                self.hide()
            else:
                self.ui.input_text.setEnabled(True)
                self.show()
                self.activateWindow()
                self.ui.input_text.setFocus()

    @Slot()
    def toggle_maximize(self):
        if Qt.WindowState.WindowMaximized != self.windowState():
            self.setWindowState(Qt.WindowState.WindowMaximized)
            self.ui.parent_box.setProperty("border-radius", 0)
            self.setProperty("border-radius", "0px")

        else:
            self.setWindowState(Qt.WindowState.WindowNoState)

    def ui_mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:  
            self.mouse_drag.update(self.frameGeometry(), event.globalPos())
    
    def ui_mouse_move_event(self, event):
        if not self.windowState() == Qt.WindowState.WindowMaximized and not self.mouse_drag.is_resizing:
            self.update_cursor()
        # Custom window dragging and resizing
        if self.mouse_drag.is_resizing and not self.windowState() == Qt.WindowState.WindowMaximized:
            # The user is resizing the widget
            self.settings.set_geometry(self.geometry())
            diff: QPoint = event.globalPos() - self.mouse_drag.pre_cur_loc
            self.resize_window(diff)            
        elif self.mouse_drag.dragging_area:
            # The user is dragging Widget
            
            # Quit Maximize window
            if Qt.WindowState.WindowMaximized == self.windowState():
                self.setWindowState(Qt.WindowState.WindowNoState)
                self.move(event.globalPos().x()-self.width()/2, event.globalPos().y()-MARGIN*2)
                # Need simulate one pressing since the widget pos changes
                mouse_press_event = QMouseEvent(QEvent.Type.MouseButtonPress, event.pos(), event.globalPos(), Qt.MouseButton.LeftButton, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
                self.ui.parent_box.mousePressEvent(mouse_press_event)
                # Enable border radius
                self.load_stylesheet("form_styles.qss")
            
            # Move the widget
            diff: QPoint = event.globalPos() - self.mouse_drag.pre_cur_loc
            destin: QPoint = self.mouse_drag.pre_frame.topLeft() + diff
            self.move(destin) 

    def ui_mouse_double_click_event(self, event):
        self.toggle_maximize()

    def ui_mouse_release_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_drag.reset_all()

    def resize_window(self, diff):
        def adjust_geometry(diff_x, diff_y):
            # Calculate adjusted geometry based on diff_x and diff_y
            new_geometry = self.mouse_drag.pre_frame.adjusted(
                diff_x if self.mouse_drag.dragging_left else 0,
                diff_y if self.mouse_drag.dragging_top else 0,
                diff.x() if self.mouse_drag.dragging_right else 0,
                diff.y() if self.mouse_drag.dragging_bottom else 0
            )

            # Enforce minimum size constraints
            new_width = max(new_geometry.width(), MIN_WIDTH)
            new_height = max(new_geometry.height(), MIN_HEIGHT)

            # Adjust geometry to maintain the position of right/bottom edges
            if new_geometry.width() != new_width:
                new_geometry.setLeft(new_geometry.right() - new_width) if self.mouse_drag.dragging_left else new_geometry.setRight(new_geometry.left() + new_width)
            if new_geometry.height() != new_height:
                new_geometry.setTop(new_geometry.bottom() - new_height) if self.mouse_drag.dragging_top else new_geometry.setBottom(new_geometry.top() + new_height)

            self.setGeometry(new_geometry)

        # Determine the diffs for x and y based on the dragging edges
        diff_x = diff.x() if self.mouse_drag.dragging_left else 0
        diff_y = diff.y() if self.mouse_drag.dragging_top else 0

        adjust_geometry(diff_x, diff_y)

    def update_cursor(self):
        cur_loc = QCursor.pos()
        
        if not self.frameGeometry().contains(cur_loc):
            self.setCursor(Qt.CursorShape.ArrowCursor)
            return
        
        m = self.mouse_drag.margin
        f = self.frameGeometry().adjusted
        tp = (not f(0, m, 0, 0).contains(cur_loc))
        lt = (not f(m, 0, 0, 0).contains(cur_loc))
        bt = (not f(0, 0, 0, -m).contains(cur_loc))
        rt = (not f(0, 0, -m, 0).contains(cur_loc))


        if (tp and lt) or (bt and rt):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif (tp and rt) or (bt and lt):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif tp or bt:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif lt or rt:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def update_session_table(self, sessions: List[List]):
        """Fill the table with sessions.
            sessions (List[int, str]): sessions: [[session_id, title], ...]
        """
        table = self.ui.tableWidget
        table.setRowCount(len(sessions))
        for s in range(len(sessions)):
            item = QTableWidgetItem(str(sessions[s][0]).zfill(3) + " " +sessions[s][1])
            self.ui.tableWidget.setItem(s, 0, item)
        
    def paintEvent(self, event):
        if not self.windowState() == Qt.WindowState.WindowMaximized and not self.mouse_drag.is_resizing:
            self.update_cursor()
        self.update_table_style()
        
    def close(self) -> bool:
        '''
        quit widget
        '''
        if self.isHidden():
            self.show()
        return super().close()


class mouseDrag:
    """Record the dragging status of the widget.
    """
    def __init__(self) -> None:
        self.margin = MARGIN
        self.dragging_left = False
        self.dragging_right = False
        self.dragging_top = False
        self.dragging_bottom = False
        self.dragging_area = False
        self.is_resizing = False

        self.pre_frame = QRect()
        self.pre_cur_loc = QPoint()
        
    def update(self, frame: QRect, cur_loc: QPoint):
        self.pre_frame = frame
        self.pre_cur_loc = cur_loc

        m = self.margin
        f = frame.adjusted
        self.dragging_top = (not f(0, m, 0, 0).contains(cur_loc))
        self.dragging_left = (not f(m, 0, 0, 0).contains(cur_loc))
        self.dragging_bottom = (not f(0, 0, 0, -m).contains(cur_loc))
        self.dragging_right = (not f(0, 0, -m, 0).contains(cur_loc))
        self.dragging_area = (not f(0, DRAGGING_AREA_HEIGHT, 0, 0).contains(cur_loc))

        self.is_resizing = self.dragging_top | self.dragging_bottom | self.dragging_left | self.dragging_right
        
    
    def reset_all(self):
        self.__init__()


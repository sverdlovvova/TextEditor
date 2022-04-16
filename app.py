from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *

import sys
import webbrowser

class FindWindow(QMainWindow):
    def __init__(self, parent, replace = False):
        super().__init__()
        self.setWindowTitle("Find Text")


        self.replace = replace
        self.label = QLabel()
        self.EditWindow = parent

        self.label_find = QLabel()
        self.label_find.setText("Find word:")

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        if replace:
            self.label_replace = QLabel()
            self.label_replace.setText("Replace to:")
            self.input_replace = QLineEdit()
            self.input_replace.textChanged.connect(self.label.setText)

        if not replace:
            button = QPushButton("Find next")
        else:
            button = QPushButton("Replace next")
        button.clicked.connect(self.next_button_clicked)
   
        layout = QVBoxLayout()
        layout.addWidget(self.label_find)
        layout.addWidget(self.input)
        if replace:
            layout.addWidget(self.label_replace)
            layout.addWidget(self.input_replace)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


    def next_button_clicked(self):
        text = self.EditWindow.textEdit.toPlainText()
        find_word = self.input.text()
        if self.replace:
            replace_word = self.input_replace.text()
        begin = self.EditWindow.get_cursor_index()
        for i in range(begin, len(text) - len(find_word) + 1):
            subtext = text[i:i+len(find_word)]
            if subtext == find_word:
                if not self.replace:
                    self.EditWindow.set_cursor(i + len(find_word))
                else:            
                    text = text[:i] + replace_word + text[i+len(find_word):]
                    self.EditWindow.textEdit.setPlainText(text)
                    self.EditWindow.set_cursor(i + len(replace_word))
                break
        begin = self.EditWindow.get_cursor_index()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text editor")
        self.resize(500, 500)
       
        filename = sys.argv[1]
        input_file = open(filename, 'r')

        self.textEdit = QTextEdit()
        self.textEdit.setPlainText(input_file.read())

        input_file.close()
            
        self._createActions()
        self._createMenuBar()

        self.hotkey_save = QShortcut(QKeySequence('Ctrl+S'), self)
        self.hotkey_save.activated.connect(self.save_button_clicked)
        
        self.hotkey_exit = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.hotkey_exit.activated.connect(self.exit_button_clicked)

        self.hotkey_find = QShortcut(QKeySequence('Ctrl+F'), self)
        self.hotkey_find.activated.connect(self.find_button_clicked)

        self.hotkey_replace = QShortcut(QKeySequence('Ctrl+R'), self)
        self.hotkey_replace.activated.connect(self.replace_button_clicked)

        self.hotkey_remove_line = QShortcut(QKeySequence('Ctrl+L'), self)
        self.hotkey_remove_line.activated.connect(self.remove_line)

        self.hotkey_remove_word = QShortcut(QKeySequence('Ctrl+W'), self)
        self.hotkey_remove_word.activated.connect(self.remove_word)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit) 

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.dialog_find = FindWindow(self, False)
        self.dialog_replace = FindWindow(self, True)


    def get_text_cursor(self):
        return self.textEdit.textCursor()


    def set_cursor(self, new_position):
        cursor = self.get_text_cursor()
        cursor.setPosition(new_position)
        self.textEdit.setTextCursor(cursor)


    def get_cursor_index(self):
        cursor = self.textEdit.textCursor()
        return cursor.selectionStart()


    def find_button_clicked(self):
        self.dialog_find.show()


    def replace_button_clicked(self):
        self.dialog_replace.show()
    

    def save_button_clicked(self):
        text = self.textEdit.toPlainText()
        with open(self.filename, 'w') as f:
            f.write(text)

    def exit_button_clicked(self):
        exit()


    def copy_button_clicked(self):
        self.textEdit.copy()


    def paste_button_clicked(self):
        self.textEdit.paste()


    def cut_button_clicked(self):
        self.textEdit.cut()


    def help_button_clicked(self):
        webbrowser.open('https://github.com/sverdlovvova/TextEditor')


    def _createActions(self):
        self.saveAction = QAction("&Save", self)
        self.saveAction.triggered.connect(self.save_button_clicked)
        
        self.exitAction = QAction("&Exit", self)
        self.exitAction.triggered.connect(self.exit_button_clicked)
        
        self.copyAction = QAction("&Copy", self)
        self.copyAction.triggered.connect(self.copy_button_clicked)

        self.pasteAction = QAction("&Paste", self)
        self.pasteAction.triggered.connect(self.paste_button_clicked)

        self.cutAction = QAction("&Cut", self)
        self.cutAction.triggered.connect(self.cut_button_clicked)

        self.findAction = QAction("Find", self)
        self.findAction.triggered.connect(self.find_button_clicked)

        self.findAndReplaceAction = QAction("Replace", self)
        self.findAndReplaceAction.triggered.connect(self.replace_button_clicked)
        
        self.helpAction = QAction("&Help", self)
        self.helpAction.triggered.connect(self.help_button_clicked)


    def _createMenuBar(self):
        menuBar = self.menuBar()
        #File menu
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        #Edit menu
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)
        findMenu = editMenu.addMenu("Find and Replace")
        findMenu.addAction(self.findAction)
        findMenu.addAction(self.findAndReplaceAction)
        #Help menu
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpAction)


    def remove_line(self):
        text = self.textEdit.toPlainText()
        i = self.get_cursor_index()
        if len(text) == 1:
            return
        if i < len(text) and text[i] == '\n' and text[i - 1] == '\n':
            new_text = text[:i] + text[i + 1:]
            self.textEdit.setPlainText(new_text)
            self.set_cursor(i)
            return
        if i == 0 and text[i] == '\n':
            new_text = text[i + 1:]
            self.textEdit.setPlainText(new_text)
            self.set_cursor(0)
            return
        begin = i - 1
        end = i + 1
        while begin >= 0 and text[begin] != '\n':
            begin -= 1
        while end < len(text) and text[end] != '\n':
            end += 1
        if begin != -1:
            begin -= 1
        new_text = text[:begin + 1] + text[end:]
        self.textEdit.setPlainText(new_text)
        self.set_cursor(begin + 1)


    def remove_word(self):
        text = self.textEdit.toPlainText()
        i = self.get_cursor_index()
        if not text[i - 1].isspace() and i < len(text):
            begin = i
            end = i
            while begin >= 0 and not text[begin].isspace():
                begin -= 1
            while end < len(text) and not text[end].isspace():
                end += 1
            new_text = text[:begin + 1] + text[end:]
            self.textEdit.setPlainText(new_text)
            self.set_cursor(begin + 1)

     

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


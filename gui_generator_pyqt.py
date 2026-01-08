import sys
# from googletrans import Translator
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox, QDialog, QDockWidget
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from file_parser import parse_file
from sentence_generator import generate_sentence
from poem_generator import generate_limerick


from deep_translator import GoogleTranslator

class TranslatorReal:
    def __init__(self):
        self.translator = GoogleTranslator(source='en', target='ru')

    def translate(self, text: str) -> str:
        try:
            return self.translator.translate(text)
        except Exception as e:
            return f"[Ошибка перевода: {e}]"


class GrammarViewer(QDialog):
    def __init__(self, grammar_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр грамматики")
        self.setGeometry(300, 300, 800, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
            }
            QTextEdit {
                font-family: 'Courier New', monospace;
                font-size: 12px;
                padding: 10px;
                border: 1px solid #ddd;
                background-color: white;
            }
        """)

        layout = QVBoxLayout(self)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont("Courier New", 12))
        text_edit.setPlainText(grammar_text)
        layout.addWidget(text_edit)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)


class SentenceGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Теория формальных языков в генерации текста")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ADD8E6;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
                margin: 5px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:pressed {
                opacity: 0.8;
            }
            QTextEdit {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background-color: white;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding: 10px;
            }
        """)
        self.translator = TranslatorReal()

        self.grammar = None
        self.terminals = None
        self.load_default_files()
        self.init_ui()


    def load_default_files(self):
        try:
            self.grammar = parse_file('grammar.txt')
            self.terminals = parse_file('terminals.txt')
            with open('grammar.txt', 'r', encoding='utf-8') as f:
                self.grammar_content = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файлы:\n{e}")


    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        title_label = QLabel("Генератор осмысленных предложений на основе формальной грамматики")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; color: #2c3e50; padding: 15px;")
        left_layout.addWidget(title_label)

        generate_button = QPushButton("Сгенерировать предложение")
        generate_button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                border: 2px solid #2c3e50;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        generate_button.clicked.connect(self.generate_and_display)
        left_layout.addWidget(generate_button, alignment=Qt.AlignmentFlag.AlignCenter)

        output_container = QWidget()
        output_layout = QVBoxLayout(output_container)
        output_layout.setSpacing(5)


        # ------------------ НОВЫЙ БЛОК: КНОПКИ ВЫБОРА РЕЖИМА ------------------
        self.generation_mode = "classic"  # по умолчанию

        classic_btn = QPushButton("Классическая КС-грамматика")
        classic_btn.clicked.connect(lambda: self.set_mode("classic"))
        left_layout.addWidget(classic_btn)

        stochastic_btn = QPushButton("Вероятностная генерация")
        stochastic_btn.clicked.connect(lambda: self.set_mode("stochastic"))
        left_layout.addWidget(stochastic_btn)

        rhymed_btn = QPushButton("С рифмой")
        rhymed_btn.clicked.connect(lambda: self.set_mode("rhymed"))
        left_layout.addWidget(rhymed_btn)
        # ----------------------------------------------------------------------

        eng_label = QLabel("Сгенерированное предложение:")
        eng_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        eng_label.setStyleSheet("""
            font-size: 17px;
            font-weight: bold;
            color: #2c3e50;
            padding: 5px 0;
        """)
        output_layout.addWidget(eng_label)


        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Segoe UI", 16))
        self.output_text.setStyleSheet("""
            border: 2px solid #2c3e50;
            border-radius: 8px;
            padding: 5px;
            background-color: white;
            min-height: 120px;
            max-height: 200px;
            font-size: 16px;
        """)
        output_layout.addWidget(self.output_text)


        ru_label = QLabel("Перевод:")
        ru_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        ru_label.setStyleSheet("""
            font-size: 17px;
            font-weight: bold;
            color: #2c3e50;
            padding: 5px;
        """)
        output_layout.addWidget(ru_label)

        self.translation_text = QTextEdit()
        self.translation_text.setReadOnly(True)
        self.translation_text.setFont(QFont("Segoe UI", 14))
        self.translation_text.setStyleSheet("""
            border: 2px solid #2c3e50;
            border-radius: 8px;
            padding: 5px;
            background-color: white;
            min-height: 120px;
            max-height: 200px;
            font-size: 16px;
        """)
        output_layout.addWidget(self.translation_text)

        left_layout.addWidget(output_container)

        main_layout.addWidget(left_widget, stretch=3)

        dock = QDockWidget("", self)
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock.setStyleSheet("""
            QDockWidget {
                background-color: #ffffff;
                border: 1px solid #ddd;
            }
        """)

        container_widget = QWidget()
        container_widget.setStyleSheet("""
            background-color: white;
            border: 2px solid #2c3e50;
            border-radius: 8px;
            padding: 10px;
        """)
        container_widget.setFixedHeight(250)
        container_layout = QVBoxLayout(container_widget)
        container_layout.setSpacing(10)

        menu_title = QLabel("Меню")
        menu_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
            border-bottom: 2px solid #2c3e50;
        """)

        container_layout.addWidget(menu_title)

        copy_button = QPushButton("Копировать предложение")
        copy_button.setStyleSheet("color: white; background-color: #2c3e50;")
        copy_button.clicked.connect(self.copy_to_clipboard)
        
        copy_translation_button = QPushButton("Копировать перевод")
        copy_translation_button.setStyleSheet("color: white; background-color: #2c3e50;")
        copy_translation_button.clicked.connect(self.copy_translation_to_clipboard)

        clear_button = QPushButton("Очистить")
        clear_button.setStyleSheet("color: white; background-color: #2c3e50;")
        clear_button.clicked.connect(self.clear_output)

        # view_grammar_button = QPushButton("Посмотреть грамматику")
        # view_grammar_button.setStyleSheet("color: white; background-color: #2c3e50;")
        # view_grammar_button.clicked.connect(self.show_grammar)

        container_layout.addWidget(copy_button)
        container_layout.addWidget(copy_translation_button)
        container_layout.addWidget(clear_button)
        # container_layout.addWidget(view_grammar_button)
        container_layout.addStretch()

        dock.setWidget(container_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("≡")
        # file_menu = menu_bar.addMenu(QIcon("menu.png"), "")

        load_grammar_action = file_menu.addAction("Загрузить грамматику")
        load_grammar_action.triggered.connect(self.load_grammar_file)

        load_terminals_action = file_menu.addAction("Загрузить терминалы")
        load_terminals_action.triggered.connect(self.load_terminals_file)

        exit_action = file_menu.addAction("Выход")
        exit_action.triggered.connect(self.close)

    def generate_and_display(self):
        if not self.grammar or not self.terminals:
            QMessageBox.warning(self, "Ошибка", "Грамматика или терминалы не загружены")
            return

        try:
            sentence = generate_sentence(self.grammar, self.terminals)
            sentence = sentence[0].upper() + sentence[1:] + "."
            self.output_text.setPlainText(sentence)

            translated = self.translator.translate(sentence)
            self.translation_text.setPlainText(translated)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сгенерировать предложение:\n{e}")

    def copy_to_clipboard(self):
        text = self.output_text.toPlainText().strip()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Копирование", "Оригинальное предложение скопировано в буфер обмена")
        else:
            QMessageBox.warning(self, "Нет текста", "Сначала сгенерируйте предложение")

    def save_to_file(self):
        text = self.output_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Нет текста", "Сначала сгенерируйте предложение")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как", "sentence.txt",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            QMessageBox.information(self, "Сохранено", f"Предложение сохранено в:\n{file_path}")

    def copy_translation_to_clipboard(self):
        text = self.translation_text.toPlainText().strip()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Копирование", "Перевод скопирован в буфер обмена")
        else:
            QMessageBox.warning(self, "Нет текста", "Сначала сгенерируйте предложение и дождитесь перевода")

    def clear_output(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Очистка")
        msg_box.setText("Вы уверены, что хотите очистить?")
        msg_box.setIcon(QMessageBox.Icon.Question)

        btn_all = msg_box.addButton("Да, очистить оба поля", QMessageBox.ButtonRole.YesRole)
        btn_sentence = msg_box.addButton("Очистить только предложение", QMessageBox.ButtonRole.NoRole)
        btn_cancel = msg_box.addButton("Нет, отменить", QMessageBox.ButtonRole.RejectRole)

        msg_box.exec()

        if msg_box.clickedButton() == btn_all:
            self.output_text.clear()
            self.translation_text.clear()
            QMessageBox.information(self, "Очистка", "Оба поля очищены")
        elif msg_box.clickedButton() == btn_sentence:
            self.output_text.clear()
            QMessageBox.information(self, "Очистка", "Предложение очищено")
        elif msg_box.clickedButton() == btn_cancel:
            pass

    def show_grammar(self):
        viewer = GrammarViewer(self.grammar_content, self)
        viewer.exec()

    def load_grammar_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите grammar.txt", "", "TXT Files (*.txt)"
        )
        if path:
            try:
                self.grammar = parse_file(path)
                QMessageBox.information(self, "Успешно", "Грамматика загружена")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить грамматику:\n{e}")

    def load_terminals_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите terminals.txt", "", "TXT Files (*.txt)"
        )
        if path:
            try:
                self.terminals = parse_file(path)
                QMessageBox.information(self, "Успешно", "Терминалы загружены!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить терминалы:\n{e}")

        
    # ------------------ НОВАЯ ФУНКЦИЯ ------------------
    def set_mode(self, mode):
        self.generation_mode = mode
        QMessageBox.information(self, "Режим генерации", f"Выбран режим: {mode}")

    # ------------------ ИЗМЕНЕНИЕ generate_and_display ------------------
    def generate_and_display(self):
        if not self.grammar or not self.terminals:
            QMessageBox.warning(self, "Ошибка", "Грамматика или терминалы не загружены")
            return

        try:
            # ------------------ ВЫБОР ФУНКЦИИ ПО РЕЖИМУ ------------------
            if self.generation_mode == "classic":
                sentence = generate_sentence(self.grammar, self.terminals)  # обычная
            elif self.generation_mode == "stochastic":
                sentence = generate_sentence(self.grammar, self.terminals, probabilistic = True)  # вероятностная
            elif self.generation_mode == "rhymed":
                sentence = generate_limerick(self.grammar, self.terminals)  # рифмованная
            else:
                sentence = generate_sentence(self.grammar, self.terminals)
            # --------------------------------------------------------------

            sentence = sentence[0].upper() + sentence[1:] + "."
            self.output_text.setPlainText(sentence)

            translated = self.translator.translate(sentence)
            self.translation_text.setPlainText(translated)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сгенерировать предложение:\n{e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SentenceGeneratorApp()
    window.show()
    sys.exit(app.exec())

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox, QDialog, QDockWidget
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from file_parser import parse_file
from sentence_generator import generate_sentence
from poem_generator import generate_limerick
<<<<<<< HEAD
from syntax_analyzer import SyntaxAnalyzer
=======


>>>>>>> 87d1ca11544f29698bb83fc50e9a83b8eef9eaa8
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
        self.setGeometry(100, 100, 950, 750)
        self.setStyleSheet("""
            QMainWindow { background-color: #ADD8E6; }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
                margin: 5px;
            }
            QPushButton:hover { opacity: 0.9; }
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

        # Храним данные и пути к файлам
        self.grammar = None
        self.terminals = None

        self.grammar_path = os.path.abspath('grammar.txt')
        self.terminals_path = os.path.abspath('terminals.txt')

        self.analyzer = None

        self.load_default_files()
        self.init_ui()

    def load_default_files(self):
        try:
            if not os.path.exists(self.grammar_path) or not os.path.exists(self.terminals_path):
                print("Файлы по умолчанию не найдены, выберите их вручную через меню.")
                return

            self.grammar = parse_file(self.grammar_path)
            self.terminals = parse_file(self.terminals_path)

            self.analyzer = SyntaxAnalyzer(
                self.grammar_path, self.terminals_path)

            with open(self.grammar_path, 'r', encoding='utf-8') as f:
                self.grammar_content = f.read()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки",
                                 f"Не удалось загрузить стандартные файлы:\n{e}")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        title_label = QLabel("Генератор осмысленных предложений")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 20px; color: #2c3e50; padding: 15px;")
        left_layout.addWidget(title_label)

        generate_button = QPushButton("Сгенерировать предложение")
        generate_button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                border: 2px solid #2c3e50;
                color: white;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        generate_button.clicked.connect(self.generate_and_display)
        left_layout.addWidget(generate_button)

        output_container = QWidget()
        output_layout = QVBoxLayout(output_container)
        output_layout.setSpacing(5)

<<<<<<< HEAD
        self.generation_mode = "classic"

        classic_btn = QPushButton("Классическая КС-грамматика")
        classic_btn.setStyleSheet("background-color: #ecf0f1; color: #2c3e50;")
=======

        # ------------------ НОВЫЙ БЛОК: КНОПКИ ВЫБОРА РЕЖИМА ------------------
        self.generation_mode = "classic"  # по умолчанию

        classic_btn = QPushButton("Классическая КС-грамматика")
>>>>>>> 87d1ca11544f29698bb83fc50e9a83b8eef9eaa8
        classic_btn.clicked.connect(lambda: self.set_mode("classic"))
        left_layout.addWidget(classic_btn)

        stochastic_btn = QPushButton("Вероятностная генерация")
<<<<<<< HEAD
        stochastic_btn.setStyleSheet(
            "background-color: #ecf0f1; color: #2c3e50;")
=======
>>>>>>> 87d1ca11544f29698bb83fc50e9a83b8eef9eaa8
        stochastic_btn.clicked.connect(lambda: self.set_mode("stochastic"))
        left_layout.addWidget(stochastic_btn)

        rhymed_btn = QPushButton("С рифмой")
<<<<<<< HEAD
        rhymed_btn.setStyleSheet("background-color: #ecf0f1; color: #2c3e50;")
        rhymed_btn.clicked.connect(lambda: self.set_mode("rhymed"))
        left_layout.addWidget(rhymed_btn)

        eng_label = QLabel("Предложение (можно редактировать):")
=======
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
>>>>>>> 87d1ca11544f29698bb83fc50e9a83b8eef9eaa8
        output_layout.addWidget(eng_label)

        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText(
            "Введите текст или сгенерируйте...")
        self.output_text.setFont(QFont("Segoe UI", 16))
        self.output_text.setStyleSheet(
            "border: 2px solid #2c3e50; border-radius: 8px; padding: 5px;")
        output_layout.addWidget(self.output_text)

        ru_label = QLabel("Перевод:")
        output_layout.addWidget(ru_label)

        self.translation_text = QTextEdit()
        self.translation_text.setReadOnly(True)
        self.translation_text.setFont(QFont("Segoe UI", 14))
        self.translation_text.setStyleSheet(
            "border: 2px solid #2c3e50; border-radius: 8px; padding: 5px; background-color: #f0f0f0;")
        output_layout.addWidget(self.translation_text)

        left_layout.addWidget(output_container)
        main_layout.addWidget(left_widget, stretch=3)

        dock = QDockWidget("", self)
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock.setStyleSheet("QDockWidget { border: none; }")

        container_widget = QWidget()
        container_widget.setStyleSheet("""
            background-color: white;
            border: 2px solid #2c3e50;
            border-radius: 8px;
            padding: 10px;
        """)
        container_widget.setFixedHeight(380)

        container_layout = QVBoxLayout(container_widget)
        container_layout.setSpacing(5)

        menu_title = QLabel("Меню")
        menu_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_title.setStyleSheet(
            "font-size: 20px; font-weight: bold; border-bottom: 2px solid #2c3e50; margin-bottom: 10px;")
        container_layout.addWidget(menu_title)

        check_syntax_button = QPushButton("Запустить анализатор")
        check_syntax_button.setCursor(Qt.CursorShape.PointingHandCursor)
        check_syntax_button.setStyleSheet("""
            QPushButton {
                color: white; 
                background-color: #085182; 
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover { background-color: #0b65bf; }
        """)
        check_syntax_button.clicked.connect(self.check_syntax)
        container_layout.addWidget(check_syntax_button)

        copy_button = QPushButton("Копировать предложение")
        copy_button.setStyleSheet(
            "color: white; background-color: #2c3e50; padding: 12px;")
        copy_button.clicked.connect(self.copy_to_clipboard)
        container_layout.addWidget(copy_button)

        copy_translation_button = QPushButton("Копировать перевод")
        copy_translation_button.setStyleSheet(
            "color: white; background-color: #2c3e50; padding: 12px;")
        copy_translation_button.clicked.connect(
            self.copy_translation_to_clipboard)
        container_layout.addWidget(copy_translation_button)

        clear_button = QPushButton("Очистить")
        clear_button.setStyleSheet(
            "color: white; background-color: #7f8c8d; padding: 12px;")
        clear_button.clicked.connect(self.clear_output)
        container_layout.addWidget(clear_button)

        container_layout.addStretch()

        dock.setWidget(container_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction("Загрузить грамматику").triggered.connect(
            self.load_grammar_file)
        file_menu.addAction("Загрузить терминалы").triggered.connect(
            self.load_terminals_file)
        file_menu.addAction("Выход").triggered.connect(self.close)


    def check_syntax(self):
        text = self.output_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Пусто", "Нет текста для проверки.")
            return
        if self.generation_mode == "rhymed":
            QMessageBox.warning(self, "Ограничение",
                                "Синтаксический анализ доступен только для простых предложений (КС-грамматика).\n"
                                "Для стихотворений эта функция отключена, так как структура слишком сложна.")
            return
        if not self.analyzer:
            QMessageBox.critical(
                self, "Ошибка", "Анализатор не инициализирован.")
            return

        is_valid, tree = self.analyzer.parse(text)

        if is_valid:
            filename = "parse_tree"
            try:
                tree.save_tree_image(filename)
                QMessageBox.information(self, "Результат",
                                        f"Предложение принадлежит языку.\n\nДерево сохранено в: {filename}.png")
            except Exception as e:
                QMessageBox.warning(self, "Результат",
                                    f"Предложение принадлежит языку.\n(Ошибка сохранения картинки: {e})")
        else:
            QMessageBox.warning(self, "Результат",
                                "Предложение не принадлежит языку.")

    def set_mode(self, mode):
        self.generation_mode = mode
        msg = f"Выбран режим: {mode}"
        if mode == "rhymed":
            msg += "\n(Проверка синтаксиса будет недоступна)"
        QMessageBox.information(self, "Режим", msg)

    def generate_and_display(self):
        if not self.grammar or not self.terminals:
            QMessageBox.warning(self, "Ошибка", "Файлы не загружены")
            return

        try:
            if self.generation_mode == "classic":
                sentence = generate_sentence(self.grammar, self.terminals)
            elif self.generation_mode == "stochastic":
                sentence = generate_sentence(
                    self.grammar, self.terminals, probabilistic=True)
            elif self.generation_mode == "rhymed":
                sentence = generate_limerick(self.grammar, self.terminals)
            else:
                sentence = generate_sentence(self.grammar, self.terminals)

            sentence = sentence[0].upper() + sentence[1:]
            if not (sentence.endswith('.') or sentence.endswith('!') or sentence.endswith('?')):
                sentence += "."

            self.output_text.setPlainText(sentence)

            translated = self.translator.translate(sentence)
            self.translation_text.setPlainText(translated)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка генерации", str(e))

    def copy_to_clipboard(self):
        text = self.output_text.toPlainText().strip()
        if text:
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "Успех", "Скопировано!")

    def copy_translation_to_clipboard(self):
        text = self.translation_text.toPlainText().strip()
        if text:
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "Успех", "Перевод скопирован!")

    def clear_output(self):
        self.output_text.clear()
        self.translation_text.clear()

    def load_grammar_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл грамматики", "", "TXT Files (*.txt)")
        if path:
            try:
                self.grammar = parse_file(path)
                self.grammar_path = path
                self.analyzer = SyntaxAnalyzer(
                    self.grammar_path, self.terminals_path)
                QMessageBox.information(
                    self, "Успешно", "Грамматика загружена и анализатор обновлен.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Сбой загрузки: {e}")

    def load_terminals_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл терминалов", "", "TXT Files (*.txt)")
        if path:
            try:
                self.terminals = parse_file(path)
                self.terminals_path = path
                self.analyzer = SyntaxAnalyzer(
                    self.grammar_path, self.terminals_path)
                QMessageBox.information(
                    self, "Успешно", "Терминалы загружены и анализатор обновлен.")
            except Exception as e:
<<<<<<< HEAD
                QMessageBox.critical(self, "Ошибка", f"Сбой загрузки: {e}")
=======
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

>>>>>>> 87d1ca11544f29698bb83fc50e9a83b8eef9eaa8


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SentenceGeneratorApp()
    window.show()
    sys.exit(app.exec())

import sys
import PreSavedMovesUi
from Model import Model
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class PreSavedMoves(QtWidgets.QMainWindow, PreSavedMovesUi.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.model = None
        self.move_script_file_path = None
        self.default_move_script_text = "Move script is now empty"
        self.place_default_text()

        self.open_script_file_btn.clicked.connect(self.open_move_script)
        self.load_script_file_btn.clicked.connect(self.load_move_script)
        self.send_full_sequence_btn.clicked.connect(self.send_full_sequence)
        self.send_next_command_btn.clicked.connect(self.send_next_command)

    def set_model(self, model: Model):
        self.model = model

    def place_default_text(self):
        self.move_script_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.move_script_label.setWordWrap(True)
        self.move_script_label.setText(self.default_move_script_text)

    def open_move_script(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if file_path:
            self.script_file_path_label.setText(file_path)
            self.move_script_file_path = file_path

    def load_move_script(self):
        if self.move_script_file_path is None:
            QMessageBox.warning(self, 'Warning', 'Undefined file location')
        else:
            with open(self.move_script_file_path, 'r') as file:
                file_data = file.read()
                self.move_script_label.setText(file_data)
                file.close()
            # QMessageBox.information(self, 'Success', 'Data successfully saved!')

    # TODO: Data can be loaded from the file. Need to do data transition!
    def send_full_sequence(self):
        text_bytes = self.move_script_label.text().split()
        print(f'PreSavedMoves/send_full_sequence - ready to send file data (len = {len(text_bytes)}):')
        print(*text_bytes)

    def send_next_command(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PreSavedMoves()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QComboBox,
                             QMessageBox, QFormLayout, QDialog, QLineEdit, QMainWindow, QToolBar, QAction, QCheckBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PIL import Image

# Load language file from the locale directory
def load_language(language_code):
    language_file = os.path.join('locale', f'{language_code}.json')
    if os.path.exists(language_file):
        with open(language_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        # Fallback to English if language file doesn't exist
        print(f"Language file '{language_code}' not found, falling back to English.")
        return load_language('en')

# Load settings (default save location and language)
def load_settings():
    settings = {'save_location': '', 'language': 'en', 'always_create_folder': 'False'}
    if os.path.exists('settings.txt'):
        with open('settings.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                settings[key] = value
    return settings

# Save settings to file
def save_settings(save_location, language, always_create_folder):
    with open('settings.txt', 'w') as file:
        file.write(f'save_location={save_location}\n')
        file.write(f'language={language}\n')
        file.write(f'always_create_folder={always_create_folder}\n')

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = load_settings()
        self.language_data = parent.language_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.language_data['settings'])

        layout = QFormLayout()

        # Default Save Location (Folder selection dialog)
        self.save_location_edit = QLineEdit(self)
        self.save_location_edit.setText(self.settings['save_location'])
        self.btn_select_folder = QPushButton(self.language_data['select_folder'], self)
        self.btn_select_folder.clicked.connect(self.openFolderDialog)

        layout.addRow(self.language_data['default_save_location'], self.save_location_edit)
        layout.addRow(self.btn_select_folder)

        # Language Selection
        self.language_combo = QComboBox(self)
        self.language_combo.addItems(self.available_languages())
        self.language_combo.setCurrentText(self.settings['language'])
        layout.addRow(self.language_data['language'], self.language_combo)

        # Always Create Folder Checkbox
        self.always_create_folder_checkbox = QCheckBox(self.language_data['always_create_folder'], self)
        self.always_create_folder_checkbox.setCheckable(True)
        self.always_create_folder_checkbox.setChecked(self.settings['always_create_folder'] == 'True')
        layout.addRow(self.always_create_folder_checkbox)

        # Save Button
        self.save_button = QPushButton(self.language_data['save_settings'], self)
        self.save_button.clicked.connect(self.saveSettings)
        layout.addRow(self.save_button)

        self.setLayout(layout)

    def openFolderDialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, self.language_data['select_folder'])
        if folder_path:
            self.save_location_edit.setText(folder_path)

    def available_languages(self):
        return [f.split('.')[0] for f in os.listdir('locale') if f.endswith('.json')]

    def saveSettings(self):
        save_location = self.save_location_edit.text()
        language = self.language_combo.currentText()
        always_create_folder = 'True' if self.always_create_folder_checkbox.isChecked() else 'False'
        save_settings(save_location, language, always_create_folder)
        QMessageBox.information(self, 'Info', self.language_data['settings_saved'])
        self.close()

class ImageConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.language_data = load_language(self.settings['language'])  # Load language based on settings
        self.file_paths = []  # List to hold multiple file paths
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.language_data['title'])
        self.setGeometry(300, 300, 600, 400)
        self.setWindowIcon(QIcon('res/icon.png'))
        # Toolbar with Settings menu
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        settings_action = QAction(self.language_data['settings'], self)
        settings_action.triggered.connect(self.openSettings)
        toolbar.addAction(settings_action)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Image preview
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(250, 250)

        # Label to show the selected file paths
        self.file_label = QLabel(self.language_data['no_file_selected'], self)
        self.file_label.setAlignment(Qt.AlignCenter)

        # Button to select images
        self.btn_select = QPushButton(self.language_data['select_images'], self)
        self.btn_select.clicked.connect(self.openFileDialog)

        # Dropdown for selecting output format
        self.combo_format = QComboBox(self)
        self.combo_format.addItems(['png', 'jpeg', 'jpg', 'webp', 'jfif'])

        # Convert button
        self.btn_convert = QPushButton(self.language_data['convert'], self)
        self.btn_convert.clicked.connect(self.convertImages)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.file_label)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.combo_format)
        layout.addWidget(self.btn_convert)

        central_widget.setLayout(layout)

    def openSettings(self):
        settings_window = SettingsWindow(self)
        settings_window.exec_()
        self.settings = load_settings()  # Reload settings after closing the settings window
        self.language_data = load_language(self.settings['language'])  # Reload language data based on updated settings
        self.refreshUI()

    def refreshUI(self):
        """Refresh UI elements based on the new language."""
        self.setWindowTitle(self.language_data['title'])
        self.file_label.setText(self.language_data['no_file_selected'])
        self.btn_select.setText(self.language_data['select_images'])
        self.btn_convert.setText(self.language_data['convert'])

    def openFileDialog(self):
        options = QFileDialog.Options()
        file_filter = "Images (*.png *.jpg *.jpeg *.jfif *.webp)"
        files, _ = QFileDialog.getOpenFileNames(self, self.language_data['select_images'], "", file_filter, options=options)
        if files:
            self.file_paths = files
            self.file_label.setText(f'{len(files)} {self.language_data["files_selected"]}')
            pixmap = QPixmap(files[0])  # Show preview of the first selected image
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def convertImages(self):
        if self.file_paths:
            try:
                # Check whether to create a folder or not
                always_create_folder = self.settings['always_create_folder'] == 'True'
                multiple_files = len(self.file_paths) > 1

                # Create a folder only if "Always Create Folder" is checked or if there are multiple files
                if always_create_folder or multiple_files:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    save_folder_name = f'{self.language_data["converted_folder"]}_{timestamp}'
                    save_location = self.settings['save_location'] or os.path.dirname(self.file_paths[0])
                    output_folder = os.path.join(save_location, save_folder_name)

                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                else:
                    # If only one file and no folder is needed, save in the default location
                    output_folder = self.settings['save_location'] or os.path.dirname(self.file_paths[0])

                output_format = self.combo_format.currentText()

                for file_path in self.file_paths:
                    img = Image.open(file_path)
                    if output_format.lower() in ['jpeg', 'jpg'] and img.mode == 'RGBA':
                        # Convert RGBA to RGB by removing the alpha channel and filling transparent parts with white
                        img = Image.alpha_composite(Image.new('RGB', img.size, (255, 255, 255)), img.convert('RGBA'))

                    output_file_name = os.path.splitext(os.path.basename(file_path))[0] + f'.{output_format}'
                    output_file_path = os.path.join(output_folder, output_file_name)
                    img.save(output_file_path, format=output_format.upper())

                QMessageBox.information(self, 'Success', self.language_data['success'].format(len(self.file_paths), output_folder))
            except Exception as e:
                QMessageBox.critical(self, 'Error', self.language_data['error'].format(e))
        else:
            QMessageBox.warning(self, 'Warning', self.language_data['warning'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageConverter()
    ex.show()
    sys.exit(app.exec_())

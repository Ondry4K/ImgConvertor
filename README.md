# ImgConvertor for Windows 🌟

## Overview

**ImgConvertor for Windows** is a fast and user-friendly desktop application designed to convert images between various formats. Built with Python and Qt5, this app offers a seamless experience for converting images, managing file formats, and customizing save options.

## Features 🚀

- **Multi-format Conversion**: Convert images between formats such as `.webp`, `.jpeg`, `.jfif`, `.jpg`, `.png`, and more.
- **Batch Processing**: Select and convert multiple images simultaneously.
- **Dynamic Folder Creation**: Automatically create timestamped folders for storing converted images. Customize this behavior through the settings.
- **Flexible Save Locations**: Choose where to save converted images or create new folders as needed.
- **Language Support**: Select from multiple languages with support managed through JSON files in the `/locale` directory.
- **Image Preview**: View images before conversion to ensure accuracy.
- **Settings Customization**: Configure default save locations, languages, and folder creation preferences.

## Installation 📦

### Download the Setup File

1. Go to the [Releases page](https://github.com/Ondry4K/ImgConvertor/releases) on GitHub.
2. Download the latest setup file for Windows.
3. Run the setup file and follow the on-screen instructions to install ImgConvertor for Windows.

### Build the App Yourself 🛠️

If you prefer to build the app yourself, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/image-converter-app.git
   cd image-converter-app
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Build with PyInstaller**:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```
   - The built application will be located in the `dist` directory.

4. **Run the Application**:
   ```bash
   dist/main.exe
   ```

## Usage

1. **Open the Application**: Launch ImgConvertor for Windows.
2. **Select Images**: Click "Select Images" to choose the files you want to convert.
3. **Choose Output Format**: Select the desired format from the dropdown menu.
4. **Convert Images**: Click "Convert" to start the process.
5. **View Converted Images**: Check the designated folder for your converted images.

## Settings ⚙️

- **Default Save Location**: Specify where converted images should be saved.
- **Language**: Select your preferred language for the interface.
- **Always Create Folder**: Enable or disable automatic folder creation for conversions.

## Localization 🌍

Language files are located in the `/locale` directory. Add or update JSON files to support additional languages.

## Performance Comparison 🚀

Here’s how ImgConvertor for Windows stacks up against popular online converters:

| Feature              | ImgConvertor for Windows | FreeConvert | CloudConvert | AnyConv |
|----------------------|---------------------------|---------------------|---------------------|---------------------|
| **Formats Supported**| Multiple formats          | Limited formats     | Multiple formats    | Limited formats     |
| **Batch Processing** | Yes                       | No                  | Yes                 | No                  |
| **Image Preview**    | Yes                       | No                  | Yes                 | No                  |
| **Folder Creation**  | Customizable              | Fixed output path   | Fixed output path   | Fixed output path   |
| **Speed**            | Up to 75% faster           | Slower              | Slower              | Slower              |

*Note: Speed comparison is approximate and may vary depending on your CPU.*[^1]

## Contributing 🤝

We welcome contributions! Feel free to open issues or submit pull requests on GitHub if you have suggestions or improvements.

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact 📧

For questions or support, reach out to [ondry@inquiries.co.uk](mailto:ondrygfx@gmail.com).

[^1]: Tested on Intel i5-10th generation

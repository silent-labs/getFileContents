# File Contents Processor

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A modern and user-friendly desktop application designed to process and combine the contents of multiple files. Perfect for developers who need to share code with AI tools like ChatGPT, Claude, or GitHub Copilot. The application makes it easy to extract and combine the contents of large programming projects into a single text file, making it simple to share your codebase with AI assistants for better context and more accurate responses.

## 🚀 Features

- **Modern GUI Interface**
  - Clean and intuitive design
  - Dark and light theme support
  - System tray integration
  - File search functionality

- **File Management**
  - Multiple file selection
  - Detailed file information (size, type, modification date)
  - Advanced file filtering
  - Directory traversal

- **Processing Capabilities**
  - Combine multiple file contents
  - Preserve file metadata
  - UTF-8 encoding support

- **User Experience**
  - Global hotkey support (Ctrl+Alt+P)
  - Persistent theme preferences
  - Responsive interface
  - Real-time search filtering

## 🎯 Main Use Cases

- **AI Development Assistance**
  - Extract entire project contents for AI tools
  - Share code context with ChatGPT, Claude, or other AI assistants
  - Maintain file structure information for better AI understanding
  - Easily copy large codebases for AI analysis

- **Code Documentation**
  - Generate comprehensive project overviews
  - Create code documentation templates
  - Export code for review or sharing

## 📋 Prerequisites

- Python 3.12 or higher
- Required Python packages:
  ```
  tkinter
  keyboard
  pystray
  pillow
  setproctitle
  ```

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/getFileContents.git
   cd getFileContents
   ```

2. Install required packages:
   ```bash
   pip install keyboard pystray pillow setproctitle
   ```

3. Run the application:
   ```bash
   python file_processor.py
   ```

## 💡 Usage

1. **Launch the Application**
   - Run `file_processor.py`
   - The application will start minimized in the system tray
   - Press `Ctrl+Alt+P` to show/hide the window

2. **Select Files**
   - Click "Select Folder" to choose your project directory
   - Use the search bar to filter specific files
   - Select the files you want to include in your AI context
   - View detailed file information including size and modification date

3. **Process Files for AI Tools**
   - Select the relevant project files
   - Click "Process Selected"
   - Choose an output location for the combined file
   - The resulting text file will contain all file contents with clear separators
   - Copy the contents and paste them into your preferred AI tool

4. **Customize Appearance**
   - Toggle between dark and light themes
   - Theme preference is automatically saved

## 📝 Best Practices for AI Integration

- Select only relevant files to maintain context quality
- Include key configuration and documentation files
- Organize files in a logical order before processing
- Consider file size limits of your AI tool
- Remove sensitive information before sharing

## ⌨️ Keyboard Shortcuts

| Shortcut    | Action                 |
|-------------|------------------------|
| Ctrl+Alt+P  | Show/Hide Application  |

## 🛠️ Technical Details

The application is built using:
- Python's Tkinter for the GUI
- TTK widgets for modern styling
- Custom theme implementation
- System tray integration using pystray
- File system operations with os module

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Your Name - [@yourusername](https://twitter.com/yourusername)

Project Link: [https://github.com/yourusername/getFileContents](https://github.com/yourusername/getFileContents)

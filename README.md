# Modern Mod Manager

A sleek and intuitive desktop application for managing game mods across multiple popular games. Built with Python and CustomTkinter for a modern, user-friendly interface.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/customtkinter-v5.2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 🎮 Supported Games

- **Zenless Zone Zero**
- **Wuthering Waves**
- **Genshin Impact**
- **Honkai: Star Rail**

## ✨ Features

- **Multi-Game Support**: Manage mods for multiple games from a single interface
- **Intuitive Character Selection**: Browse characters with intelligent name matching
- **Smart Mod Detection**: Automatically detects currently installed mods
- **One-Click Replacement**: Replace mods with a single button click
- **Modern UI**: Clean, responsive interface with dark/light theme support
- **Persistent Settings**: Automatically saves your mod directory configurations
- **Safe Operations**: Backup and replace operations with error handling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/modern-mod-manager.git
   cd modern-mod-manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
mod_manager/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── config/                # Configuration management
│   ├── __init__.py
│   ├── constants.py       # Game and character data
│   └── settings.py        # Settings save/load functions
├── gui/                   # User interface components
│   ├── __init__.py
│   ├── app.py            # Main application window
│   ├── tabs/             # Tab implementations
│   │   ├── __init__.py
│   │   ├── settings_tab.py  # Settings configuration tab
│   │   └── game_tab.py      # Individual game mod tabs
│   └── widgets/          # Custom UI widgets
│       ├── __init__.py
│       └── custom_widgets.py
└── utils/                # Utility functions
    ├── __init__.py
    ├── character_matcher.py  # Character name matching
    └── file_operations.py    # File system operations
```

## 🛠️ Usage

### Initial Setup

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Configure game directories** in the Settings tab:
   - **Mods From**: Directory containing your mod collections (organized by character)
   - **Mods To**: Your game's mod directory where mods are installed

3. **Directory Structure Example**:
   ```
   Mods From/
   ├── Anby/
   │   ├── Mod1_Anby_Outfit/
   │   ├── Mod2_Anby_Hair/
   │   └── Mod3_Anby_Weapon/
   └── Ellen/
       ├── Mod1_Ellen_Skin/
       └── Mod2_Ellen_Effects/
   
   Mods To/
   └── [Your game's mod folder]
   ```

### Managing Mods

1. **Select a game tab** (e.g., "ZenlessZoneZero")
2. **Choose a character** from the left panel
3. **Browse available mods** in the center panel
4. **View currently installed mods** at the bottom
5. **Select a mod** and click "Replace" to install it

### Features in Detail

- **Smart Character Matching**: The app automatically matches folder names to known character names
- **Current Mod Display**: See which mods are currently installed for each character
- **Safe Replacement**: Old mods are safely removed before installing new ones
- **Error Handling**: Clear error messages for common issues

## ⚙️ Configuration

The application stores settings in `mod_manager_data.json`:

```json
{
  "ZenlessZoneZero": {
    "from": "/path/to/your/mod/collection",
    "to": "/path/to/game/mod/folder"
  },
  "Wuthering Waves": {
    "from": "/path/to/ww/mods",
    "to": "/path/to/ww/game/mods"
  }
}
```

## 🎨 Customization

### Adding New Characters

Edit `config/constants.py` and add character names to the appropriate game list:

```python
CHARACTER_LISTS = {
    "ZenlessZoneZero": [
        'Anby', 'Ellen', 'Nekomata', 'YourNewCharacter'
        # Add more characters here
    ]
}
```

### Adding New Games

1. Add the game name to `GAME_TABS` in `config/constants.py`
2. Create a character list for the new game
3. The application will automatically create a new tab

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Setup

1. Clone your fork and install dependencies
2. Make changes following the existing code structure
3. Test your changes thoroughly
4. Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Bug Reports & Feature Requests

Please use the [GitHub Issues](https://github.com/yourusername/modern-mod-manager/issues) page to:
- Report bugs
- Request new features
- Ask questions

When reporting bugs, please include:
- Operating system and version
- Python version
- Steps to reproduce the issue
- Screenshots if applicable

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI
- Inspired by the gaming modding community
- Thanks to all contributors and testers

## 📞 Support

If you find this project useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting issues
- 🤝 Contributing improvements
- 📢 Sharing with others

---

**Happy Modding!** 🎮✨
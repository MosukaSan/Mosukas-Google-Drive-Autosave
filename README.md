# Mosuka's Google Drive Autosave
![](https://img.shields.io/badge/license-GPLv3-orange.svg)
![](https://tokei.rs/b1/github/MosukaSan/mosukas-google-drive-autosave?category=code)

<p align=center>
    <img src=icon.png height=200px>
</p>
A script that automatically saves your projects on google drive after pressing ctrl+s or after a specific time range.

- [Mosuka's Google Drive Autosave](#mosukas-google-drive-autosave)
    - [Installation](#installation)
    - [How to use](#how-to-use)
- [Modifying](#modifying)
- [To add](#to-add)

##  Installation
### Windows
Install the latest [Release](https://github.com/MosukaSan/Mosukas-Google-Drive-Autosave/releases).

### Arch
```bash
Soon...
```

### Debian
```bash
Soon...
```

## How to use
1. Install;
2. Login into your google account;
3. Select a folder or a file on your pc to save;
4. Select a mode:
    - Save after a period of time;
    - Save every time you press ctrl+s;
5. Let the program running. (Don't close it, it don't run on backgorund).

# Modifying
For the project to work, you need to:
1. Clone this repository;
2. Install Python 3;
3. Install project dependencies;
```bash
pip install -r requirements.txt
```
4. Create a [Google Cloud](https://cloud.google.com) project;
5. Install the Google Drive API;
6. Configure the OAuth permission screen and add the `https://www.googleapis.com/auth/drive.file` scope;
7. Create an OAuth Client ID and download the JSON file;
8. Move it to the project folder and rename it to credentials.json;
9. the main code is in src/mosukas_google_drive_autosave, have fun!

# To add
- ✅ Custom hotkeys;
- ✅ GUI.

# 📘 TutorialsPoint to PDF

A Python script that downloads complete TutorialsPoint tutorials, merges all chapters, and converts them into high quality PDF files.

Designed for reliable offline reading and personal study archives.

---

## ✨ Features

- Select a specific category or download all categories  
- Choose individual tutorials or bulk download  
- Parallel chapter downloading using threads  
- Automatic image URL fixing  
- Clean HTML output  
- Automatic PDF generation using WeasyPrint  
- Progress bar for chapter downloads  
- Safe and clean file naming  

---

## 🐍 Python Version

This project is tested with:

- **Python 3.13.7**
- pip 25.2

No virtual environment or pyenv is required. The script runs directly on system Python.

---

## 📂 Output Structure

```
output/
├── TutorialName.html
├── TutorialName.pdf
└── ...
```

---

## 🧰 Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### requirements.txt

```txt
requests==2.32.5
beautifulsoup4==4.14.3
tqdm==4.67.3
weasyprint==68.1
```

---

## 🖨️ WeasyPrint System Dependencies (Windows)

WeasyPrint requires GTK3 runtime on Windows.

### 1. Install GTK3 Runtime

Download and install:
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

Default install path:
```
C:\Program Files\GTK3-Runtime Win64\bin
```

### 2. Set Environment Variable

You must set `WEASYPRINT_DLL_DIRECTORIES` so WeasyPrint can locate GTK DLL files.

#### Windows CMD

```cmd
set WEASYPRINT_DLL_DIRECTORIES=C:\Program Files\GTK3-Runtime Win64\bin
```

#### PowerShell

```powershell
$Env:WEASYPRINT_DLL_DIRECTORIES="C:\Program Files\GTK3-Runtime Win64\bin"
```

⚠️ This environment variable must be set **before running the script**.

---

## 🖨️ WeasyPrint System Dependencies (Linux)

```bash
sudo apt install libcairo2 pango1.0-tools libgdk-pixbuf2.0-0 libffi-dev
```

---

## 🚀 How to Use

```bash
git clone https://github.com/cahjul/TutorialsPoint-to-PDF.git
cd TutorialsPoint-to-PDF
python TutorialsPoint-to-PDF.py
```

Follow the on screen prompts to select categories and tutorials.

---

## 🗂️ Supported Categories

- Programming Languages  
- Latest Technologies  
- Machine Learning  
- Computer Science  
- Web Development  
- Mobile Development  
- Databases  

---

## ⚙️ How It Works

1. Scan TutorialsPoint category pages  
2. Extract tutorial listings  
3. Retrieve all chapters from each tutorial  
4. Download content in parallel threads  
5. Merge chapters into a single HTML file  
6. Convert HTML into a PDF document  

---

## 📸 Screenshots

<img width="1918" height="297" alt="image" src="https://github.com/user-attachments/assets/f5d77d23-98f4-412f-b278-5ab7abe49267" />

<img width="1918" height="850" alt="image" src="https://github.com/user-attachments/assets/e9ca809c-60f0-4084-a280-06d390fba8ea" />

<img width="787" height="97" alt="image" src="https://github.com/user-attachments/assets/8647b397-752d-4a3b-803f-b83509babe94" />


---

## ⚠️ Disclaimer

This project is intended for educational and personal use only.

All tutorial content belongs to TutorialsPoint.  
Please respect the original website terms of service.

---

## 🤝 Contributing

Contributions are welcome.  
Fork the repository and submit a pull request.

---

## 👤 Credits

Project Author: Cahjul

Technical/ReadMe by: ChatGPT ❤️

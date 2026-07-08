# Python Storage Cleanup Tool

A Python-based storage management and cleanup utility that combines traditional file system operations with AI-assisted analysis using the **Groq API**. The project helps automate storage optimization through cleanup utilities, compression, decoding, trash management, and AI-powered recommendations.

---

## 🚀 Project Overview

Python Storage Cleanup Tool is a modular command-line application that helps organize and optimize disk storage. Along with standard cleanup operations, it integrates **Groq LLM** to analyze Python source files and provide intelligent cleanup suggestions.

The project demonstrates practical usage of Python for automation, filesystem management, compression, JSON processing, and AI integration.

---

# ✨ Features

- AI-powered cleanup analysis using **Groq**
- Disk cleanup utilities
- Storage optimization
- File compression
- Trash management
- Python file analysis
- File decoding utilities
- Cleanup report generation
- JSON report support
- Modular command-line utilities
- Cross-platform Python implementation

---

# 🤖 AI Integration

The project integrates the **Groq API** to analyze Python files and provide intelligent cleanup suggestions.

AI capabilities include:

- Source code analysis
- Cleanup recommendations
- Code quality suggestions
- Automation support
- JSON-based AI responses

> **Security Note:**  
> API keys are **not stored in the repository**. Configure your own `GROQ_API_KEY` as an environment variable before running AI-related utilities.

Example:

```bash
export GROQ_API_KEY=your_api_key
```

Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_api_key"
```

---

# 🛠 Technologies Used

- Python 3
- Groq API
- JSON
- File System Operations
- Environment Variables
- Standard Python Libraries

---

# 📂 Project Structure

```text
python-storage-cleanup-tool/
│
├── ai_cleanup.py
├── cleanup_ai.py
├── compressorv1.py
├── decoder.py
├── drive_cleanup.py
├── trash.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/prathameshkhedkar50-arch/python-storage-cleanup-tool.git
```

Navigate to the project

```bash
cd python-storage-cleanup-tool
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file or configure the environment variable:

```text
GROQ_API_KEY=your_api_key
```

Never commit your API key to GitHub.

---

# ▶ Usage

Run any module individually.

```bash
python drive_cleanup.py
```

```bash
python compressorv1.py
```

```bash
python cleanup_ai.py
```

```bash
python ai_cleanup.py
```

```bash
python decoder.py
```

```bash
python trash.py
```

---

# 📚 Learning Outcomes

This project demonstrates practical experience with:

- Python scripting
- AI API integration
- Groq LLM
- Environment variable management
- Filesystem automation
- JSON processing
- Storage optimization
- Compression
- Command-line application development
- Modular software design

---

# 🔮 Future Improvements

- Interactive CLI
- GUI version
- Duplicate file detection
- Large file analyzer
- Scheduled cleanup
- AI-generated cleanup reports
- Progress indicators
- Unit testing
- Logging system

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Prathamesh Khedkar**

GitHub: https://github.com/prathameshkhedkar50-arch

---

⭐ If you found this project useful, consider giving it a Star.

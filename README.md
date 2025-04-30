# EVIL LOCK Multi-Tool

![2025-04-30_23-40](https://github.com/user-attachments/assets/a8f4d151-04f2-4d59-b767-b528ff282b6a)

[![Author](https://img.shields.io/badge/Author-PYSCODES-red?style=flat-square)](https://github.com/Pyscodes-pro)
[![Instagram](https://img.shields.io/badge/Instagram-@pyscodes-red?style=flat-square&logo=instagram)](https://instagram.com/pyscodes)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A command-line multi-tool with a hacker aesthetic, combining various utilities for cryptography, network analysis, data manipulation, and system information. Built with Python and wrapped in a Bash installer script for easy setup.

---

## ✨ Features

EVIL LOCK provides a menu-driven interface for the following tools:

**🔐 Cryptography Tools:**
*   **Encrypt/Decrypt Text:** Symmetrically encrypt and decrypt text messages using a password (AES-256 via Fernet, PBKDF2 key derivation).
*   **Encrypt/Decrypt File:** Encrypt and decrypt entire files using the same strong symmetric encryption.
*   **Hash Calculator:** Calculate hashes (MD5, SHA-1, SHA-256, SHA-512) for text input or files.
*   **Password Generator:** Create strong, random passwords with customizable length and character sets.

**🌐 Network Tools:**
*   **Basic Port Scanner:** Scan a target IP or hostname for common open TCP ports or a custom range. *(Use Ethically!)*
*   **Whois Domain Lookup:** Retrieve public registration information for a domain name.
*   **DNS Record Lookup:** Query various DNS record types (A, AAAA, MX, TXT, NS, CNAME) for a domain.
*   **HTTP Header Viewer:** Fetch and display HTTP response headers from a given URL.
*   **Website Cookie Viewer:** Connect to a URL and display any cookies set by the server in the response.

**💻 Data Utilities:**
*   **Encode/Decode:** Encode and decode data using Base64 and Hexadecimal formats.

**⚙️ System Utilities:**
*   **System Information:** Display basic information about the host operating system, architecture, and Python version.
*   **List Running Processes:** Show a list of currently running processes on the local machine (PID, Username, Name).

**🚀 General:**
*   **Hacker-Style Interface:** Uses ASCII art and colorized output.
*   **Automatic Dependency Check:** The installer script checks for required Python libraries (cryptography, requests, python-whois, dnspython, psutil ) and prompts the user to install them via pip if missing.

---

## ⚠️ Disclaimer

This tool includes features (like the port scanner) that can be misused. **This software is intended for educational and ethical purposes ONLY.**
*   **DO NOT** use this tool for any illegal or malicious activities.
*   **DO NOT** scan networks or systems you do not have explicit permission to test.
*   The author (Pyscodes-pro) is **NOT responsible** for any damage or legal consequences resulting from the misuse of this tool.
*   Use at your own risk and responsibility.

---

## 📋 Prerequisites

*   A **Linux or Unix-like system** (like macOS, or Windows with WSL) is recommended due to the Bash installer script.
*   **Python 3** (version 3.6 or higher recommended).
*   **pip** (Python package installer) for Python 3.
*   **Git** (for cloning the repository).
*   An **Internet connection** (for cloning and downloading dependencies).

---

## 🛠️ Installation

1.  **Clone the repository:**
    Open your terminal and run:
    
    git clone https://github.com/Pyscodes-pro/evil-lock-multitool.git 
    # Replace with your ACTUAL repository URL 
   

2.  **Navigate to the directory:**
    
    cd evil-lock-multitool 
    #  Or whatever you named the repository directory 
    

3.  **Make the installer script executable:**
    
    **chmod +x encryptor.sh**             
   

4.  **Run the installer script:**
    
    ./encryptor.sh
    
    *   This script will first check if Python 3 and pip are available.
    *   Then, it will check for the required Python libraries (cryptography, requests,python-whois,dnspython,psutil).
    *   If any library is missing, it will ask for your permission (`y/n`) to attempt installation using 'pip'. You might need 'sudo' privileges if installing system-wide, although installing in a virtual environment is recommended for cleaner management.

---

## ▶️ Usage

Once the installation (dependency check/install) is complete, you can run the tool simply by executing the same script again from within the project directory:


./encryptor.sh

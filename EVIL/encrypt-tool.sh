#!/bin/bash

# --- Colors ---
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear

# --- ASCII Art ---
echo -e "${CYAN}"
cat << "EOF"
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⠟⠉⠀⠀⠀⠈⠙⠿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢰⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠉⠉⠛⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡶⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣶⣶⣶⣶⣶⣾⣿⣿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠛⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      
          ENCRYPT-TOOL EVIL
EOF
echo -e "${NC}"

# --- Author Info ---
echo -e "${GREEN}==============================================================${NC}"
echo -e "${YELLOW} Author    : ${CYAN}Pyscodes-pro${NC}"
echo -e "${YELLOW} Instagram : ${CYAN}https://instagram.com/pyscodes${NC}" # Change this link
echo -e "${YELLOW} GitHub    : ${CYAN}https://github.com/Pyscodes-pro${NC}"     # Change this link
echo -e "${GREEN}==============================================================${NC}"
sleep 1

# --- Dependency Check ---
echo -e "\n${YELLOW}[*] Initializing Secure Environment...${NC}"
sleep 0.5

echo -e "${YELLOW}[*] Checking System Dependencies...${NC}"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Error: python3 is not installed. Please install Python 3.${NC}"
    exit 1
fi
echo -e "${GREEN}[+] Python 3 Found.${NC}"
sleep 0.5

# Check for pip3
if ! python3 -m pip --version &> /dev/null; then
     if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}[!] Error: pip3 is not installed. Please install pip for Python 3.${NC}"
        exit 1
     else
        PIP_COMMAND="pip3"
     fi
else
    PIP_COMMAND="python3 -m pip"
fi
echo -e "${GREEN}[+] Pip Found.${NC}"
sleep 0.5

# Check for cryptography module
echo -e "${YELLOW}[*] Checking Python Cryptography Module...${NC}"
python3 -c "import cryptography" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[!] Python 'cryptography' module not found.${NC}"
    read -p "$(echo -e ${CYAN}'[?] Do you want to install it now? (y/n): '${NC})" INSTALL_CONFIRM
    if [[ "$INSTALL_CONFIRM" == "y" || "$INSTALL_CONFIRM" == "Y" ]]; then
        echo -e "${YELLOW}[*] Attempting to install 'cryptography' using pip...${NC}"
        $PIP_COMMAND install cryptography
        if [ $? -ne 0 ]; then
            echo -e "${RED}[!] Error: Failed to install 'cryptography'. Please install it manually.${NC}"
            exit 1
        else
            echo -e "${GREEN}[+] 'cryptography' module installed successfully.${NC}"
        fi
    else
        echo -e "${RED}[!] 'cryptography' module is required. Exiting.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}[+] Python 'cryptography' module found.${NC}"
fi

sleep 1
echo -e "\n${GREEN}[+] All dependencies met. Launching Core Encryptor...${NC}\n"
sleep 1.5

# --- Run Python Script ---
python3 core_encryptor.py

echo -e "\n${YELLOW}[*] Encryptor session terminated.${NC}"
exit 0


GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'


check_and_install_pkg() {
    local pkg_name="$1"
    local pkg_import_name="${2:-$pkg_name}" 
    local feature_desc="$3"

    echo -e "${YELLOW}[*] Checking Dependency: '${pkg_name}' (${feature_desc})...${NC}"
    python3 -c "import ${pkg_import_name}" &> /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}[!] Notice: Required module '${pkg_name}' is missing.${NC}"
        read -p "$(echo -e ${CYAN}'[?] Attempt automatic installation via pip? (y/n): '${NC})" INSTALL_CONFIRM
        if [[ "$INSTALL_CONFIRM" == "y" || "$INSTALL_CONFIRM" == "Y" ]]; then
            echo -e "${YELLOW}[*] Initiating installation sequence for '${pkg_name}'...${NC}"
            $PIP_COMMAND install "$pkg_name"
           
             python3 -c "import ${pkg_import_name}" &> /dev/null
             if [ $? -ne 0 ]; then
                echo -e "${RED}[!] Error: Installation failed or module still not found. Please install manually ('$PIP_COMMAND install ${pkg_name}').${NC}"
                exit 1
            else
                echo -e "${GREEN}[+] '${pkg_name}' module installed successfully.${NC}"
            fi
        else
            echo -e "${RED}[!] '${pkg_name}' module is needed for full functionality. Aborting launch.${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}[+] Module '${pkg_name}': Ready.${NC}"
    fi
     sleep 0.3 
}



clear
echo -e "${YELLOW}[*] Initializing EVIL LOCK Multi-Tool Environment...${NC}"
sleep 1

echo -e "${YELLOW}[*] Verifying System Core Components...${NC}"


if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Critical Error: Python 3 interpreter not found.${NC}"
    echo -e "${RED}[!] Please install Python 3 to proceed.${NC}"
    exit 1
fi
echo -e "${GREEN}[+] Python 3 Runtime: Detected.${NC}"
sleep 0.5


if ! python3 -m pip --version &> /dev/null; then
     if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}[!] Critical Error: pip package manager for Python 3 not found.${NC}"
        echo -e "${RED}[!] Please install pip (e.g., 'sudo apt install python3-pip' or 'sudo yum install python3-pip').${NC}"
        exit 1
     else
        PIP_COMMAND="pip3"
     fi
else
    PIP_COMMAND="python3 -m pip"
fi
echo -e "${GREEN}[+] Pip Package Manager: Detected.${NC}"
sleep 0.5

echo -e "${YELLOW}[*] Verifying Required Python Modules...${NC}"


check_and_install_pkg "cryptography" "cryptography" "Core Encryption"
check_and_install_pkg "requests" "requests" "Web Features (Cookies, Headers)"
check_and_install_pkg "python-whois" "whois" "Whois Lookup"
check_and_install_pkg "dnspython" "dns.resolver" "DNS Lookup" 
check_and_install_pkg "psutil" "psutil" "Process Listing & System Info"



sleep 1
echo -e "\n${GREEN}[+] System Check Complete. All Dependencies Satisfied.${NC}"
echo -e "${YELLOW}[*] Launching EVIL LOCK Multi-Tool Interface... Standby.${NC}\n"
sleep 1.5


python3 core_encryptor.py 

echo -e "\n${YELLOW}[*] EVIL LOCK session terminated by user.${NC}"
exit 0

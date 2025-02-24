# CyberCompass CDN Scanner (`cccdn`)

## Overview
**`cccdn`** is a CLI tool for:
- **Detecting ALL CDN targets dynamically** (no predefined list).
- **Extracting CDNs even from JavaScript-loaded content**.
- **Automating pipeline-based CDN discovery**.

---

## **🚀 One-Line Installation**
### **Linux (Debian, Ubuntu, Arch, Fedora)**
```bash
sudo curl -sSL "https://raw.githubusercontent.com/CyberCompass/CdnCompass/cdn_compass.py" -o /usr/local/bin/cccdn && sudo chmod +x /usr/local/bin/cccdn
```
### **macOS (Homebrew)**
```bash
brew install wget && wget -qO /usr/local/bin/cccdn "https://raw.githubusercontent.com/CyberCompass/CdnCompass/cdn_compass.py" && chmod +x /usr/local/bin/cccdn
```
### **macOS (Without Homebrew)**
```bash
sudo curl -sSL "https://raw.githubusercontent.com/CyberCompass/CdnCompass/cdn_compass.py" -o /usr/local/bin/cccdn && sudo chmod +x /usr/local/bin/cccdn
```

---

## **📌 Usage**
### **1️⃣ Scan a Single Website**
```bash
cccdn -u https://example.com
```
Extracts all **CDN URLs** from `https://example.com`.

### **2️⃣ Scan Multiple URLs via Pipe**
```bash
cat subdomains.httpx | cccdn > subdomains.cdns
```
Finds **CDN targets for all subdomains** and saves them to `subdomains.cdns`.

### **3️⃣ Direct File Input**
```bash
cccdn < subdomains.httpx > subdomains.cdns
```

---

## **💡 Why `cccdn`?**
✅ **Detects ANY CDN dynamically** using **WHOIS & Reverse DNS lookups**  
✅ **No predefined CDN list** → **Finds hidden providers**  
✅ **Works with JavaScript-based content** (headless browser)  
✅ **Automates CDN scanning in pipelines**  

---

🚀 **Now, `cccdn` is installable on macOS & Linux with one command!**  
Let me know if you need more refinements! 🔥

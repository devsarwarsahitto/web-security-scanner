# 🔒 Security Scanner - Advanced Web Vulnerability Scanner

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**A powerful, production-ready security toolkit for discovering exposed .env files, backup files, and common web vulnerabilities**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples) • [Disclaimer](#%EF%B8%8F-disclaimer)

</div>

---

## 👨‍💻 Author

**Sarwar Jahan Sahitto**  
GitHub: [https://github.com/devsarwarsahitto](https://github.com/devsarwarsahitto)

---

## 🎯 Features

This security scanner provides comprehensive vulnerability assessment capabilities:

### 🔍 Enumeration & Discovery
- **IP Range Scanning** - Scan entire networks using CIDR notation
- **ASN Lookup** - Enumerate targets by Autonomous System Number
- **Domain Enumeration** - Discover subdomains and related hosts
- **Multi-threaded Scanning** - Fast, efficient concurrent scanning

### 🔐 Security Checks
- **Exposed .env Files** - Detect and retrieve exposed environment configuration files
- **Backup File Detection** - Find exposed database dumps, ZIP files, and backups
- **Git Directory Exposure** - Identify exposed .git repositories
- **Admin Panel Discovery** - Locate administrative interfaces
- **Directory Listing** - Detect servers with directory browsing enabled

### 📊 Reporting & Analysis
- **JSON Reports** - Machine-readable structured output
- **Text Reports** - Human-readable detailed reports
- **Auto-save Functionality** - Automatically save discovered .env files
- **Statistics Dashboard** - Real-time scan statistics
- **Remediation Recommendations** - Actionable security advice

---

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/devsarwarsahitto/security-scanner.git
cd security-scanner
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```
Or install manually:
```bash
pip install requests dnspython ipwhois tqdm colorama beautifulsoup4
```

3. **Run the scanner**
```bash
python main.py --help
```

---

## 📖 Usage

### Basic Syntax
```bash
python main.py [TARGET_OPTIONS] [SCAN_OPTIONS] [CONFIG_OPTIONS]
```

### Target Options
| Option | Description | Example |
|--------|-------------|---------|
| `-t`, `--target` | Single target URL or IP | `-t example.com` |
| `-r`, `--ip-range` | IP range in CIDR notation | `-r 192.168.1.0/24` |
| `-a`, `--asn` | Autonomous System Number | `-a AS15169` |
| `-d`, `--domain` | Domain with subdomain enumeration | `-d example.com` |
| `-f`, `--file` | File containing target list | `-f targets.txt` |

### Scan Options
| Option | Description |
|--------|-------------|
| `--env-only` | Only scan for exposed .env files |
| `--security-only` | Only run security checks (skip .env scan) |
| `--all` | Run all scan types (default) |

### Configuration Options
| Option | Description | Default |
|--------|-------------|---------|
| `--threads` | Number of concurrent threads | 10 |
| `--timeout` | Request timeout (seconds) | 10 |
| `-o`, `--output` | Output filename prefix | `scan_YYYYMMDD_HHMMSS` |

---

## 💡 Examples

### Example 1: Scan a Single Website
```bash
python main.py -t example.com
```

### Example 2: Scan IP Range
```bash
python main.py -r 192.168.1.0/24 --threads 20
```

### Example 3: Only Check for .env Files
```bash
python main.py -t example.com --env-only
```

### Example 4: Scan Multiple Targets from File
Create a `targets.txt` file:
```
https://example1.com
https://example2.com
192.168.1.100
```

Then run:
```bash
python main.py -f targets.txt --all
```

### Example 5: Domain Enumeration with Subdomains
```bash
python main.py -d example.com --threads 15
```

### Example 6: Custom Output with Timeout
```bash
python main.py -t example.com --timeout 15 -o my_scan_report
```

---

## 📁 Output Structure

```
security-scanner/
├── scans/
│   ├── env_files/          # Retrieved .env files
│   │   ├── example_com_20241026_123456.env
│   │   └── ...
│   └── reports/            # Scan reports
│       ├── scan_20241026_123456.json
│       └── scan_20241026_123456.txt
```

### Sample Report Output

**JSON Report** (`scans/reports/scan_YYYYMMDD_HHMMSS.json`)
```json
{
  "scan_info": {
    "scan_name": "scan_20241026_123456",
    "timestamp": "2024-10-26T12:34:56",
    "author": "Sarwar Jahan Sahitto",
    "version": "1.0.0"
  },
  "statistics": {
    "total_targets": 5,
    "vulnerable_targets": 2,
    "env_files_found": 1,
    "git_exposed": 1,
    "backup_files_found": 0,
    "admin_panels_found": 1
  },
  "vulnerabilities": [...]
}
```

**Text Report** (`scans/reports/scan_YYYYMMDD_HHMMSS.txt`)
- Detailed vulnerability descriptions
- Remediation recommendations
- Full scan statistics

---

## 🛡️ Vulnerability Types Detected

### 1. Exposed .env Files
Detects environment configuration files containing:
- Database credentials
- API keys and secrets
- AWS credentials
- Application secrets
- SMTP/Email configurations

### 2. Exposed Git Directories
Identifies publicly accessible `.git` folders that may expose:
- Source code
- Commit history
- Configuration files
- Developer information

### 3. Backup Files
Finds exposed backup files:
- Database dumps (.sql)
- Archive files (.zip, .tar.gz)
- Configuration backups (.bak)

### 4. Admin Panels
Discovers administrative interfaces:
- `/admin`, `/administrator`
- WordPress admin panels
- phpMyAdmin
- cPanel/WHM interfaces
- Custom admin portals

### 5. Directory Listing
Detects servers with directory browsing enabled

---

## 🔧 Configuration

Edit `config.py` to customize:
- Default timeout values
- Number of threads
- User-agent strings
- Scan paths and patterns
- Output directories

---

## 📊 Features Comparison

| Feature | Security Scanner | Similar Tools |
|---------|------------------|---------------|
| Multi-threaded Scanning | ✅ | ✅ |
| .env File Detection | ✅ | ❌ |
| Auto-save .env Files | ✅ | ❌ |
| IP Range Scanning | ✅ | Limited |
| Subdomain Enumeration | ✅ | Limited |
| JSON/Text Reports | ✅ | Text Only |
| Progress Bars | ✅ | ❌ |
| Colored Output | ✅ | Limited |
| Production Ready | ✅ | ❌ |

---

## 🎨 Screenshots

When you run the scanner, you'll see:
- Colorful ASCII banner with author credits
- Real-time progress bars
- Color-coded vulnerability alerts
- Detailed scan statistics
- Professional reports

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY**

This tool is designed for:
- Security professionals conducting authorized penetration tests
- Website owners auditing their own infrastructure
- Educational purposes in controlled environments

**IMPORTANT:**
- Always obtain written permission before scanning any systems
- Unauthorized scanning may be illegal in your jurisdiction
- The author is NOT responsible for misuse or damage caused by this tool
- Use responsibly and ethically

---

## 🙏 Acknowledgments

- Built with Python and various open-source libraries
- Inspired by the need for comprehensive .env file detection
- Developed to help security professionals protect web applications

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Sarwar Jahan Sahitto](https://github.com/devsarwarsahitto)

---

## 🌟 Star History

If you find this tool useful, please give it a ⭐ on GitHub!

---

<div align="center">

**Developed with ❤️ by [Sarwar Jahan Sahitto](https://github.com/devsarwarsahitto)**

[⬆ Back to Top](#-security-scanner---advanced-web-vulnerability-scanner)

</div>

Here is a comprehensive README file based on the current contents of your GitHub repository:

markdown

# Tools

A collection of Python tools for various network and forensic analysis tasks, including DNS checks, email spoof detection, keylogging, port scanning, and more.

## Table of Contents

- [Tools Overview](#tools-overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Keylogger](#keylogger)
  - [Backup Files](#backup-files)
  - [Directory Buster](#directory-buster)
  - [Email Spoof Detection](#email-spoof-detection)
  - [File Checker](#file-checker)
  - [Malware Hash Checker](#malware-hash-checker)
  - [Network Checker](#network-checker)
  - [Ping Sweep](#ping-sweep)
  - [Server Information Gatherer](#server-information-gatherer)
  - [Domain Squatter](#domain-squatter)
  - [SSH Brute Force](#ssh-brute-force)
  - [Subdomain Enumeration](#subdomain-enumeration)
  - [WiFi Scanner](#wifi-scanner)
- [Contributing](#contributing)
- [License](#license)

## Tools Overview

This repository contains various Python scripts designed for network and forensic analysis:

- **keylogger.py**: Logs keystrokes for monitoring purposes.
- **bkup-files.py**: Backs up specified files or directories.
- **dir-buster.py**: Enumerates directories and files on web servers.
- **email-spoof-det.py**: Detects potential email spoofing by analyzing SPF and DMARC records.
- **file-chk.py**: Checks files for hidden data and metadata.
- **malware-hash-chk.py**: Checks files against known malware hashes.
- **net-check.py**: Performs network checks and diagnostics.
- **ping-sweep2.py**: Performs a ping sweep to identify active hosts in a network.
- **server_info_gatherer2.py**: Gathers detailed information about a server.
- **squatter3.py**: Detects potential domain squatters.
- **ssh-brute.py**: Attempts to brute force SSH credentials.
- **subdomain-enum.py**: Enumerates subdomains for a given domain.
- **wifi-scanner.py**: Scans for available WiFi networks.

## Requirements

The scripts require the following Python packages:

- `requests`
- `dnspython`
- `python-whois`
- `pynput`
- `selenium`
- `python-magic`
- `subprocess`
- `hashlib`

Install the required packages using the following command:

```bash
pip install -r requirements.txt

Installation

    Clone the repository:

bash

git clone https://github.com/brkn404/tools.git
cd tools

    Install the dependencies:

bash

pip install -r requirements.txt

Usage
Keylogger

Description: Logs keystrokes for monitoring purposes.

Usage:

bash

sudo python keylogger.py

The key logs will be saved in key_log.txt.
Backup Files

Description: Backs up specified files or directories.

Usage:

bash

python bkup-files.py <source_path> <destination_path>

Example:

bash

python bkup-files.py /path/to/source /path/to/backup

Directory Buster

Description: Enumerates directories and files on web servers.

Usage:

bash

python dir-buster.py <target_url>

Example:

bash

python dir-buster.py http://example.com

Email Spoof Detection

Description: Detects potential email spoofing by analyzing SPF and DMARC records.

Usage:

bash

python email-spoof-det.py

You will be prompted to enter the target domain.
File Checker

Description: Checks files for hidden data and metadata.

Usage:

bash

python file-chk.py <file_path>

Example:

bash

python file-chk.py /path/to/file

Malware Hash Checker

Description: Checks files against known malware hashes.

Usage:

bash

python malware-hash-chk.py <file_path>

Example:

bash

python malware-hash-chk.py /path/to/file

Network Checker

Description: Performs network checks and diagnostics.

Usage:

bash

python net-check.py

You will be prompted to enter the target domain or IP address.
Ping Sweep

Description: Performs a ping sweep to identify active hosts in a network.

Usage:

bash

python ping-sweep2.py <network_prefix>

Example:

bash

python ping-sweep2.py 192.168.1

Server Information Gatherer

Description: Gathers detailed information about a server.

Usage:

bash

python server_info_gatherer2.py

You will be prompted to enter the target domain.
Domain Squatter

Description: Detects potential domain squatters.

Usage:

bash

python squatter3.py <target_domain>

Example:

bash

python squatter3.py example.com

SSH Brute Force

Description: Attempts to brute force SSH credentials.

Usage:

bash

python ssh-brute.py <target_ip> <username_list> <password_list>

Example:

bash

python ssh-brute.py 192.168.1.1 usernames.txt passwords.txt

Subdomain Enumeration

Description: Enumerates subdomains for a given domain.

Usage:

bash

python subdomain-enum.py <target_domain>

Example:

bash

python subdomain-enum.py example.com

WiFi Scanner

Description: Scans for available WiFi networks.

Usage:

bash

python wifi-scanner.py

Contributing

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

    Fork the repository.
    Create a new branch (git checkout -b feature-branch).
    Make your changes.
    Commit your changes (git commit -am 'Add new feature').
    Push to the branch (git push origin feature-branch).
    Create a new Pull Request.



# LogSync | Universal Log Processor

![Log Tool](https://img.shields.io/badge/Purpose-Log%20Processor-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## Parse, Filter & Analyze Any Log Format

LogSync processes logs from any source - servers, applications, containers - and gives you the information you need.

**Works with:**
- Apache/Nginx access logs
- Application logs (JSON, plain text)
- System logs (syslog, journald)
- Docker & Kubernetes logs
- Custom log formats

---

## Features

- 📄 **Multi-format** - Auto-detect log formats
- 🔍 **Powerful filtering** - Filter by level, time, keywords
- 📊 **Statistics** - Generate insights from log data
- 🔄 **Transform** - Convert between formats
- ⚡ **Stream processing** - Handle massive log files
- 🎯 **Custom parsers** - Define your own patterns

---

## Installation

```bash
pip install logsync

# Or from source
git clone https://github.com/simplestar-992/logsync.git
cd logsync
pip install -e .
```

---

## Usage

```bash
# Tail and filter
logsync tail /var/log/nginx/access.log --level error

# Search logs
logsync search /var/log/app.log -pattern "Exception"

# Statistics
logsync stats /var/log/nginx/access.log

# Transform format
logsync convert app.jsonl -to csv -output app.csv

# Real-time monitoring
logsync monitor /var/log/syslog --alert "ERROR"
```

---

## Examples

```bash
# Find errors in JSON logs
logsync search app.log -pattern "error" -format json

# Monitor Docker logs in real-time
docker logs -f container | logsync --format docker

# Generate report
logsync report /var/log/nginx/access.log -o report.html

# Time-based filtering
logsync search app.log --since "2024-01-01" --until "2024-01-31"
```

---

## Output Formats

| Format | Description |
|--------|-------------|
| `text` | Plain text (default) |
| `json` | JSON lines |
| `csv` | CSV table |
| `table` | Formatted table |
| `html` | HTML report |

---

## License

MIT © 2024 [simplestar-992](https://github.com/simplestar-992)

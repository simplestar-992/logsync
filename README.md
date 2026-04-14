# LogSync - Universal Log Processor

**Parse, stream, filter, and analyze any log format instantly**

LogSync automatically detects and parses JSON, Apache/Nginx, syslog, and custom timestamped logs with zero configuration.

## Features

- **Auto-detection** - Detects log format automatically
- **Multi-format support** - JSON, Apache/Nginx, Syslog, Simple timestamps
- **Real-time streaming** - Tail -f with automatic formatting
- **Powerful filtering** - Filter by level, source, or search term
- **Statistics** - Get insights about your log files
- **Color output** - Easy to read in terminal

## Installation

```bash
# Quick install
pip install logsync

# Or run directly
python3 logsync.py /path/to/logs
```

## Usage

```bash
# Process and display logs
logsync access.log

# Stream with follow mode
logsync -f /var/log/nginx/access.log

# Filter by level
logsync --level ERROR /var/log/app.log

# JSON output
logsync --json /var/log/app.log

# Show statistics
logsync --stats /var/log/app.log

# Combine options
logsync -f --level WARNING /var/log/app.log
```

## Supported Formats

| Format | Example |
|--------|---------|
| JSON | `{"timestamp":"2024-01-01","level":"INFO","message":"Hello"}` |
| Apache/Nginx | `192.168.1.1 - - [01/Jan/2024:00:00:00 +0000] "GET /api HTTP/1.1" 200 123` |
| Syslog | `Jan 1 00:00:00 hostname service[pid]: message` |
| Simple | `2024-01-01 12:00:00 INFO message here` |

## Examples

```bash
# Watch errors in real-time
logsync -f --level ERROR /var/log/app/error.log

# Find specific patterns
logsync --search "database" /var/log/app.log

# Generate report
logsync --stats --json /var/log/access.log > report.json

# Combine with other tools
logsync --level ERROR /var/log/nginx/access.log | grep "192.168"
```

## License

MIT

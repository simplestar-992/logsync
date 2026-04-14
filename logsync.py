#!/usr/bin/env python3
"""LogSync - Universal Log Processor"""

import argparse
import json
import re
import sys
import time
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import collections

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

@dataclass
class LogEntry:
    timestamp: Optional[str]
    level: Optional[str]
    source: Optional[str]
    message: str
    raw: str
    line_number: int
    parsed_fields: Dict[str, str]

class LogPattern:
    def parse(self, line: str, line_num: int) -> Optional[LogEntry]:
        raise NotImplementedError

class JSONLogPattern(LogPattern):
    def parse(self, line: str, line_num: int) -> Optional[LogEntry]:
        try:
            data = json.loads(line)
            return LogEntry(
                timestamp=data.get("timestamp") or data.get("time"),
                level=data.get("level") or data.get("severity") or "INFO",
                source=data.get("source") or data.get("service"),
                message=data.get("message") or str(data),
                raw=line,
                line_number=line_num,
                parsed_fields={k: str(v) for k, v in data.items()}
            )
        except:
            return None

class SimpleLogPattern(LogPattern):
    pattern = re.compile(r'(?P<ts>\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})?\s*(?P<level>\w+)?\s*(?P<msg>.*)')
    def parse(self, line: str, line_num: int) -> Optional[LogEntry]:
        m = self.pattern.match(line)
        if m:
            g = m.groupdict()
            return LogEntry(
                timestamp=g.get("ts"),
                level=g.get("level") or "INFO",
                source=None,
                message=g.get("msg") or line,
                raw=line,
                line_number=line_num,
                parsed_fields=g
            )
        return None

class LogSync:
    def __init__(self):
        self.patterns = [JSONLogPattern(), SimpleLogPattern()]
        self.stats = {"total": 0, "parsed": 0, "by_level": collections.Counter()}

    def parse_line(self, line: str, num: int) -> LogEntry:
        for p in self.patterns:
            e = p.parse(line, num)
            if e:
                self.stats["parsed"] += 1
                self.stats["by_level"][e.level or "?"] += 1
                return e
        self.stats["total"] += 1
        return LogEntry(None, None, None, line, line, num, {})

    def process(self, path: str, limit: int = None):
        entries = []
        self.stats["total"] = 0
        with open(path) as f:
            for i, line in enumerate(f, 1):
                line = line.rstrip()
                if line.strip():
                    entries.append(self.parse_line(line, i))
                if limit and len(entries) >= limit:
                    break
        return entries

    def stream(self, path: str):
        pos = os.path.getsize(path) if os.path.exists(path) else 0
        while True:
            try:
                with open(path) as f:
                    if pos: f.seek(pos)
                    for line in f:
                        line = line.rstrip()
                        if line.strip():
                            yield self.parse_line(line, self.stats["total"]+1)
                    pos = f.tell()
                time.sleep(0.5)
            except KeyboardInterrupt:
                break
            except FileNotFoundError:
                time.sleep(1)
                pos = 0

def main():
    p = argparse.ArgumentParser(description="LogSync - Universal Log Processor")
    p.add_argument("file", help="Log file")
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--stats", action="store_true", help="Show stats")
    p.add_argument("--follow", "-f", action="store_true", help="Follow mode")
    p.add_argument("--level", help="Filter by level")
    args = p.parse_args()

    sync = LogSync()
    entries = sync.process(args.file)

    if args.follow:
        for e in sync.stream(args.file):
            if args.level and e.level != args.level.upper():
                continue
            ts = e.timestamp or ""
            lvl = (e.level or "??").ljust(8)
            print(f"{ts} {lvl} {e.message}")
    else:
        for e in entries:
            if args.level and e.level != args.level.upper():
                continue
            if args.json:
                print(json.dumps(asdict(e)))
            else:
                ts = e.timestamp or ""
                lvl = (e.level or "??").ljust(8)
                print(f"{ts} {lvl} {e.message}")

    if args.stats:
        print("\n📊 Stats:", file=sys.stderr)
        print(f"   Total: {len(entries)}", file=sys.stderr)
        print(f"   Parsed: {sync.stats['parsed']}", file=sys.stderr)
        for lvl, cnt in sync.stats["by_level"].most_common():
            print(f"   {lvl}: {cnt}", file=sys.stderr)

if __name__ == "__main__":
    main()
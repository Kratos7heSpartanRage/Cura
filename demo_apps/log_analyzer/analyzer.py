from parser import parse_logs
from utils.formatter import format_report

def analyze_logs(file_path):
    lines = parse_logs(file_path)
    counts = {"INFO": 0, "ERROR": 0, "WARNING": 0}

    for line in lines:
        for level in counts:
            if level in line:
                counts[level] += 1

    return format_report(counts)

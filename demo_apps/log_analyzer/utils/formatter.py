def format_report(counts):
    report = "Log Summary:\n"
    for level, count in counts.items():
        report += f"{level}: {count}\n"
    return report

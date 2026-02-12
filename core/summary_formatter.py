# core/summary_formatter.py

import re
from typing import Dict, List, Optional

def extract_core_summary(raw_summary: str) -> str:
    """
    Extract the essential information from LLM-generated file summaries.
    Removes markdown, section headers, and redundant formatting.
    Returns a clean, concise summary.
    """
    if not raw_summary:
        return ""
    
    # Remove markdown headers (###, ===, ---)
    text = re.sub(r'^#+.*$', '', raw_summary, flags=re.MULTILINE)
    text = re.sub(r'^=+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^-+$', '', text, flags=re.MULTILINE)
    
    # Remove markdown formatting
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # italic
    text = re.sub(r'`([^`]+)`', r'\1', text)        # inline code
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # links
    
    # Remove list markers
    text = re.sub(r'^[\*\-\+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)
    
    # Remove section labels
    text = re.sub(r'(?i)^(role|purpose|functionality|key components?):?\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'(?i)^(file|module|class|function):?\s*', '', text, flags=re.MULTILINE)
    
    # Extract the actual content - focus on role and main functionality
    lines = text.split('\n')
    useful_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip lines that are just punctuation or single words
        if len(line.split()) < 2:
            continue
            
        # Skip lines that are still markdown artifacts
        if re.match(r'^[\s=*\-_]+$', line):
            continue
            
        useful_lines.append(line)
    
    # Join and clean up whitespace
    text = ' '.join(useful_lines)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def compress_summary(text: str, max_words: int = 50) -> str:
    """
    Compress a summary to a maximum word count.
    Preserves the most important information first.
    """
    if not text:
        return ""
    
    words = text.split()
    if len(words) <= max_words:
        return text
    
    # Take first N words and add ellipsis
    return ' '.join(words[:max_words]) + "..."


def format_file_summary(summary_dict: Dict) -> Optional[Dict]:
    """
    Format a single file summary into a clean, compressed version.
    """
    if not summary_dict or not summary_dict.get("summary"):
        return None
    
    file_name = summary_dict.get("file", "")
    raw_summary = summary_dict.get("summary", "")
    
    # Extract core information
    clean_summary = extract_core_summary(raw_summary)
    
    # Compress to reasonable length
    compressed_summary = compress_summary(clean_summary, max_words=40)
    
    return {
        "file": file_name,
        "summary": compressed_summary
    }


def format_summaries_batch(summaries: List[Dict], max_files: int = 10) -> List[Dict]:
    """
    Format multiple file summaries in batch.
    Prioritizes Python files and entry points.
    """
    formatted = []
    
    # Separate Python files first
    python_summaries = [s for s in summaries if s.get("file", "").endswith(".py")]
    other_summaries = [s for s in summaries if not s.get("file", "").endswith(".py")]
    
    # Sort Python files - prioritize potential entry points
    def is_entry_point(filename):
        return any(filename.endswith(ep) for ep in ["main.py", "__main__.py", "app.py", "cli.py"])
    
    python_summaries.sort(key=lambda x: (not is_entry_point(x.get("file", "")), x.get("file", "")))
    
    # Process Python files first
    for summary in python_summaries:
        formatted_summary = format_file_summary(summary)
        if formatted_summary:
            formatted.append(formatted_summary)
        
        if len(formatted) >= max_files:
            break
    
    # If we still have room, add other files
    if len(formatted) < max_files:
        for summary in other_summaries:
            if len(formatted) >= max_files:
                break
                
            formatted_summary = format_file_summary(summary)
            if formatted_summary:
                formatted.append(formatted_summary)
    
    return formatted
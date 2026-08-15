import os
import re

# Regex patterns to match subtitle index numbers and timestamps
timestamp_pattern = re.compile(
    r"^\d{1,2}:\d{2}:\d{2}[,\.]\d{3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[,\.]\d{3}"
)
index_pattern = re.compile(r"^\d+$")

for filename in os.listdir("."):
    if filename.endswith(".srt"):
        txt_filename = os.path.splitext(filename)[0] + ".txt"

        with open(filename, "r", encoding="utf-8", errors="ignore") as infile:
            lines = infile.readlines()

        clean_lines = []
        for line in lines:
            stripped = line.strip()
            # Skip empty lines, sequence numbers, and timestamp lines
            if not stripped:
                continue
            if index_pattern.match(stripped):
                continue
            if timestamp_pattern.match(stripped):
                continue

            # Remove HTML-style formatting tags like <i> or <font> if present
            clean_text = re.sub(r"<[^>]+>", "", stripped)
            clean_lines.append(clean_text)

        # Write clean text out to .txt
        with open(txt_filename, "w", encoding="utf-8") as outfile:
            outfile.write("\n".join(clean_lines))

print("Conversion complete!")
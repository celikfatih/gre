import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'ingestion', 'src'))
from cleaners.header_footer_cleaner import HeaderFooterCleaner

# Load the file
with open('output/cleaned_texts/1.txt', 'r') as f:
    content = f.read()

# Enable logging to see what matches
import logging

cleaner = HeaderFooterCleaner(min_repeats=3)
cleaned = cleaner.clean(content)

print(f"Cleaned content type: {type(cleaned)}")
print("--- PAGE 2 CHECK ---")
parts = cleaned.split('=== PAGE 2 ===')
if len(parts) > 1:
    before = parts[0][-50:]
    after = parts[1][:100]
    print(f"Ends of Page 1: {repr(before)}")
    print(f"Start of Page 2: {repr(after)}")
else:
    print("Page 2 marker not found")



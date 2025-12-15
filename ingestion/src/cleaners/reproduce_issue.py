import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'ingestion', 'src'))
from cleaners.header_footer_cleaner import HeaderFooterCleaner

# Mock text mimicking the user's issue
# We need enough pages so the header is detected as frequent (min_repeats=3 by default)
header = "S. Ajorloo et al. AppliedSoftComputing 162(2024)111805"
page_break = "\n=== PAGE {} ===\n"

# Page 1, 2, 3 have clean headers
p1 = f"{page_break.format(1)}{header}\nSome content."
p2 = f"{page_break.format(2)}{header}\nMore content."
p3 = f"{page_break.format(3)}{header}\nPage 3 content."

# Page 4 has header mixed with text
p4 = f"{page_break.format(4)}{header} application where traditional... ignored.\nContent continue."

# Page 5 clean
p5 = f"{page_break.format(5)}{header}\nPage 5."

full_text = p1 + p2 + p3 + p4 + p5

cleaner = HeaderFooterCleaner(min_repeats=3)
cleaned = cleaner.clean(full_text)

print("Original P4 line:")
print(f"{header} application where traditional... ignored.")
print("-" * 20)
print("Cleaned Output around Page 4:")

# Extract page 4 content (approx)
parts = cleaned.split("=== PAGE 4 ===")
if len(parts) > 1:
    p4_cleaned = parts[1].split("=== PAGE 5 ===")[0].strip()
    print(p4_cleaned)

    # Check if header is removed
    if header in p4_cleaned:
        print("\nFAIL: Header still present in Page 4 content.")
    else:
        print("\nSUCCESS: Header removed from Page 4 content.")

    # Check if content is preserved
    if "application where traditional... ignored." in p4_cleaned:
        print("SUCCESS: Content preserved.")
    else:
        print("FAIL: Content lost.")
else:
    print("Could not find Page 4 in output.")

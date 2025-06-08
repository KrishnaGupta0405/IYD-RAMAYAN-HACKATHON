# Yes we made another code for the final output, so what this code does is
# As said by our mentor, that the values for which you were unable to extract value just put null for that
# Thst's it, from the part2.py generated file it takes that as input, and put 'Null' in English translation col. for the missing vereses

import pandas as pd
import re

# Load your input CSV file
input_file = 'Part2_Cleaned_Output_ordered.csv'
df = pd.read_csv(input_file)

# Strip and normalize column names
df.columns = [col.strip() for col in df.columns]

# Function to extract integer verse numbers from entries like "92,93a"
def extract_verse_nums(verse_str):
    parts = re.findall(r'\d+', str(verse_str))
    return set(map(int, parts))

# Collect output rows
output_rows = []

# Group by Book and Chapter
grouped = df.groupby(['Book Name', 'Chapter Number'], sort=False)

for (book, chapter), group in grouped:
    seen_verses = set()
    new_rows = []

    # Collect all actual verse numbers
    for _, row in group.iterrows():
        verse_str = row['Verse Number']
        verse_nums = extract_verse_nums(verse_str)
        seen_verses.update(verse_nums)

    # Insert missing verse rows
    max_verse = max(seen_verses) if seen_verses else 0
    for v in range(1, max_verse + 1):
        if v not in seen_verses:
            new_rows.append({
                'Book Name': book,
                'Chapter Number': chapter,
                'Verse Number': str(v),
                'English Translation': "Null"
            })

    # Merge original group + inserted rows while keeping order
    idx = 0
    for _, row in group.iterrows():
        # Insert all missing verses that should come before this row
        current_verses = extract_verse_nums(row['Verse Number'])
        insert_before = [r for r in new_rows if int(r['Verse Number']) < min(current_verses)]
        for r in insert_before:
            output_rows.append(r)
            new_rows.remove(r)
        # Append the actual row
        output_rows.append(row)

    # Add any remaining inserted rows at the end of chapter
    output_rows.extend(new_rows)

# Create final DataFrame
final_df = pd.DataFrame(output_rows, columns=df.columns)

# Save to output
final_df.to_csv("part3_output.csv", index=False)
print("✅ Missing verses filled. Output saved to 'part1_output.csv'")

import csv
from datetime import datetime
import os

csv_file = 'Todo.csv'

print("CSV File Analysis")
print("=" * 50)

# Get basic file info
file_size = os.path.getsize(csv_file)
print(f"File size: {file_size:,} bytes ({file_size/1024:.2f} KB)")

# Read and analyze CSV structure
print("\nAnalyzing CSV structure...")
print("-" * 50)

with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
    # Read first few raw lines
    f.seek(0)
    print("\nFirst 3 raw lines:")
    for i in range(3):
        line = f.readline()
        print(f"Line {i+1}: {line[:200]}...")  # Show first 200 chars
    
    # Reset and use csv reader
    f.seek(0)
    reader = csv.reader(f)
    
    # Get headers
    headers = next(reader)
    print(f"\nColumns detected ({len(headers)}): {headers}")
    
    # Read sample rows
    sample_rows = []
    for i, row in enumerate(reader):
        if i < 5:
            sample_rows.append(row)
        if i >= 1000:  # Stop after 1000 rows for analysis
            break
    
    total_rows = i + 1
    
    print(f"\nTotal rows analyzed: {total_rows}")
    print(f"\nSample data (first 3 rows):")
    print("-" * 50)
    
    for idx, row in enumerate(sample_rows[:3]):
        print(f"\nRow {idx + 1}:")
        for i, (header, value) in enumerate(zip(headers, row)):
            # Truncate long values for display
            display_value = value[:100] + "..." if len(value) > 100 else value
            print(f"  {header}: {display_value}")
    
    # Analyze column content
    f.seek(0)
    reader = csv.DictReader(f)
    
    column_analysis = {col: {"samples": [], "max_length": 0, "has_values": 0} for col in headers}
    
    for i, row in enumerate(reader):
        if i >= 100:  # Analyze first 100 rows
            break
        for col in headers:
            if col in row and row[col]:
                column_analysis[col]["has_values"] += 1
                column_analysis[col]["max_length"] = max(column_analysis[col]["max_length"], len(row[col]))
                if len(column_analysis[col]["samples"]) < 3:
                    column_analysis[col]["samples"].append(row[col][:100])
    
    print("\nColumn Analysis:")
    print("-" * 50)
    for col, data in column_analysis.items():
        print(f"\n{col}:")
        print(f"  Non-empty values: {data['has_values']}/100")
        print(f"  Max length: {data['max_length']} chars")
        print(f"  Samples: {data['samples'][:2]}")
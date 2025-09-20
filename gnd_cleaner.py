import json
import csv

def clean_gnd_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_records = []
    
    for record in data:
        # Remove 'gnd:' prefix from code
        full_code = record.get('Code', '').strip()
        gnd_id = full_code[4:] if full_code.startswith('gnd:') else full_code
        
        # Get German name
        german_name = record.get('Name', '').strip()
        
        # Join related subjects
        related_subjects = record.get('Related Subjects', [])
        related_text = ' | '.join([str(rel).strip() for rel in related_subjects if rel]) if related_subjects else ''
        
        if gnd_id and german_name:
            cleaned_records.append({
                'gnd_id': gnd_id,
                'german_name': german_name,
                'related_subjects': related_text
            })
    
    return cleaned_records

def save_to_csv(records, output_file):
    fieldnames = ['gnd_id', 'german_name', 'related_subjects']
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

def main():
    input_file = 'data/GND-Subjects-tib-core.json'
    output_file = 'gnd_clean.csv'
    
    records = clean_gnd_data(input_file)
    save_to_csv(records, output_file)
    
    print(f"Processed {len(records)} records - {output_file}")

if __name__ == '__main__':
    main()
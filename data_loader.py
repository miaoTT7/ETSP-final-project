import os
import json
import pandas as pd

def load_and_clean_papers(base_dir="train", language="en"):
    papers = []
    
    for root, _, files in os.walk(base_dir):
        if not root.endswith(language):
            continue
      
        for file in files:
            if not file.endswith('.jsonld'):
                continue
                
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Find main document entity in @graph array
                    graph = data.get('@graph', [])
                    main_entity = None
                    for item in graph:
                        if any(key in item for key in ['title', 'dc:title', 'dcterms:title']):
                            main_entity = item
                            break
                    
                    if not main_entity:
                        continue
                    
                    # Extract field value with fallback options
                    def get_field_value(entity, field_names):
                        for field in field_names:
                            if field in entity:
                                value = entity[field]
                                if isinstance(value, list):
                                    for v in value:
                                        if isinstance(v, str) and v.strip():
                                            return v.strip()
                                        elif isinstance(v, dict) and '@value' in v:
                                            return str(v['@value']).strip()
                                elif isinstance(value, dict) and '@value' in value:
                                    return str(value['@value']).strip()
                                elif isinstance(value, str):
                                    return value.strip()
                                else:
                                    return str(value).strip()
                        return ''
                    
                    # Extract subject IDs from graph
                    subjects = []
                    for item in graph:
                        if '@id' in item and item['@id'].startswith('gnd:'):
                            subjects.append(item['@id'].replace('gnd:', ''))
                    
                    # Check main entity for additional subjects
                    subject_fields = ['subject', 'dc:subject', 'dcterms:subject']
                    for field in subject_fields:
                        if field in main_entity:
                            subject_data = main_entity[field]
                            if isinstance(subject_data, list):
                                for s in subject_data:
                                    if isinstance(s, dict) and '@id' in s:
                                        subjects.append(s['@id'].replace('gnd:', ''))
                    
                    paper = {
                        'id': main_entity.get('@id', data.get('@id', '')),
                        'title': get_field_value(main_entity, ['title', 'dc:title', 'dcterms:title']),
                        'abstract': get_field_value(main_entity, ['abstract', 'dc:description', 'dcterms:abstract', 'description']),
                        'subjects': ','.join(list(set(subjects)))
                    }
                    
                    if paper['title']:
                        papers.append(paper)
                    
            except Exception:
                continue
    
    return pd.DataFrame(papers)

if __name__ == "__main__":
    df = load_and_clean_papers(base_dir="train", language="en")
    df.to_csv("tibkat_english_papers.csv", index=False, encoding='utf-8')
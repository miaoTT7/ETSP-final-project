# ETSP-final-project: GND Subject Tagging & References Recommendation
A project for retrieving and automatically matching GND subjects from TIB core, and related references recommendation.

## Dataset
All data is officially provided by the LLMs4Subjects shared task:
- **GND Subject Taxonomy**: `GND-Subjects-tib-core.json` 
- **TIBKAT Technical Records**: `TIBKAT/tib-core-subjects/` dataset

## Data Processing
We have successfully cleaned and prepared the English subset of the data:
  Filtered and loaded **English papers** from the TIBKAT collection
  Extracted key fields: `title`, `abstract`, and associated `GND subject IDs`
  Generated cleaned dataset: `tibkat_english_papers.csv`

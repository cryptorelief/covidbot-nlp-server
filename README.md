# NLP Server Instructions

- Model should be available at [root]/models/model_dir (example: [root]/models/spacy_model_v2)
    - This directory should contain the various pipeline directories (ner, entity_ruler, textcat, etc), the config files (config.cfg, meta.json) and the tokenizer binary file
    - The model is hosted at https://drive.google.com/file/d/1ChUpUtiMrYErolTv4Me5B5E7-Mw7_rUJ/view?usp=sharing temporarily till a better solution is found
- Requirements:
    - Python 3.8+
    - Flask 2.0.2+
    - Spacy 3.0.6+
    - and dependants of above

# The api endpoints
- `/process`
TBD


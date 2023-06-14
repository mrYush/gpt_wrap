tax_code_schema = {
    "class": "TaxCode",
    "description": "tax code with articles",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
            "model": "ada",
            "modelVersion": "002",
            "type": "text",
            "vectorizeClassName": True
        }
    },
    "properties": [
        {
            "name": "paragraph",
            "description": "paragraph",
            "dataType": ["string"]
        },
        {
            "name": "subparagraph",
            "description": "subparagraph",
            "dataType": ["string"]
        },
        {
            "name": "title",
            "description": "title",
            "dataType": ["string"]
        },
        {
            "name": "content",
            "description": "content",
            "dataType": ["text"],
            "moduleConfig": {"text2vec-openai": {"skip": True}}
        }
    ]
}

all_schemes = [tax_code_schema, ]

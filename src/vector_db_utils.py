import numpy as np
import pandas as pd
import weaviate

from embeddings_utils import TextToEmbedings
from settings import OPENAI_TOKEN


def set_schema():
    '''
    function to set database schema
    Returns
    -------

    '''
    client = weaviate.Client(
        url="http://localhost:8080",
        additional_headers={
            "X-OpenAI-Api-Key": OPENAI_TOKEN
        }
    )

    print('weaviate client is ready:', client.is_ready())
    client.schema.delete_all()
    client.schema.get()

    article_schema = {
        "class": "Article",
        "description": "A collection of articles",
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            "text2vec-openai": {
                "model": "ada",
                "modelVersion": "002",
                "type": "text"
            }
        },
        "properties": [
            {
                "name": "title",
                "description": "Title of the article",
                "dataType": ["string"]
            },
            {
                "name": "content",
                "description": "Contents of the article",
                "dataType": ["text"],
                "moduleConfig": {"text2vec-openai": {"skip": True}}
            }
        ]
    }

    # add the Article schema
    client.schema.create_class(article_schema)
    print(client.schema.get())


def load_embeddings_to_base(article_df: pd.DataFrame):
    '''
    function to write database with texts and embeddings for them

    Parameters
    ----------
    article_df: dataframe that consists of texts and embeddings for them. Mandatory columns: file_path, text, embeddings

    Returns None
    -------

    '''
    client = weaviate.Client(
        url="http://localhost:8080",
        additional_headers={
            "X-OpenAI-Api-Key": OPENAI_TOKEN
        }
    )

    client.batch.configure(
        batch_size=100,
        dynamic=True,
        timeout_retries=3,
    )

    counter = 0
    with client.batch as batch:
        for k, v in article_df.iterrows():
            # print update message every 100 objects
            if counter % 100 == 0:
                print(f"Import {counter} / {len(article_df)} ")

            properties = {
                "title": v["file_path"],
                "content": v["text"]
            }

            vector = v["embeddings"]

            batch.add_data_object(properties, "Article", None, vector)
            counter = counter + 1

    print(f"Importing ({len(article_df)}) Articles complete")


def query(input_text: str, k: int):
    '''

    Parameters
    ----------
    input_text: text to query
    k: how many results will be returned

    Returns
    -------

    '''

    client = weaviate.Client(
        url="http://localhost:8080",
        additional_headers={
            "X-OpenAI-Api-Key": OPENAI_TOKEN
        }
    )

    tte = TextToEmbedings(max_cost_to_encode=1)
    test_emb, _ = tte.len_safe_get_embedding(input_text)
    input_embedding = np.array(test_emb)
    vec = {"vector": input_embedding}
    result = client \
        .query.get(class_name='Article', properties='content') \
        .with_near_vector(vec) \
        .with_limit(k) \
        .do()

    output = []
    closest_paragraphs = result.get('data').get('Get').get('Article')
    for p in closest_paragraphs:
        output.append(p.get('content'))

    return output


if __name__ == '__main__':
    set_schema()
    sample_file = 'please insert path here'
    article_df = pd.read_pickle(sample_file)
    load_embeddings_to_base(article_df)




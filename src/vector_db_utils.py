import weaviate

from settings import OPENAI_TOKEN

if __name__ == '__main__':
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

    # get the schema to make sure it worked
    print(client.schema.get())

    ### Step 1 - configure Weaviate Batch, which optimizes CRUD operations in bulk
    # - starting batch size of 100
    # - dynamically increase/decrease based on performance
    # - add timeout retries if something goes wrong
    client.batch.configure(
        batch_size=100,
        dynamic=True,
        timeout_retries=3,
    )

    ### Step 2 - import data

    print("Uploading data with vectors to Article schema..")

    counter = 0



    # with client.batch as batch:
    #     for k, v in article_df.iterrows():
    #
    #         # print update message every 100 objects
    #         if (counter % 100 == 0):
    #             print(f"Import {counter} / {len(article_df)} ")
    #
    #         properties = {
    #             "title": v["title"],
    #             "content": v["text"]
    #         }
    #
    #         vector = v["title_vector"]
    #
    #         batch.add_data_object(properties, "Article", None, vector)
    #         counter = counter + 1
    #
    # print(f"Importing ({len(article_df)}) Articles complete")



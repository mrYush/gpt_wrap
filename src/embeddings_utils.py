import os
import warnings
from itertools import islice
from typing import Union

import openai
import pandas as pd
import tiktoken
from PyPDF2 import PdfReader
from tqdm import tqdm

from settings import OPENAI_TOKEN

openai.api_key = OPENAI_TOKEN


class TextToEmbedings:
    def __init__(self,
                 encoding_base="cl100k_base",
                 model='text-embedding-ada-002',
                 embedding_ctx_length=8191,
                 cost_encoding_per_token=0.0004 / 1000,
                 max_cost_to_encode = None
                 ):
        self.encoding_embedding = encoding_base
        self.model = model
        self.embedding_ctx_length = embedding_ctx_length
        self.cost_encoding_per_token = cost_encoding_per_token
        self.max_cost_to_encode = max_cost_to_encode
        self.money_left = max_cost_to_encode

    def truncate_text_tokens(self, text):
        """Truncate a string to have `max_tokens` according to the given encoding."""
        encoding = tiktoken.get_encoding(self.encoding_embedding)
        return encoding.encode(text)[:self.embedding_ctx_length]

    def batched(self, iterable, n):
        """Batch data into tuples of length n. The last batch may be shorter."""
        # batched('ABCDEFG', 3) --> ABC DEF G
        encoding = tiktoken.get_encoding(self.encoding_embedding)
        if n < 1:
            raise ValueError('n must be at least one')
        it = iter(iterable)
        while batch := list(islice(it, n)):
            yield encoding.decode(batch)

    def chunked_text(self, text):
        encoding = tiktoken.get_encoding(self.encoding_embedding)
        tokens = encoding.encode(text)
        chunks_iterator = self.batched(tokens, self.embedding_ctx_length)
        yield from chunks_iterator

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return openai.Embedding.create(input=[text], model=self.model)['data'][0]['embedding']

    def len_safe_get_embedding(self, text):
        chunk_embeddings = []
        cunk_texts = []
        for chunk in self.chunked_text(text):
            chunk_embeddings.append(self.get_embedding(chunk))
            cunk_texts.append(chunk)

        return chunk_embeddings, cunk_texts

    def read_pdf(self, path: str) -> list:
        reader = PdfReader(path)
        full_book = []
        book_tokens = 0

        encoding = tiktoken.get_encoding(self.encoding_embedding)

        for page in reader.pages:
            extr_res = page.extract_text()

            extr_res = extr_res.replace('\n', ' ')
            extr_res = extr_res.replace('- ', '-')
            extr_res = extr_res.replace('\n-', '\n')

            full_book.append(extr_res)
            page_tokens = encoding.encode(extr_res)
            book_tokens += len(page_tokens)

        est_cost = book_tokens * self.cost_encoding_per_token
        spent = self.max_cost_to_encode - self.money_left
        print(f'total tokens in this book: {book_tokens}, '
              f'total pages in this book: {len(full_book)}, '
              f'total estimated cost for this book : {est_cost}, '
              f'already spent {spent}')

        if (self.max_cost_to_encode is not None) and \
                (self.money_left <= est_cost):
            print(f'Cost for this book is bigger than set limit ... interrupting')
            return list()

        self.money_left -= est_cost
        return full_book

    def process_one_file(self, path_to_file: str) -> pd.DataFrame:

        filename, file_extension = os.path.splitext(path_to_file)
        if file_extension == '.pdf':
            full_book = self.read_pdf(path_to_file)
        else:
            warnings.warn('only "*.pdf" type is supported for now .. skipping')
            return pd.DataFrame(
                {
                    'file_path': [path_to_file],
                    'text': [None],
                    'embeddings': [None],
                 }
            )

        full_book_chunked = []
        embeddings = []

        for text in tqdm(full_book):
            if len(text.replace(' ', '')) == 0:
                continue

            chunk_emb, chunk_text = self.len_safe_get_embedding(text)
            embeddings += chunk_emb
            full_book_chunked += chunk_text

        return pd.DataFrame({'text': full_book_chunked, 'embeddings': embeddings})

    def process_files(self, path_to_file: Union[str, list]) -> pd.DataFrame:

        if type(path_to_file) == str:
            return self.process_one_file(path_to_file=path_to_file)

        elif type(path_to_file) == list:
            results = []
            for file in path_to_file:
                file_res = self.process_one_file(path_to_file=file)
                file_res['file_path'] = file
                results.append(file_res)

            return pd.concat(results)

        else:
            raise ValueError('path to file could be only list with str or str')
#!/usr/bin/env python3

import os

from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.index import Index, create_in


doc_schema = Schema(
    title=TEXT(stored=True),
    description=TEXT(stored=True),
    content=TEXT(stored=True),
    id=ID(stored=True),
    keywords=KEYWORD,
)


if not os.path.exists("apiserver/index"):
    os.mkdir("apiserver/index")


search_index: Index = create_in("apiserver/index", doc_schema)
index_writer = search_index.writer()


def markdown_to_json(lines: list[str]) -> dict:
    doc = {}
    for line in lines:
        line = line.replace('\n', '')
        if ": " in line:
            attr, val = line.split(": ", 1)
            if attr in ["title", "description", "keywords"]:
                doc[attr] = val
    doc['content'] = ''.join(lines)
    return doc


wiki_files = os.listdir('investorswiki')

for file in wiki_files:
    with open(f"investorswiki/{file}", 'r') as f:
        doc_id = file.replace('.md', '')
        lines = f.readlines()
        doc_dict = markdown_to_json(lines)
        doc_dict['id'] = doc_id
        index_writer.add_document(
            **doc_dict
        )

index_writer.commit()
from pathlib import Path
import os

from django.core.management.base import BaseCommand

from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.index import Index, create_in


APP_DIR = Path(__file__).resolve().parent.parent.parent
INDEX_DIR = "index"
INDEX_PATH = APP_DIR / INDEX_DIR

INVESTORS_WIKI_DIR = APP_DIR / "investorswiki"

DOC_SCHEMA = Schema(
    title=TEXT(stored=True),
    description=TEXT(stored=True),
    content=TEXT(stored=True),
    id=ID(stored=True),
    keywords=KEYWORD,
)


def _markdown_to_json(lines: list[str]) -> dict:
    doc = {}
    for line in lines:
        line = line.replace('\n', '')
        if ": " in line:
            attr, val = line.split(": ", 1)
            if attr in ["title", "description", "keywords"]:
                doc[attr] = val
    doc['content'] = ''.join(lines)
    return doc


class Command(BaseCommand):
    help = "Builds the search index with investor wiki content"

    def handle(self, *args, **kwargs):
        if not os.path.exists(INDEX_PATH):
            os.mkdir(INDEX_PATH)

        search_index: Index = create_in(INDEX_PATH, DOC_SCHEMA)
        index_writer = search_index.writer()

        wiki_files = os.listdir(INVESTORS_WIKI_DIR)

        file_count = len(wiki_files)
        self.stdout.write(f"Indexing {file_count} files.")

        indexed_count = 0
        for file in wiki_files:
            with open(f"{INVESTORS_WIKI_DIR}/{file}", 'r') as f:
                doc_id = file.replace('.md', '')
                lines = f.readlines()
                doc_dict = _markdown_to_json(lines)
                doc_dict['id'] = doc_id
                index_writer.add_document(
                    **doc_dict
                )
            indexed_count += 1
            if indexed_count % 500 == 0:
                percent = round(float(indexed_count) / float(file_count) * 100, 2)
                self.stdout.write(f"Indexed {indexed_count} files ({percent}% completed.)")

        index_writer.commit()
        self.stdout.write("Indexing process completed!")
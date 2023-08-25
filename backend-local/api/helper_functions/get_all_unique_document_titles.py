import os 
from typing import List
import numpy


def get_unique_document_titles() -> List[str]:
    return ['']


if __name__ == "__main__":
    from get_unique_documents_from_query import get_unique_doc_titles
    #example usage
    print(get_unique_document_titles())
else:
    from .get_unique_documents_from_query import get_unique_doc_titles
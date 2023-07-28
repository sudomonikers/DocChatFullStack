from typing import List, Dict, Any, Union

def get_unique_doc_titles(json_object: Dict[str, Union[List[Dict[str, Any]], str]]) -> List[str]:
    doc_titles = set()
    if 'matches' in json_object and isinstance(json_object['matches'], list):
        for match in json_object['matches']:
            if 'metadata' in match and 'doc_title' in match['metadata']:
                doc_title = match['metadata']['doc_title']
                doc_titles.add(doc_title)
    return list(doc_titles)

if __name__ == "__main__":
    #example usage
    print(get_unique_doc_titles({"matches": [{"metadata": {"doc_title": "test1"}}, {"metadata": {"doc_title": "test2"}}]}))
import json

class SearchParams:
    def __init__(self, search_params: dict):
        self.search_params = search_params

    def get_size(self):
        return self.search_params.get('size')

    def get_dict(self):
        return self.search_params
    
class SearchResults:
    """
    Represents a collection of search results.
    Fields:
    id -> string
    title -> string
    price -> float
    size -> string
    url -> string
    img -> list of string
    """

    def __init__(self, results_json: str):
        self.results = json.loads(results_json)

    def get(self, index: int) -> dict:
        """
        Returns the search result at the specified index as a dictionary.
        """
        try:
            return self.results[index]
        except IndexError:
            return "Index out of range. No result found at the given index."

    def get_all(self) -> list:
        """
        Returns all search results as a list of dictionaries.
        """
        return self.results
    
    def count(self) -> int:
        """
        Returns the total number of search results.
        """
        return len(self.results)
    
    def __str__(self) -> str:
        result_strings = []
        for i, result in enumerate(self.results, start=1):
            item_str = f"Item {i}: ID={result.get('id')}, Title={result.get('title')}, Price={result.get('price')}, Size={result.get('size')}, URL={result.get('url')}"
            result_strings.append(item_str)
        return f"Total search results: {self.count()}\n" + "\n".join(result_strings)
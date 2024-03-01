from abc import ABC, abstractmethod
import httpx
from postalservice.utils.search_utils import SearchParams

class PostalService(ABC):
    @abstractmethod
    async def fetch_data(self, message: str) -> httpx.Response:

        pass

    @abstractmethod
    def parse_response(self, response: str):

        pass

    @abstractmethod
    def get_search_params(self, data: SearchParams):

        pass
    



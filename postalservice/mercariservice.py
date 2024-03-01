import json
import random
import string
import httpx
from postalservice.postalservice import PostalService
from postalservice.utils.network_utils import get_pop_jwt
from postalservice.utils.search_utils import SearchParams

CHARACTERS = string.ascii_lowercase + string.digits
HITS_PER_PAGE = 10

class MercariService(PostalService):
    
    async def fetch_data(self, message: str) -> httpx.Response:

        search_term = message

        url = "https://api.mercari.jp/v2/entities:search"
        searchSessionId = ''.join(random.choice(CHARACTERS) for i in range(32))
        payload = {
            "userId": "",
            "pageSize": HITS_PER_PAGE,
            "searchSessionId": searchSessionId,
            "indexRouting": "INDEX_ROUTING_UNSPECIFIED",
            "thumbnailTypes": [],
            "searchCondition": {
                "keyword": search_term,
                "excludeKeyword": "",
                "sort": "SORT_CREATED_TIME",
                "order": "ORDER_DESC",
                "status": [],
                "sizeId": [],
                "categoryId": [],
                "brandId": [],
                "sellerId": [],
                "priceMin": 0,
                "priceMax": 0,
                "itemConditionId": [],
                "shippingPayerId": [],
                "shippingFromArea": [],
                "shippingMethod": [],
                "colorId": [],
                "hasCoupon": False,
                "attributes": [],
                "itemTypes": [],
                "skuIds": []
            },
            "defaultDatasets": ["DATASET_TYPE_MERCARI", "DATASET_TYPE_BEYOND"],
            "serviceFrom": "suruga",
            "userId": "",
            "withItemBrand": False,
            "withItemSize": True
        }
        headers = {
            "dpop": get_pop_jwt(url, "POST"),
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "x-platform": "web"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200: return response
            else: 
                raise Exception(f"Failed to fetch data from Mercari API. Status code: {response.status_code}")
        
        
    def parse_response(self, response: str) -> str:
        items = json.loads(response.text)['items']
        cleaned_items_list = []
        for item in items:
            temp = {}

            # Check that each field is of the expected type
            if not isinstance(item.get('id'), str):
                raise TypeError('id must be a string')
            temp['id'] = item['id']

            if not isinstance(item.get('name'), str):
                raise TypeError('name must be a string')
            temp['title'] = item['name']

            price = float(item.get('price'))
            if not isinstance(price, (int, float)):
                raise TypeError('price must be a number')
            temp['price'] = item['price']

            if item.get('itemSize') and isinstance(item['itemSize'], dict):
                temp['size'] = item['itemSize'].get('name')
            else:
                temp['size'] = None

            temp['url'] =  'https://jp.mercari.com/item/' + item['id']

            if not isinstance(item.get('thumbnails'), list):
                raise TypeError('thumbnails must be a list')
            temp['img'] = item['thumbnails']
                
            cleaned_items_list.append(temp)

        item_json = json.dumps(cleaned_items_list)
        return item_json
    
    def get_search_params(self, data: SearchParams):
        return data.get_all()
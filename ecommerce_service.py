import asyncio

from typing import List
from dataclasses import dataclass

MAX_LIST_OF_ITEM_IDS_AVAILABILITY_CALL = 100
MAX_LIST_OF_ITEM_IDS_PRICING_CALL = 150


@dataclass
class PricedItem:
    item_id: str
    selling_price: float
    discount: bool


async def consult_item_available(item_ids: List[str]) -> List[bool]:
    """
    Checks for a batch of item_ids if each of them are available or not

    :param item_ids: List of IDs of the items for which we need to know the availability
    :return: List of booleans indicating the availability of each ID in item_ids

        .. note:
            The service does not accept a list longer than MAX_LIST_OF_ITEM_IDS_AVAILABILITY_CALL
    """
    import random
    assert len(item_ids) <= MAX_LIST_OF_ITEM_IDS_AVAILABILITY_CALL
    await asyncio.sleep(0.1)
    # backend logic from the server 
    return [bool(random.randint(0, 1)) for _ in item_ids]


async def consult_price(item_ids: List[str]) -> List[PricedItem]:
    """
    Returns a list of :class:PricedItem for each of the requested item_ids


    :param item_ids: List of IDs of the items for which we need to know the pricing information
    :return: List of :class:PricedItem for each of the item_ids

        .. note:
            The service does not accept a list longer than MAX_LIST_OF_ITEM_IDS_PRICING_CALL
    """
    import random
    assert len(item_ids) <= MAX_LIST_OF_ITEM_IDS_PRICING_CALL
    await asyncio.sleep(0.1)
    # backend logic from the server 
    return [PricedItem(item_id, random.random(), bool(random.randint(0, 1))) for item_id in item_ids]


def return_top_cheapest_items(item_ids: List[str], top_k: int) -> List[str]:
    """
    Function that receives a list of item IDs and a top_k parameter, and returns a
    list of item_ids that are available and sorted from cheapest to most expensive

    :param item_ids: The list of item IDs that are candidates to be returned
    :param top_k: The amount of item IDs to be returned
    """

    # Select available items
    item_availability = asyncio.run(consult_item_available(item_ids))
    item_available = [item_ids[index] for index, item in enumerate(item_availability) if item==True]

    # Sort items from cheapest to most expensive
    item_price = asyncio.run(consult_price(item_available))
    item_price.sort(key=lambda x:x.selling_price)

    # Promote better discounted items
    promoted_item_price = promote_discounted_items(item_price)
    
    # Extract top_k items
    top_cheapest = item_price[:top_k]
    return [item.item_id for item in top_cheapest]


def promote_discounted_items(item_price: List[PricedItem]) -> List[PricedItem]:
    """
    Function that receives a sorted list of :class:PricedItem for each of the item_ids,
    and returns a list of :class:PricedItem where we have promoted the discounted items.

    :param item_price: The sorted list of :class:PricedItem for each of the item_ids
    :return: List of :class:PricedItem for each of the item_ids
    """
    items_discounted = [item for item in item_price if item.discount==1]
    items_not_discounted = [item for item in item_price if item.discount==0]
    items_discounted += items_not_discounted
    return items_discounted
    
    
if __name__ == '__main__':
    top_k = 2
    items_ids = ['item_id_1', 'item_id_2', 'item_id_3', 'item_id_4', 'item_id_5',
                'item_id_6', 'item_id_7', 'item_id_8', 'item_id_9']
    top_cheapest_items = return_top_cheapest_items(items_ids, top_k)
    print(f'The top cheapest items are: {top_cheapest_items}')

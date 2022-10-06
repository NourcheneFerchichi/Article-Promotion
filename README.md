# E-commerce company service

We are an e-commerce company, and we have to write a service whose job will be to return the `top_k` items. `top_k` here means the `k` cheapest items. This list should 
be sorted from cheapest to most expensive.

To support the service, we have to call 2 other external services managed by other teams in the company.

- Availability service (consult_item_available) is a service mantained by the operations team, that returns information about the stock availability of a given item

- Pricing service (consult_price) is a service mantained by the pricing team, that knows the exact price applicable for each item at a given time, and whether it is
 discounted or not.

The interface with the Availability Service is clear because it returns a simple boolean for each item indicating its availability.
With the pricing team, we have agreed on encapsulating the response in a class `PricedItem` where the selling price and the discount flag is filled.

Both services can process in a single call as much as MAX_LIST_OF_ITEM_IDS_AVAILABILITY_CALL and MAX_LIST_OF_ITEM_IDS_PRICING_CALL for a single request.

The job of the team is to provide a service that returns the list of top_k items that are available. The list should be sorted from cheapest to most expensive. 
The product manager also told us that they would like to promote better discounted items, because they plan to show a special badge in the frontend.

    ..note:
        `consult_item_available` and `consult_price` are shown for clarity, but the exact implementation is unknown,

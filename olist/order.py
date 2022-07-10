
from olist.data import Olist
import pandas as pd
import numpy as np

class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        order = self.data['orders'].copy()
        order = order[order['order_status'] == 'delivered']

        order[['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']] = \
        order[['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']]\
        .apply(pd.to_datetime)

        order['expected_wait_time'] = (order['order_estimated_delivery_date']\
        - order['order_purchase_timestamp'])/np.timedelta64(1, 'D')
        order['true_wait_time'] = (order['order_delivered_customer_date']\
        - order['order_purchase_timestamp'])/np.timedelta64(1, 'D')

        order['delay_vs_expected'] = order['true_wait_time'] - order['expected_wait_time']

        order = order[['order_id', 'true_wait_time', 'delay_vs_expected', 'order_status']]

        return order
    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews']

        reviews['one_star'] = reviews['review_score'].apply(lambda x: 1 if x == 1 else 0)
        reviews['five_star'] = reviews['review_score'].apply(lambda x: 1 if x == 5 else 0)

        reviews = reviews[['order_id', 'one_star', 'five_star', 'review_score']]

        return reviews

    def get_product_seller_price_freight_aggregate(self):
        """
        Returns a DataFrame with:
        order_id, number_of_products
        """
        order_items = self.data['order_items']

        order_items = order_items.groupby('order_id')['seller_id', 'product_id', 'price', 'freight_value']\
        .agg({'price' : 'sum', 'freight_value':'sum','seller_id': 'count', 'product_id': 'count'})\
        .rename(columns = {'seller_id': 'number_of_sellers', 'product_id': 'number_of_products'})

        order_items = order_items.reset_index()
        order_items = order_items[['order_id', 'number_of_products', 'number_of_sellers', 'price', 'freight_value']]

        return order_items

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_products', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        data_complete = Order.get_wait_time(self, is_delivered=True)\
        .merge(Order.get_review_score(self), on = 'order_id')\
        .merge(Order.get_product_seller_price_freight_aggregate(self), on = 'order_id')

        return data_complete

    if __name__ == '__main__':
        print(get_training_data())

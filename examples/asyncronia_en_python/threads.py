#! /usr/bin/python3
from queue import Queue
from threading import Thread
import time
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=10, datefmt='%H:%M:%S')

class Waiter:
    PREPARATION_TIME = {
        'burger':7.5,
        'frites':4,
        'soda':1,
        'beer':1.2,
    }

    def __init__(self, orders, id):
        self.orders = orders
        self.id = id

    def request_orders(self):
        while not self.orders.empty():
            order = self.orders.get()
            self.request_order(order)

    def request_order(self, order):
        logging.info('<Waiter: {}> [Order: {}] {:*^30}'.format(self.id, order['id'], 'Request order!'))
        for product in order['products']:
            self.request_product(product, order['id'])
        self.dispatch_order(order)

    def request_product(self,product, order_id):
        time_sleep = self.PREPARATION_TIME[product]
        logging.info(f'<Waiter: {self.id}> [Order: {order_id}] Request {product}. Wait {time_sleep} seg...')
        time.sleep(time_sleep)
        logging.info(f'<Waiter: {self.id}> [Order: {order_id}] Done {product}')

    def dispatch_order(self, order):
        logging.info(f'<Waiter: {self.id}> [Order: {order["id"]}] Done order!')
        for product in order['products']:
            logging.info(f'<Waiter: {self.id}> [Order: {order["id"]}] Dispatch {product}')
        logging.info('<Waiter: {}> [Order: {}] {:-^30}\n'.format(self.id, order["id"], 'Done dispatch!'))


class Cashier:
    orders = Queue()

    def __init__(self):
        self.waiters = [Waiter(self.orders, id+1) for id in range(2)]
        

    def receive_orders(self, orders:list):
        for i, value in enumerate(orders):
            order = {
                'id': i,
                'products':value
            }
            self.orders.put(order)
        logging.info('Received orders')
        for waiter in self.waiters:
            thread = Thread(target=waiter.request_orders)
            thread.start()

def main():
    orders = [
        ('burger','soda',),
        ('burger','burger', 'beer', 'frites'),
        ('beer', 'beer', 'beer'),
        ('burger','frites'),
    ]
    cashier = Cashier()
    cashier.receive_orders(orders)


if __name__ == '__main__':
    main()

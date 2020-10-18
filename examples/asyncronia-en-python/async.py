#! /usr/bin/python3
from queue import Queue
import asyncio
import logging

logging.basicConfig(format='[Thr:%(threadName)s]  %(message)s', level=10)


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
 
    async def request_orders(self):
        """
        Pedimos todas las ordenes casi en el mismo momento.
        Sin importar si ya la orden anterior esta lista.
        """
        coros = list()
        while not self.orders.empty():
            order = self.orders.get()
            coros.append(self.request_order(order))
        await asyncio.gather(*coros)

    async def request_order(self, order):
        """
        Pedir los productos a la cocina y dispachar la orden.
        """
        logging.info('<Waiter: {}> [Order: {}] {:*^30}'.format(self.id, order['id'], 'Request order!'))
        coros = [
            self.request_product(product, order['id']) for product in order['products']
        ]
        await asyncio.gather(*coros)
        self.dispatch_order(order)

    async def request_product(self,product, order_id):
        """
        Pedir un producto a la cocina.
        """
        time_sleep = self.PREPARATION_TIME[product]
        logging.info(f'<Waiter: {self.id}> [Order: {order_id}] Request {product}. Wait {time_sleep} seg...')
        await asyncio.sleep(time_sleep)
        logging.info(f'<Waiter: {self.id}> [Order: {order_id}] Done {product}')

    def dispatch_order(self, order):
        """Despacharle los productos al cliente"""
        logging.info(f'<Waiter: {self.id}> [Order: {order["id"]}] Done order!')
        for product in order['products']:
            logging.info(f'<Waiter: {self.id}> [Order: {order["id"]}] Dispatch {product}')
        logging.info('<Waiter: {}> [Order: {}] {:-^30}\n'.format(self.id, order["id"], 'Done dispatch!'))


class Cashier:
    orders = Queue()

    def __init__(self):
        self.waiter = Waiter(self.orders, 1)

    def receive_orders(self, orders:list):
        for i, value in enumerate(orders):
            order = {'id': i, 'products': value}
            self.orders.put(order)
        logging.info('Received orders')
        asyncio.run(self.waiter.request_orders())

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

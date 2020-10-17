#! /usr/bin/python3
from queue import Queue
import asyncio
import logging

logging.basicConfig(format='[Thr:%(threadName)s]  %(message)s', level=10)


class Chef:
    PREPARATION_TIME = {
        'burger':7.5,
        'frites':4,
        'soda':1,
        'beer':1.2,
    }

    def __init__(self, kitchen, id):
        self.kitchen = kitchen
        self.id = id

    async def dispatch_orders(self):
        coros = list()
        while not self.kitchen.orders.empty():
            order_id, order = self.kitchen.orders.get()
            coros.append(self.make_order(order, order_id))
        await asyncio.gather(*coros)

    async def make_order(self,order, order_id):
        logging.info('<CHEF: {}> [Order: {}] {:*^30}'.format(self.id, order_id, 'Making order!'))

        coros = [self.make_product(product, order_id) for product in order]
        await asyncio.gather(*coros)

        logging.info(f'<CHEF: {self.id}> [Order: {order_id}] Done order!')
        self.kitchen.dispatch_order(order)

    async def make_product(self,product, order_id):
        time_sleep = self.PREPARATION_TIME[product]
        logging.info(f'<CHEF: {self.id}> [Order: {order_id}] Making {product}. Wait {time_sleep} seg...')
        await asyncio.sleep(time_sleep)
        logging.info(f'<CHEF: {self.id}> [Order: {order_id}] Done {product}')

class Kitchen:
    orders = Queue()

    def __init__(self):
        self.chef = Chef(self, 1)


    def receive_orders(self, orders:list):
        for i, order in enumerate(orders):
            self.orders.put((i, order))
        logging.info('Resquest orders')
        asyncio.run(self.chef.dispatch_orders())


    def dispatch_order(self, order):
        for product in order:
            logging.info(f'Dispatch {product}')
        logging.info('{:-^30}\n'.format('Done dispatch!'))


def main():
    orders = [
        ('burger','soda',),
        ('burger','burger', 'beer', 'frites'),
        ('beer', 'beer', 'beer'),
        ('burger','frites'),
    ]
    kitchen = Kitchen()
    kitchen.receive_orders(orders)


if __name__ == '__main__':
    main()

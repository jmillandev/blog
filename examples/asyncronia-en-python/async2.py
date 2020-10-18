#! /usr/bin/python3
import asyncio
import logging
import aiohttp

logging.basicConfig(format='[ %(asctime)s ]  %(message)s', level=10)

API = 'https://swapi.dev/api/people/{id}/'

async def get_person(session, id):
    url = API.format(id=id)
    async with session.get(url) as response:
        logging.info(f'Request person number {id}')
        person = await response.json()
        logging.info(f'Person number {id} = {person["name"]}')

async def main():
    async with aiohttp.ClientSession() as session:
        coros = [get_person(session, id) for id in range(1, 10)]
        await asyncio.gather(*coros)

if __name__ == '__main__':
    asyncio.run(main())

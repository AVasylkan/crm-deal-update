import V, aiohttp
from aiohttp.log import client_logger
import dealid  
import asyncio

#STAGE_ID = C2:UC_3E1SIQ стадия зависли
#STAGE_ID = C2:WON стадия УСПЕХ
id_deal = dealid.id_deal
fields = {
        "CATEGORY_ID": 2,
        "STAGE_ID": "C2:WON",
        }


async def update_deal(session, deal_id, fields):
    data = {
        "id": deal_id,
        "fields": fields,
        "scope": "crm"
    }
    async with session.post(V.URL_UPDATE, json=data) as resp:
        response_json = await resp.json() 
        print(response_json['result']) 

async def main():
    async with aiohttp.ClientSession() as session:
        queue = asyncio.Queue()
        for deal_id in id_deal:
            task = update_deal(session, deal_id, fields)
            await queue.put(task)
        rate_limit = 100
        while not queue.empty():
            task = await queue.get()
            await task
            rate_limit -= 1
            if rate_limit == 0:
                print("Pausing for 20 second...") 
                await asyncio.sleep(20)
                rate_limit = 100

asyncio.run(main())
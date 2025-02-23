import aiohttp
import asyncio
import os
from aiofiles import open as aio_open

async def download_images(images, out_folder):
    
    try :
        async with aiohttp.ClientSession() as session:
            for id in images :
                url = images[id]
                async with session.get(url) as response:
                    if response.status == 200:
                        async with aio_open(f"{out_folder}/{id}.jpg", 'wb') as file:
                            await file.write(await response.read())
        return True
    
    except Exception as e:
        return False


import asyncio

import aiohttp
import numpy as np
import pandas as pd

df = pd.read_csv("./data/gsmarena_brand_link1.csv")

headers = {
    "URL": "www.amazon.com",
    "accept-language": "en-US,en;q=0.9,bn;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
}

data = []
missing_data = []


async def get_pages(session, brand, devices, link, code, gen_link):
    async with session.get(gen_link) as response:
        if response.status == 200:
            print(f"success for {gen_link}")
            return (
                response.status,
                brand,
                devices,
                link,
                code,
                gen_link,
                await response.text(),
            )
        else:
            print(f"failed for {gen_link}")
            return (response.status, brand, devices, link, code, gen_link)


async def main():
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for brand, devices, link, code, gen_link in df.values:
            tasks.append(get_pages(session, brand, devices, link, code, gen_link))

        results = await asyncio.gather(*tasks)
        for result in results:
            if result[0] == 200:
                data.append(result[1:])
            else:
                missing_data.append(result[1:])


asyncio.run(main())

df1 = pd.DataFrame(data, columns=["brand", "devices", "link", "code", "gen_link", "html"])

df1.to_csv("./data/gsmarena_product_pages.csv", index=False)

df2 = pd.DataFrame(missing_data, columns=["brand", "devices", "link", "code", "gen_link"])

df2.to_csv("./data/gsmarena_missing_product_pages.csv", index=False)

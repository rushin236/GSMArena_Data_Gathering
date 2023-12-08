import asyncio
import logging

import aiohttp
import pandas as pd

df = pd.read_csv("./data/gsmarena_product_missing_data_final.csv")

headers = {
    "URL": "www.amazon.com",
    "accept-language": "en-US,en;q=0.9,bn;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
}

data = []
missing_data = []


async def get_data(session, brand, name, prod_link, img_link, devices, link, code, gen_link, html):
    async with session.get(prod_link, ssl=False) as response:
        try:
            if response.status == 200:
                logging.info(f"success for {prod_link}")
                return (
                    response.status,
                    brand,
                    name,
                    prod_link,
                    img_link,
                    devices,
                    link,
                    code,
                    gen_link,
                    html,
                    await response.text(),
                )
            else:
                logging.warning(f"failed for {prod_link}")
                return (response.status, brand, name, prod_link, img_link, devices, link, code, gen_link, html)
        except:
            return (500, brand, name, prod_link, img_link, devices, link, code, gen_link, html)


async def main():
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for brand, name, prod_link, img_link, devices, link, code, gen_link, html in df.values:
            tasks.append(get_data(session, brand, name, prod_link, img_link, devices, link, code, gen_link, html))

        results = await asyncio.gather(*tasks)
        for result in results:
            if result[0] == 200:
                data.append(result[1:])
            else:
                missing_data.append(result[1:])


asyncio.run(main())


old_df1 = pd.read_csv("./data/gsmarena_product_data_final1.csv")

new_df1 = pd.DataFrame(
    data, columns=['brand', 'name', 'prod_link', 'img_link', 'devices', 'link', 'code', 'gen_link', 'html', 'prod_html']
)

if len(new_df1) != 0:
    combined_df = pd.concat([old_df1, new_df1], ignore_index=True)
    combined_df.to_csv("./data/gsmarena_product_data_final1.csv", index=False)

df2 = pd.DataFrame(
    missing_data,
    columns=['brand', 'name', 'prod_link', 'img_link', 'devices', 'link', 'code', 'gen_link', 'html'],
)

df2.to_csv("./data/gsmarena_product_missing_data_final.csv", index=False)

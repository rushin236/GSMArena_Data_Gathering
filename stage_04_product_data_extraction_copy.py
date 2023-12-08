import asyncio
import logging

import aiohttp
import pandas as pd
import requests

logging.basicConfig()

df = pd.read_csv("./data/gsmarena_product_missing_data_final.csv")

headers = {
    "URL": "www.amazon.com",
    "accept-language": "en-US,en;q=0.9,bn;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
}

data = []
missing_data = []


def get_data(brand, name, prod_link, img_link, devices, link, code, gen_link, html):
    with requests.get(prod_link, headers=headers) as response:
        if response.status_code == 200:
            logging.info(f"success for {prod_link}")
            return (
                response.status_code,
                brand,
                name,
                prod_link,
                img_link,
                devices,
                link,
                code,
                gen_link,
                html,
                response.text,
            )
        else:
            logging.warning(f"failed for {prod_link}")
            return (response.status_code, brand, name, prod_link, img_link, devices, link, code, gen_link, html)


def main():
    tasks = []
    for brand, name, prod_link, img_link, devices, link, code, gen_link, html in df.values:
        tasks.append(get_data(brand, name, prod_link, img_link, devices, link, code, gen_link, html))

    results = tasks
    for result in results:
        if result[0] == 200:
            data.append(result[1:])
        else:
            missing_data.append(result[1:])


main()


df1 = pd.DataFrame(
    data, columns=['brand', 'name', 'prod_link', 'img_link', 'devices', 'link', 'code', 'gen_link', 'html', 'prod_html']
)

df1.to_csv("./data/gsmarena_product_data_final1.csv", index=False)

df2 = pd.DataFrame(
    missing_data,
    columns=['brand', 'name', 'prod_link', 'img_link', 'devices', 'link', 'code', 'gen_link', 'html'],
)

df2.to_csv("./data/gsmarena_product_missing_data_final.csv", index=False)

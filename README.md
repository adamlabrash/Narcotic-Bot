Narcotic-Bot
==============================

Narcotic-Bot is an open source data extraction system and dataset that monitors narcotic prices on darknet marketplaces. Ultimately this project aims to track the prices and traffic of narcotics over a sustained period of time.

For now, the project only monitors the White House Market, which is one of the more popular illicit marketplaces. The initial dataset has over 33000 product listings, and will increase as more products are listed and more marketplaces are tracked by the project.


---
## Dataset Overview

The data is available in CSV format, and will be updated each month.

Note that the categories are taken directly from the marketplace listings:


| Main Categories        | Sub-categories           | Total Listings (Aug 2021) |
| ------------- |:-------------| ---|
| Benzos      | Pills, Powder, RC | 2677 |
| Cannabis      | Buds and Flowers, Concentrates, Edibles, Hash, Seeds, Shake, Synthetic    | 12520 |
| Dissociatives | GHB, Ketamine, MXE     | 1608 |
| Ecstasy      | MDA, MDMA, Methylone and BK     | 2026 |
| Opioids | Buprenorphine, Codeine, Dihydrocodeine, Heroin, Hydrocodone, Hydromorphone, Morphine, Opium, Oxycodone    | 1522 |
| Prescription Drugs      | Other      | 1925 |
| Psychedelics | 2C-B, DMT, LSD, Shrooms      | 4315 |
| Steroids      | Other      | 1182 |
| Stimulants | Adderall, Cocaine, Crack, Mephedrone, Meth, Speed     | 5520 |
| Tobacco      | Other      | 19 |
| Weight Loss | Other      | 41 |


## Relation Schema

The narcotics table is populated with products with the following schema:

| Attribute | Data Properties | Description |
| ----- |:-----| ------------|
| id | SERIAL PRIMARY KEY | Unique number identifying the product within the dataset|
| website | VARCHAR(50) NOT NULL | the website that the product is listed |
| title | TEXT NOT NULL | description of the product listing |
| update_at | TIMESTAMP NOT NULL | date that the product listing was extracted (GST) |
| vendor | VARCHAR(100) NOT NULL | the name of the product lister |
| category | VARCHAR(50) NOT NULL | general classification of the drug i.e. 'benzos' or 'cannabis'|
| price | FLOAT NOT NULL | cost of the product in USD |
| sub_category | VARCHAR(50) | specific classification of the drug i.e. 'pills', 'edibles' |
| shipping_origin | VARCHAR(50) | where the product is shipped from (not always the true origin) |
| ships_to | VARCHAR(50) | regions and countries where the product is available |
| inventory_status | VARCHAR(50) | in stock, low stock, etc. |

Example entry:

| id | website | title | update_at | vendor | category | price | sub_category | shipping_origin | ships_to | inventory_status |
|--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 27910 | White House Market | 1g SPEEDPASTE AMPHETAMINE 63-73% PURITY | 2020-07-12 00:00:00 | clicknbuy | Stimulants | 9.24 | Speed | Netherlands | Worldwide | In stock |


Note that the data is only as accurate as the listings. If a vendor is dishonest about their product that information is still in the dataset.

---

While this project is completely legal, I do not hold responsibility for how others may use this software.

Future implementations:
* Extract products from additional marketplaces
* NLP and advanced analysis based on title and descriptions
* Web-hosted dashboard
* Seperate dataset of vendors
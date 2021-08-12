darknet-analysis
==============================

A data extraction pipeline and dataset that monitors narcotic prices on darknet marketplaces. Ultimately this project aims to track the prices and traffic of narcotics over a sustained period of time.

For now, the project only monitors the White House Market, which is one of the more popular illicit marketplaces. The initial dataset has over 33000 product listings, and will increase as more marketplaces are added to the project.

---
## Data Overview

The data is available in CSV format, and will be updated each month.

Note that the categories are directly taken from the marketplace:

| Main Categories        | Sub-categories           | Total Listings |
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

## Data Schema

The narcotics table is populated with products each with the schema outlined as follows:

id SERIAL PRIMARY KEY,
website varchar(50) NOT NULL,
title text NOT NULL,
update_at TIMESTAMP,
vendor varchar(100) NOT NULL,
category varchar(50) NOT NULL,
price float NOT NULL,
sub_category varchar(50),
shipping_origin varchar(50),
ships_to varchar(100),
inventory_status varchar(50)

Example entry:

| id | website | title | update_at | vendor | category | price | sub_category | shipping_origin | ships_to | inventory_status |
|--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 27910 | White House Market | TIMESTAMP | 1g SPEEDPASTE AMPHETAMINE 63-73% PURITY | clicknbuy | Stimulants | 9.24 | Speed | Netherlands | Worldwide | In stock |

There is often information in the title

Note that the data is only as accurate as the listings. If a vendor is lying about their product that information is still in the dataset.


---

While this project is completely legal, but I do not hold responsibility for how others may use this software.

Future implementations:
    -nlp and advanced analysis
    -Extract from more marketplaces
    -web-hosted dashboard
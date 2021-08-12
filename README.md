darknet-analysis
==============================

A data extraction pipeline and dataset that monitors narcotic prices on darknet marketplaces. Ultimately this project aims to track the prices and traffic of narcotics over a sustained period of time.

For now, the project only monitors the White House Market, which is one of the more popular illicit marketplaces.

---

## Data
Data is in CSV and .SQL format, and will be updated each month. 

The data is only as accurate as the listing itself. If a vendor is lying about their product, and will negatively change the data

Note that the categories are directly taken from the marketplace


| Main Categories        | Sub_categories           | Total Listings |
| ------------- |:-------------:| -----:|
| Benzos      | Pills, Powder, RC | $1600 |
| Cannabis      | Buds and Flowers, Concentrates, Edibles, Hash, Seeds, Shake, Synthetic    |   $12 |
| Dissociatives | GHB, Ketamine, MXE     |    $1 |
| Ecstasy      | MDA, MDMA, Methylone and BK     |   $12 |
| Opioids | Buprenorphine, Codeine, Dihydrocodeine, Heroin, Hydrocodone, Hydromorphone, Morphine, Opium, Oxycodone    |    $1 |
| Prescription Drugs      | Other      |   $12 |
| Psychedelics | 2C-B, DMT, LSD, Shrooms      |    $1 |
| Steroids      | Other      |   $12 |
| Stimulants | Adderall, Cocaine, Crack, Mephedrone, Meth, Speed     |    $1 |
| Tobacco      | Other      |   $12 |
| Weight Loss | Other      |    $1 |

---

While this project is completely legal, but I do not hold responsibility for how others may use this software.

Future implementations:
    -nlp and advanced analysis
    -Extract from more marketplaces
    -web-hosted dashboard

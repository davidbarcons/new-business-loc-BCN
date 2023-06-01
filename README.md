# new-business-loc-BCN

Where in Barcelona is my new business going to be most sucessful? 

I use  ML algorithms to find the best location for a new business.

Data is stored in a mySQL database, using the following tables:
- restaurant
- neighborhood
- district
- censal_section

Data is retrieved from the following sources:
- Google maps Places API.
  * Nearby search: place_id, name, rating, user_rating_total, price_level, vicinity, geometry, business_status
- Barcelona open data (city council). The complete catalog of dataset can be consulted at https://opendata-ajuntament.barcelona.cat/data/en/dataset
 - Median tax income per unit of consumption (€/year). Censal section classification. https://opendata-ajuntament.barcelona.cat/data/en/dataset/atles-renda-mediana/resource/ef7e3825-0afd-444e-997f-8a8e999f0fe7
 - Hospitals and CAPs. Exact location. https://opendata-ajuntament.barcelona.cat/data/en/dataset/sanitat-hospitals-atencio-primaria/resource/9e135848-eb0a-4bc5-8e60-de558213b3ed




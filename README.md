# new-business-loc-BCN

Where in Barcelona is my new business going to be most sucessful? 
*Note: It will fisrt be implemented for restaurants due to google maps api restrictions

I use ML to find the best location for a new business.

Data is retrieved from the following sources:
- Google maps Places API.
  * Nearby search: place_id, name, rating, user_rating_total, price_level, vicinity, geometry, business_status
- Barcelona open data (city council). The complete catalog of dataset can be consulted at https://opendata-ajuntament.barcelona.cat/data/en/dataset. Data is stored in a mySQL database. We use the notebooks in bcn-open-data/loaders to load the data to our local mySQL database.


List of resources implemented:
 - Median tax income per unit of consumption (€/year). Censal section classification. https://opendata-ajuntament.barcelona.cat/data/en/dataset/atles-renda-mediana/resource/ef7e3825-0afd-444e-997f-8a8e999f0fe7
 - Hospitals and CAPs. Exact location. https://opendata-ajuntament.barcelona.cat/data/en/dataset/sanitat-hospitals-atencio-primaria/resource/9e135848-eb0a-4bc5-8e60-de558213b3ed
 - Population in every censal section by sex, age group (0-18, 18-64, 64+) and national/EU/extra-communitary. https://opendata-ajuntament.barcelona.cat/data/en/dataset/taula-map-scensal/resource/f1d9d5aa-61d7-460e-b423-1bbfff96fab3
 - Public transports (underground, Renfe, FGC, funicular, cable car, tramcar, etc) of the city of Barcelona. https://opendata-ajuntament.barcelona.cat/data/en/dataset/transports/resource/e07dec0d-4aeb-40f3-b987-e1f35e088ce2
 - Hotels. https://opendata-ajuntament.barcelona.cat/data/en/dataset/allotjaments-hotels/resource/9bccce1b-0b9d-4cc6-94a7-459cb99450de
 - Tourist housing accomodations. By coordinates and available places. https://opendata-ajuntament.barcelona.cat/data/en/dataset/habitatges-us-turistic/resource/b32fa7f6-d464-403b-8a02-0292a64883bf
 - Points of interests. With coordinates. Need to choose. https://opendata-ajuntament.barcelona.cat/data/en/dataset/punts-informacio-turistica/resource/31431b23-d5b9-42b8-bcd0-a84da9d8c7fa

To implement:
 - Pedestrian streets, in a geojson format. https://opendata-ajuntament.barcelona.cat/data/en/dataset/carrers-plataforma-unica-bcn/resource/7ba0e893-dc28-499d-aba8-126fe95e6249
 - Areas of the city of Barcelona with higher concentration of tourism. Weird format. https://opendata-ajuntament.barcelona.cat/data/en/dataset/intensitat-activitat-turistica






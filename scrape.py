import time
import logging
import pandas as pd
from nytimesarticle import articleAPI

# Set up logging
logging.basicConfig(filename='nyt_api.log', level=logging.INFO)

# Initialize the API client
api = articleAPI("mmjN0edfoSxSC0FtNkzcCAG2MBNjSliB")

# Define the years we want to retrieve data for
start_year = 1923
end_year = 2022

# Define the columns we want to extract
columns = ['title', 'author', 'publisher', 'description', 'rank', 'weeks_on_list', 'price', 'isbn', 'genre']

# Initialize an empty list to store the data
data = []

# Loop through each year and week, and retrieve the data
for year in range(start_year, end_year + 1):
    for week in range(1, 54):
        try:
            # Make the API request
            articles = api.search(q='best sellers', fq={'source':['The New York Times']}, 
                                   begin_date=str(year)+'0101', end_date=str(year)+'1231', 
                                   sort='newest', page=0, facet_field='week', facet_filter=True, 
                                   facet_filter='week:'+str(week))

            # Extract the books from the API response
            books = articles['response']['docs']

            # Loop through each book and extract the desired data
            for book in books:
                try:
                    book_data = [book[column] for column in columns]
                    book_data.append(year)
                    data.append(book_data)
                except KeyError as e:
                    logging.warning(f"Missing data for book in year {year}, week {week}: {e}")
        except Exception as e:
            logging.error(f"Error retrieving data for year {year}, week {week}: {e}")

        # Add a delay between API requests to avoid hitting the rate limit
        time.sleep(2)

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data, columns=['title', 'author', 'publisher', 'description', 'rank', 'weeks_on_list', 'price', 'isbn', 'genre', 'year'])

# Save the data to a CSV file
df.to_csv('nyt_bestsellers.csv', index=False)

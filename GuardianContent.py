import requests, json, sys
import datetime as dt
import pandas as pd

URL = 'https://content.guardianapis.com/search'
API_KEY = open('key.txt', 'r').read().strip()

# no args - default behaviour, query for articles about coding and python
query_str = 'python AND coding'

# if cmd line args - create query from cmd line args (assumes user realises correct input format)
if len(sys.argv) > 1:
    # create query string from input
    query_str = ' '.join(sys.argv[1:])

query_file = '_'.join(query_str.split())
date_str = dt.datetime.now().strftime('%d_%m_%Y')

# add query params as dict
query_params = {
    'q': query_str,
    'show-fields': 'wordcount',
    'order-by': 'newest',
    'page-size': 200,
    'api-key': API_KEY
}

curr_page = 1
num_pages = 1
results = []

# download all pages
while curr_page <= num_pages:
    # add page to params
    query_params['page'] = curr_page

    # make request
    print(f'Downloading page {curr_page}...')
    res = requests.get(URL, params=query_params)
    res.raise_for_status()

    # load json as dict
    response = json.loads(res.text)

    # get number of pages
    num_pages = response['response']['pages']

    # append results to results arr
    page_results = response['response']['results']
    results += page_results

    curr_page += 1


print(f'{len(results)} results found...')

# format word count field
for page in results:
    page['wordcount'] = page['fields']['wordcount']
    page.pop('fields', None)

article_df = pd.DataFrame(results)

print('Formatting fields...')
# format date as dd/mm/yy
article_df['formatted_date'] = pd.to_datetime(article_df['webPublicationDate']).dt.strftime('%d/%m/%y')

# create a new column for year article was published
article_df['year'] = pd.to_datetime(article_df['webPublicationDate']).dt.strftime('%Y')

# remove articles with a wc < 1000
article_df = article_df.astype({'wordcount': 'int32'})
article_df = article_df[article_df['wordcount'] < 1000]
print(f'Removing articles with < 1000 words, remaining results: {article_df.shape[0]}')

# write to csv
print(f'Writing to {query_file}_{date_str}.csv...')
article_df.to_csv(f'{query_file}_{date_str}.csv', index=False)

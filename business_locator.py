import requests
import creds
import csv
import time
import datetime
import sys
import pandas as pd
import os
import os.path

# When Google API terminates connection because of limit
def process_csv_output(csv_data):

    time_start = csv_data["time_start"]
    b_name = csv_data["b_name"]
    b_phone_number = csv_data["b_phone_number"]
    b_address = csv_data["b_address"]
    b_website = csv_data["b_website"]
    b_gmb_url = csv_data["b_gmb_url"]
    b_name_not_existed = csv_data["b_name_not_existed"]
    b_add_not_existed = csv_data["b_add_not_existed"]
    b_query_list_exist = csv_data["b_query_list_exist"]


    time_end = datetime.datetime.now().replace(microsecond=0)
    runtime = time_end - time_start
    print(f"Script runtime: {runtime}.")
    print(' ')

    # Save scraped URLs to a CSV file
    now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    print('Saving to a CSV file...')
    print(' ')
    data = {"Query": b_query_list_exist, "Business Name":b_name,"Phone Number":b_phone_number, "Address":b_address, "Website":b_website, "GMB URL": b_gmb_url}
    df=pd.DataFrame(data=data)
    df.index+=1
    directory = os.path.dirname(os.path.realpath(__file__))
    filename = "business_details" + now + ".csv"
    file_path = os.path.join(directory,'csvfiles/', filename)
    df.to_csv(file_path)

    # Save recaptchaed requests to a CSV file
    if b_name_not_existed:
        no_gmb_data = {"Business Name":b_name_not_existed, "Address": b_add_not_existed}
        df2 = pd.DataFrame(data=no_gmb_data)
        df2.index+=1
        directory2 = os.path.dirname(os.path.realpath(__file__))
        filename2 = "gmb_not_existing" + now + ".csv"
        file_path2 = os.path.join(directory2,'no_google_business_address/', filename2)
        df2.to_csv(file_path2)

    print('Your files are ready.')
    print(' ')
    sys.exit()

def local_search():

    b_name = []
    b_phone_number = []
    b_address = []
    b_website = []
    b_gmb_url = []
    business_location_id = []
    b_name_not_existed = []
    b_add_not_existed = []
    b_query_list = []
    b_query_list_exist = []

    time_start = datetime.datetime.now().replace(microsecond=0)

    with open('search_query.csv') as f:
            reader = csv.DictReader(f)

            for line in reader:

                query = line['query']

                print(f'Searching for query: {query}')

                url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + query + "&radius=50000&key=" + creds.API_key

                payload={}
                headers = {}

                response = requests.request("GET", url, headers=headers, data=payload)
                response_items = response.json()
                result_items = response_items['results']
                
                for business_item in result_items:
                    business_location_id.append(business_item['place_id'])
                    b_query_list.append(query)
    
    for idx, businessID in enumerate(business_location_id):
        try:
            url = "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + businessID + "&fields=name,formatted_phone_number,formatted_address,website,url&key=" + creds.API_key

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            results = response.json()

            name = results['result']['name']
            formatted_phone_number = results['result']['formatted_phone_number']
            formatted_address = results['result']['formatted_address']
            website = results['result']['website']
            url = results['result']['url']

            b_name.append(name if name != "" else 'none')
            b_phone_number.append(formatted_phone_number if formatted_phone_number != "" else 'none')
            b_address.append(formatted_address if formatted_address != "" else 'none')
            b_website.append(website if website != "" else 'none')
            b_gmb_url.append(url if url != "" else 'none')
            b_query_list_exist.append(b_query_list[idx])
            print(f'{name} details retrieved successfully...')
            print(' ')
            time.sleep(1)

        except requests.exceptions.ConnectionError as e:
            print('Connection terminated...\n')
            csv_data = {
                'b_name': b_name,
                'b_phone_number': b_phone_number,
                'b_address': b_address,
                'b_website': b_website,
                'b_gmb_url': b_gmb_url,
                'b_name_not_existed': b_name_not_existed,
                'b_add_not_existed': b_add_not_existed,
                'time_start': time_start,
                'b_query_list_exist': b_query_list_exist

            }
            process_csv_output(csv_data)

        except:
            pass
    
    
    time_end = datetime.datetime.now().replace(microsecond=0)
    runtime = time_end - time_start
    print(f"Script runtime: {runtime}.\n")

    # Save scraped URLs to a CSV file
    now = datetime.datetime.now().strftime('%Y%m%d-%Hh%M')
    print('Saving to a CSV file...')
    print(' ')
    data = {"Query": b_query_list_exist, "Business Name":b_name,"Phone Number":b_phone_number, "Address":b_address, "Website":b_website, "GMB URL": b_gmb_url}
    df=pd.DataFrame(data=data)
    df.index+=1
    directory = os.path.dirname(os.path.realpath(__file__))
    filename = "business_details" + now + ".csv"
    file_path = os.path.join(directory,'csvfiles/', filename)
    df.to_csv(file_path)

    # Save NO GMB requests to a CSV file
    if b_name_not_existed:
        no_gmb_data = {"Business Name":b_name_not_existed, "Address": b_add_not_existed}
        df2 = pd.DataFrame(data=no_gmb_data)
        df2.index+=1
        directory2 = os.path.dirname(os.path.realpath(__file__))
        filename2 = "gmb_not_existing" + now + ".csv"
        file_path2 = os.path.join(directory2,'no_google_business_address/', filename2)
        df2.to_csv(file_path2)

    print('Your files are ready.\n')

if __name__ == '__main__':
    local_search()
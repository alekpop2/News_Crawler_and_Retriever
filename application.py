import requests
import json

def send_command_to_server(endpoint, data=None):
    url = f'http://3.134.76.36:5000{endpoint}'
    if data:
        response = requests.post(url, json=data)
    else:
        response = requests.get(url)
    return response.text

command = '0'

while command != '4':
    print('\n1. Crawl & Scrape TMZ\n2. Build Index\n3. Query\n4. Stop\n')
    command = input('Input the number of the command you would like to execute: ')

    match command:
        case '1':
            try:
                print(send_command_to_server('/crawl'))
            except Exception as e:
                print(f'exception: {e}')
                continue
        case '2':
            try:
                message = send_command_to_server('/build_index')
                if message == 'Index has been built.':
                    print(message)
                else:
                    print('docs.csv file does not exist')
            except Exception:
                print('docs.csv file does not exist')
                continue
        case '3':
            try:
                query = input('Input a query: ')
                response = send_command_to_server('/query', data={'query': query})
                docs = json.loads(response)
                for doc in docs:
                    print(f'Doc {doc['doc_index']}:\n{doc['doc_content']}\n')
            except Exception:
                print('pickled index file does not exist')
                continue
        case '4':
            print('Goodbye')
            break
        case _:
            print('Please enter a valid command number (1-4)')

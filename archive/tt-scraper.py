import json
import pandas

# Curl Command for getting Table tennis data:
#
# curl --request GET \
#   --url 'https://24live.com/api/tournament/22357?lang=en&section=all&seasonId=70665&short=0&limit=5000&sid=70523' \
#   --header 'accept: application/json, text/plain, */*' \
#   --header 'accept-language: en-US,en;q=0.8' \
#   --header 'cookie: XSRF-TOKEN=voSSbVIw5DNa3JSWXp0WVEo9RAzjeAptwjM9rqWk; laravelsession=LdRfSKOoOF4OaHZ2nnpcnUGN5FiYQZYWM6KGoHOH' \
#   --header 'priority: u=1, i' \
#   --header 'referer: https://24live.com/page/sport/event/table-tennis-22/22357?lang=en' \
#   --header 'sec-ch-ua: "Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"' \
#   --header 'sec-ch-ua-mobile: ?0' \
#   --header 'sec-ch-ua-platform: "Linux"' \
#   --header 'sec-fetch-dest: empty' \
#   --header 'sec-fetch-mode: cors' \
#   --header 'sec-fetch-site: same-origin' \
#   --header 'sec-gpc: 1' \
#   --header 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36' \
#   --header 'x-requested-with: XMLHttpRequest' \
#   --cookie 'XSRF-TOKEN=voSSbVIw5DNa3JSWXp0WVEo9RAzjeAptwjM9rqWk; laravelsession=LdRfSKOoOF4OaHZ2nnpcnUGN5FiYQZYWM6KGoHOH'

# with open('tt-export-111624.json', 'r') as file:
#     data = json.load(file)

# print(data)

# df =  pd.json_normalize(data['data']['finished'])

# df.to_csv('tt-match-data.csv', index=False)

from copy import deepcopy
import pandas


def cross_join(left, right):
    new_rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows


def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem


def json_to_dataframe(data_in):
    def flatten_json(data, prev_heading=''):
        if isinstance(data, dict):
            rows = [{}]
            for key, value in data.items():
                rows = cross_join(rows, flatten_json(value, prev_heading + '.' + key))
        elif isinstance(data, list):
            rows = []
            for item in data:
                [rows.append(elem) for elem in flatten_list(flatten_json(item, prev_heading))]
        else:
            rows = [{prev_heading[1:]: data}]
        return rows

    return pandas.DataFrame(flatten_json(data_in))


if __name__ == '__main__':

    with open('match-export-1.json', 'r') as file:
        json_data = json.load(file)

    # df = json_to_dataframe(json_data['data']['finished'])
    df = json_to_dataframe(json_data['h2h']['total']['h2h'])

    df.to_csv('tt-match-data-match.csv', index=False)

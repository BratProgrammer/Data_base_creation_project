import requests
from bs4 import BeautifulSoup

cookies = {
    '_gcl_au': '1.1.494824844.1717173572',
    '_ga': 'GA1.1.1795103482.1717173572',
    '_ALGOLIA': 'anonymous-cac854d2-8c07-4474-a9d8-0acc641e1727',
    '_ga_ELVP0YFQNX': 'GS1.1.1717178626.2.1.1717181038.60.0.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': '_gcl_au=1.1.494824844.1717173572; _ga=GA1.1.1795103482.1717173572; _ALGOLIA=anonymous-cac854d2-8c07-4474-a9d8-0acc641e1727; _ga_ELVP0YFQNX=GS1.1.1717178626.2.1.1717181038.60.0.0',
    'priority': 'u=0, i',
    'referer': 'https://www.iihs.org/ratings/class-summary/midsize-cars',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}


def get_int_from_symbol_grade(symbol):
    if symbol == 'P':
        return 1
    elif symbol == 'M':
        return 2
    elif symbol == 'A':
        return 3
    elif symbol == 'G':
        return 4
    else:
        return 0


def get_symbol(block):
    try:
        symbol = block.find('strong').text
    except:
        symbol = None
    if symbol == None:
        return 'NOT TESTED'
    else:
        return symbol


def is_it_in_top_safety_pick_plus(block):
    try:
        check = block.find('span', {'class': 'tspPlus is-small'})
        if check != None:
            return True
    except:
        return False


def is_it_in_top_safety_pick(block):
    try:
        check = block.find('span', {'class': 'tsp is-small'})
        if check != None:
            return True
    except:
        return False


def get_data_from_site():
    url_mask = 'https://www.iihs.org/ratings/class-summary/'
    car_types = "Minicars/Small-cars/Midsize cars/Midsize luxury cars/Midsize convertibles/Large cars/Large luxury cars/Small SUVs/Midsize SUVs/Midsize luxury SUVs/Large SUVs/Minivans/Small pickups/Large pickups".split(
        "/")

    cars = []
    cars_results = []
    top_safety_pick_cars = []
    top_safety_pick_plus_cars = []
    index = 0
    for i in range(len(car_types)):
        url = url_mask + car_types[i].lower().replace(" ", "-")
        response = requests.get(url, cookies=cookies, headers=headers).text

        page_code = BeautifulSoup(response, features="lxml")
        car_blocks = page_code.find_all('td', {'class': 'Vehicle'})
        for i in car_blocks:
            name = i.find('a').find('span', {'class': ''}).text
            info = i.find('a').find('span', {'class': 'door'}).text
            type = str(info.split('|')[0]).strip()
            year = str(info.split('|')[1]).strip().split(" ")[0]
            brand = name.split(" ")[0]
            model = name[len(brand):]
            car = {"model": model, "brand": brand, "type": type, "year": year}
            cars.append(car)

        buffer = page_code.find('tbody')
        car_results_code = buffer.find_all('tr')

        for i in car_results_code:
            index += 1
            sof = get_int_from_symbol_grade(get_symbol(i.find('td', {'data-label': 'Small overlap front'})))
            mof = get_int_from_symbol_grade(get_symbol(i.find('td', {'data-label': 'Moderate overlap front'})))
            s = get_int_from_symbol_grade(get_symbol(i.find('td', {'data-label': 'Side'})))
            h = get_int_from_symbol_grade(get_symbol(i.find('td', {'data-label': 'Headlights'})))
            fcpp = get_int_from_symbol_grade(get_symbol(i.find('td', {'data-label': 'Front crash prevention: pedestrian'})))
            sbr = get_int_from_symbol_grade(get_symbol(i.find('td', {'data-label': 'Seat belt reminders'})))
            leou = get_int_from_symbol_grade(get_symbol(i.find('td', {'data-label': 'LATCH ease of use '})))


            result = {"Small overlap front": sof,
                "Moderate overlap front": mof,
                "Side": s,
                "Headlights": h,
                "Front crash prevention: pedestrian": fcpp,
                "Seat belt reminders": sbr,
                "LATCH ease of use": leou,}
            cars_results.append(result)

            if is_it_in_top_safety_pick(i):
                average = (sof + mof + s + h + fcpp + sbr + leou) / 7
                top_safety_pick_cars.append({'car_id': index, 'average': average})
            elif is_it_in_top_safety_pick_plus(i):
                average = (sof + mof + s + h + fcpp + sbr + leou) / 7
                top_safety_pick_plus_cars.append({'car_id': index, 'average': average})


    grades = {0: 'NOT TESTED', 1: 'P', 2: 'M', 3: 'A', 4: 'G'}
    return cars, cars_results, grades, top_safety_pick_cars, top_safety_pick_plus_cars

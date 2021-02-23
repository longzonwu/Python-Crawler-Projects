import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


class TWLottery:

    def __init__(self):
        self.session = requests.Session()

    def crawl_list_page(self):
        prices = []
        raw_lotteries_info = []

        try:
            response = self.session.request(method="GET", url='https://www.taiwanlottery.com.tw/info/instant/sale.aspx')
            document = BeautifulSoup(response.content, 'lxml')

            # https://stackoverflow.com/questions/44428250/css-style-nth-sibling
            all_due_date_elements = document.select('table.tableFull td.td_center[rowspan="3"] ~ td:nth-of-type(5)')
            valid_count = 0
            for due_date_element in all_due_date_elements:
                lottery_due_date = due_date_element.text  # 110/7/19
                splitted_lottery_due_date = lottery_due_date.split('/')
                lottery_due_date = datetime(
                    int(splitted_lottery_due_date[0]) + 1911,
                    int(splitted_lottery_due_date[1]),
                    int(splitted_lottery_due_date[2]))
                today = datetime.now()
                if today > lottery_due_date:
                    break
                valid_count += 1

            # https://www.w3schools.com/css/css_combinators.asp
            all_lottery_elements = document.select('table.tableFull td.td_center[rowspan="3"]+td')
            for index, lottery_element in enumerate(all_lottery_elements):
                prices.append(lottery_element.text.replace(',', ''))
                if index >= valid_count:
                    break

            all_link_elements = document.select('table.tableFull a')
            for link_element in all_link_elements:
                lottery_info = {}
                link = link_element['href']
                if 'news' in link:
                    if len(raw_lotteries_info) >= valid_count:
                        break
                    lottery_info['url'] = link.split('#')[0]
                    lottery_info['id'] = link.split('#')[-1]
                    # 將 price 資訊組合進去
                    lottery_info['price'] = prices[len(raw_lotteries_info)]
                    raw_lotteries_info.append(lottery_info)
        except BaseException as error:
            print('{} in crawl_list_page'.format(error))
        finally:
            return raw_lotteries_info

    def process_raw_lotteries_info(self, raw_lotteries_info):
        all_url_info = {}
        for raw_lottery_info in raw_lotteries_info:
            url = raw_lottery_info['url']
            del raw_lottery_info['url']
            if url not in all_url_info:
                all_url_info[url] = {raw_lottery_info['id']: raw_lottery_info['price']}
            else:
                all_url_info[url][raw_lottery_info['id']] = raw_lottery_info['price']
        return all_url_info

    def crawl_url_detail(self, url, url_info):
        lotteries_per_url = []
        try:
            response = self.session.request(method="GET", url=url)
            document = BeautifulSoup(response.content, 'lxml')
            price_tables_elements = document.select('div.tx_md')
        except BaseException as error:
            print('{} in crawl_url_detail of {}'.format(error, url))
            return lotteries_per_url

        for price_table_element in price_tables_elements:
            lottery = {}
            expected_prize = 0

            try:
                id = price_table_element.select_one('p a')
                if not id:
                    continue
                id = id.get('id')
                lottery_price = url_info.get(id)
                if not lottery_price:
                    continue
                lottery_price = int(lottery_price)

                # https://www.w3schools.com/cssref/sel_nth-child.asp
                name = price_table_element.select_one('p:nth-child(2) strong')
                name = name.find(text=True).replace("遊戲主題：", '').strip()

                all_number = price_table_element.select('[align="right"]')
                if all_number:
                    total_count = all_number[-2]  # 4,999,680
                    total_count = re.findall(r'\d+', total_count.text)
                    total_count = int(''.join(total_count))

                    all_number = all_number[:-2]

                    for index in range(0, len(all_number), 2):
                        prize = all_number[index].text.strip()
                        count = all_number[index + 1].text.strip()
                        if not prize or not count:
                            continue

                        prize = re.findall(r'\d+', prize)  # NT$1,000,000
                        prize = int(''.join(prize))

                        count = re.findall(r'\d+', count)  # 951,800
                        count = int(''.join(count))

                        # 獎金大於 5000 以上，20% 稅，+ 4% 印花稅
                        if prize >= 5000:
                            tax = 0.796
                        else:
                            tax = 1
                        expected_prize += prize * tax * (count / total_count)

                    lottery["id"] = id
                    lottery["expected_prize"] = round(expected_prize, 3)
                    lottery["lottery_price"] = round(lottery_price, 3)
                    lottery["name"] = name
                    lottery["prize_ratio"] = round(expected_prize / lottery_price, 3)
                    lotteries_per_url.append(lottery)

            except BaseException as error:
                print('{} in crawl_url_detail of every lottery. {}'.format(error, url))
                continue

        return lotteries_per_url


def start_crawl():
    tw_lottery = TWLottery()
    result = []

    # 步驟 1, 2
    while True:
        # get 列表的時候，常會失敗
        raw_lotteries_info = tw_lottery.crawl_list_page()
        if raw_lotteries_info:
            break
        print("try again....")
    print("crawl_list_page done")

    # 步驟 3
    all_url_info = tw_lottery.process_raw_lotteries_info(raw_lotteries_info)
    print("process_raw_lotteries_info done")

    # 步驟 4
    for url, url_info in all_url_info.items():
        lotteries_per_url = tw_lottery.crawl_url_detail(url, url_info)
        if lotteries_per_url:
            result.extend(lotteries_per_url)

    # 排序
    result = sorted(result, key=lambda i: i['prize_ratio'], reverse=True)

    for lottery in result:
        print(lottery)


if __name__ == "__main__":
    start_crawl()
import os
import re
import sys
import requests
from bs4 import BeautifulSoup

class GoobikeScraper:
    def __init__(self, manufacturer, model):
        self.base_url = f"https://www.goobike.com/maker-{manufacturer}/car-{manufacturer}_{model}/index"
        self.bikes = []

    def scrape(self):
        # 最初のページの内容を取得して最大ページ数を把握
        response = requests.get(self.base_url + ".html")
        response.encoding = response.apparent_encoding
        
        if response.status_code != 200:
            return [f"検索結果の取得に失敗しました。ステータスコード: {response.status_code}"]
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # URL不正の場合
        errorDiv = soup.find('span', class_='sj')
        if not errorDiv:
            max_page_num = self.get_max_page_num(soup)
            # 各ページをループしてデータを収集
            for num in range(1, max_page_num + 1):
                page_content = self.get_page_content(num)
                if page_content:
                    self.extract_bike_data(page_content)

        return self.bikes

    def get_max_page_num(self, soup):
        # 最大ページ数を取得
        page_info = soup.find('div', class_='bxr').find('p')
        return int(re.search(r'\d+', str(page_info)).group())

    def get_page_content(self, page_num):
        # 指定されたページの内容を取得
        response = requests.get(f"{self.base_url}{page_num}.html")
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        return None

    def extract_bike_data(self, soup):
        # ページからバイクのデータを抽出
        results = soup.find_all('div', class_='bike_sec')
        for result in results:
            bike_info = result.find('div', class_='cont01')    # 車体情報用 div
            shop_info = result.find('div', class_='shop_info') # 販売店情報用 div
            bike_data = {
                'total_payment': bike_info.find('table').find_all('td')[1].find('b').text.strip(), # 支払総額
                'model_year': bike_info.find('ul').find_all('li')[0].find('b').text.strip(),       # モデル年式
                'regist_year': bike_info.find('ul').find_all('li')[1].find('b').text.strip(),      # 初度登録年
                'distance': bike_info.find('ul').find_all('li')[2].find('b').text.strip(),         # 走行距離
                'insurance': bike_info.find('ul').find_all('li')[3].find('b').text.strip(),        # 車検
                'shop_name': shop_info.find('dt').text.strip(),                                    # 販売店名
                'shop_addr': shop_info.find('dd').text.strip().split('営業時間')[0]                 # 販売店場所
            }
            self.bikes.append(self.format_bike_data(bike_data))

    def format_bike_data(self, data):
        # フォーマット「 値段, 年式, 初度登録年, 走行距離, 車検, 店名（場所） 」で出力
        return (f"{data['total_payment']}万円, {data['model_year']}, {data['regist_year']}, {data['distance']}, "
                f"{data['insurance']}, {data['shop_name']} ({data['shop_addr']})")

def clear_terminal():
    # Windowsの場合は 'cls'、それ以外のOSでは 'clear' コマンドを使用
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_terminal()

    manufacturer = input("メーカー: ").lower()
    model = input("モデル名: ").lower()
    
    scraper = GoobikeScraper(manufacturer, model)
    bike_list = scraper.scrape()

    if not bike_list:
        print("結果が見つかりません。\nメーカー名、モデル名を正しく入力してください。")
        return

    specify_year_flag = input("年式を指定するか (y/n): ").lower()
    if specify_year_flag in ['y', 'n']:
        if specify_year_flag == 'y':
            specified_year = input("年式: ")
            filtered_bike_list = [bike for bike in bike_list if specified_year in bike.split(', ')[1]]
            if not filtered_bike_list:
                print(f"指定された年式 {specified_year} のバイクは見つかりませんでした。")
                return
            else:
                bike_list = filtered_bike_list
    else:
        print("y または n を入力してください。")
        return
    
    sort_flag = input("支払総額を昇順で表示するか (y/n): ").lower()
    if sort_flag in ['y', 'n']:
        if sort_flag == 'y':
            bike_list.sort(key=lambda x: int(x.split('万円')[0].replace(',', '')))
    else:
        print("y または n を入力してください。")
        return
    
    clear_terminal()
    for bike in bike_list:
        print(bike)

if __name__ == "__main__":
    main()

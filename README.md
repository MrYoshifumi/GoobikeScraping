# GoobikeScraping

流石に業務時間内でバイク販売サイトを堂々と見るのもあれですが、

仕事中の暇な時間を利用して、グーバイクに販売中のバイクを一覧としてスクレイピングしてみた。

## まずWEBサイトの画面構成に対して調査を行おう。
グーバイク側では、データベースから抽出された結果を動的にフロント側で同じdiv構成によってloopしてレンダリングするはずです

（多分）

なので今回は、`BeautifulSoup`モジュールの`find()`または`find_all()`を利用して、特定divの内容を抽出すればいいですよ。

## 画面構成
調査した結果ですが、基本的に一台のバイクに対して、`<div class="bike_sec">`と`<div class="shop_info>`という2個のdiv要素が付与されます。

`bike_sec`はバイク情報、`shop_info`は販売店情報になっております。

```HTML
<div class="bike_sec">                  検索結果
    <div class="clear_fix">
        <div class="bike_img">          画像
        <div class="bike_info">         車体情報
            <div class="model_title">   モデル
            <div class="fav_btn">       検討ボタン
            <div class="detail_cont">   車体情報エリア
                <div class="cont01">
                    <table>             車両価格 + 支払総額
                    <ul>
                        <li> 0          モデル年式
                            <span>     「モデル年式」
                            <b>         年式数字 + 年
                        <li> 1          初度登録年
                            <span>     「初度登録年」
                            <b>         新車（在庫あり）/ 年式数字 + 年
                        <li> 2          走行距離
                            <span>     「走行距離」
                            <b>         ― / 距離数字 + Km
                        <li> 3          車検/自賠責保険
                            <span>     「車検/自賠責保険」
                            <b>         検 + yyyy/mm
                        <li> 4          修復歴
                            <span>     「修復歴」
                            <b>
                <div class="cont02">

    <div class="shop_info>
        <div class="bxl>
            <div class="shop_name">     販売店名前
                <dt>                    店名
                <dd>                    場所 ＋ 営業時間
            <div class="cus_voice">     販売店へのお客様の声
```

## 使用例
```
$ python goobike_scraper.py
メーカー: ktm
モデル名: 390_duke
年式を指定するか (y/n): y
年式: 2020
支払総額を昇順で表示するか (y/n): y
```

## 出力例
```
47万円, 2020年, 2021年, 14245Km, 検2026/01, Ｃ２０４ (大阪府守口市佐太中町３丁目９−１６ドミール佐太１Ｆ)
47万円, 2020年, 2021年, 17380Km, 検2024/08, バイク王　伊丹店 (兵庫県伊丹市北伊丹５−９６−１)
49万円, 2020年, 2020年, 19239Km, 検無し, バイク館富田林店 (大阪府富田林市喜志町５丁目４−３０)
50万円, 2020年, 2020年, 17565Km, 検2025/06, ＫＴＭ小山 (栃木県小山市雨ケ谷新田６９−１)
51万円, 2020年, 2020年, 7422Km, 検無し, ビジョギマンケーブ (埼玉県戸田市美女木４−１９−２７)
```

## 注意点
グーバイク側では検索用APIが公開されていないため、あくまでもユーザー側が見れる画面に対した調査結果になります。

また、コマンド引数で`メーカー`と`モデル名`によって自由に調べられるよう、その機能も追加しておりますが、

なぜかグーバイク側で生成された固定URLが規則的ではないと分かりました。

### 不規則なURL
最初にURLの解釈は全部`https://www.goobike.com/maker-{manufacturer}/car-{manufacturer}_{model}/index{page_number}.html`でいいと思いましたが、
一部のモデル名がアンダーバー付いてたり、付いていなかったりしています。

たまに`maker-{manufacturer}/car-{model}/index.html`の場合もあります。

以下は例です

```
https://www.goobike.com/maker-ktm/car-ktm_890smt/index.html
https://www.goobike.com/maker-ktm/car-ktm_890duke_r/index.html
https://www.goobike.com/maker-ktm/car-ktm_390_adventure/index.html
https://www.goobike.com/maker-bmw/car-bmw_f900xr/index.html
https://www.goobike.com/maker-honda/car-honda_cbr250rr/index2.html
```
作業量が増えちゃうんで、今後の課題にしておこう。

（統一しろよおい）


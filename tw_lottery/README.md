1. 找出半年前到今天，所有發行的刮刮樂。(獲得所有“下市日期”大於本月的刮刮樂)
2. 取得所有刮刮樂的期別、網址、售價
- 期別：id
- 網址：url
- 售價: price
```json
[
    {
        "url": "url1",
        "id": "id1",
        "price": "price1",
    },
    {
        "url": "url1",
        "id": "id2",
        "price": "price2",
    },
    {
        "url": "url1",
        "id": "id3",
        "price": "price3",
    },
    {
        "url": "url2",
        "id": "id3",
        "price": "price3",
    }....
]
```
3. 因為每個 url 進去後，會得到很多張刮刮樂的資訊，所以將資料整理成
- 期別：id
- 網址：url
- 售價: price
```json
{
    "url1": {
        "id1": "price1",
        "id2": "price2",
        "id3": "price3"
    },
    "url2": {
        "id4": "price4",
        "id5": "price5",
    }....
}
```
4. 進去每個網址，爬出每個 id 對應的期望值，並除以售價
- 期別：id
- 期望獎金: expected_prize
- 售價: lottery_price
- 刮刮樂名稱: name
- 期望獎金比例: prize_ratio (期望獎金/售價)
**最後記得用 prize_ratio 由高排到低**
**獎金超過 5000 塊要扣稅 20.4% ( 把獎金乘以 0.796)** 
```json
[
    {
        "id": 4404,
        "expected_prize": 149.719,
        "lottery_price": 200,
        "name": "台灣好棒",
        "prize_ratio": 0.749
    },
    {
        "id": 4420,
        "expected_prize": 736.285,
        "lottery_price": 1000,
        "name": "1,000萬大富翁",
        "prize_ratio": 0.736
    }....
]
```

---

##  修正版 (以此版本策略為主！)

1. 爬取刮刮樂總列表頁面，找出半年前到今天，所有發行的刮刮樂。(獲得所有“下市日期”大於本月的刮刮樂)
2. 取得所有刮刮樂的期別、網址、售價
- 期別：id
- 網址：url
- 售價: price
```json
[
    {
        "url": "url1",
        "id": "id1",
        "price": "price1",
    },
    {
        "url": "url1",
        "id": "id2",
        "price": "price2",
    },
    {
        "url": "url1",
        "id": "id3",
        "price": "price3",
    },
    {
        "url": "url2",
        "id": "id3",
        "price": "price3",
    }....
]
```
3. 因為每個 url 進去後，會得到很多張刮刮樂的資訊，所以將資料整理成
- 期別：id
- 網址：url
- 售價: price
```json
{
    "url1": {
        "id1": "price1",
        "id2": "price2",
        "id3": "price3"
    },
    "url2": {
        "id4": "price4",
        "id5": "price5",
    }....
}
```
4. 進去每個網址，爬出每個 id 對應的期望值，並除以售價
- 期別：id
- 期望獎金: expected_prize
- 售價: lottery_price
- 刮刮樂名稱: name
- 期望獎金比例: prize_ratio (期望獎金/售價)
**獎金超過 5000 塊要扣稅 20.4% ( 把獎金乘以 0.796)** 
**最後記得用 prize_ratio 由高排到低**
```json
[
    {
        "id": 4420,
        "expected_prize": 149.719,
        "lottery_price": 200,
        "name": "台灣好棒",
        "prize_ratio": 0.749
    },
    {
        "id": 4425,
        "expected_prize": 736.285,
        "lottery_price": 1000,
        "name": "1,000萬大富翁",
        "prize_ratio": 0.736
    }....
]
```
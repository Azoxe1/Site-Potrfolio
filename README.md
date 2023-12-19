<h1 align="center"> Сайт-портфолио </h1>
<h2>Описание</h2>
• Установлена автоматизации закупок через REST API.<br/>
• Создана визуальная составляющая<br/>
• Форма обратной связи с отбивкой на почту админам<br/>
• Подтверждение регистрации на почту указанную при регистрации<br/>
• Онлайн корзина, через КЭШ, для каждого юзера<br/>
• Динамичная вкладка с проектами<br/>
• Настроенная админка, для удобного управления сайтом<br/>
• Возможность управлением продукцией, для магазинов<br/>
• Уведомление на почту (покупателю) при изменении состава заказа<br/>

<h1 align="center"> Работа с API </h1>
<h2>Содержание</h2>
<h3>Важно</h3>
Приложение (Postman) должно использовать полученный access_token для авторизации, передавая его в заголовке в формате:
Authorization: Token ACCESS_TOKEN

<h4>Регистрация</h3>
>api/v1/registration/
> 
Обращаясь к адресу с <span style="color: orange">POST</span> запросом необходимо передать данные: ```{'username': 'user','email':'email, 'password': 'password'}```
>опциональное поле {'type': 'тип пользователя shop/buyer'}
> 

В качестве ответа будет получено: 
```{"Status": true}```<br/><br/><br/>
<h3>Авторизация</h3>
>api/v1/login/
> 
Обращаясь к адресу с <span style="color: orange">POST</span> запросом необходимо передать данные: ```{'username': 'user', 'password': 'password'}```
<br/>
В качестве ответа будет получено: ```{"Status": true, "Token": "ACCESS_TOKEN"}```<br/><br/><br/>

<h3>Информация о пользователе</h3>
>api/v1/details/
> 
При обращении с <span style="color: green">GET</span> запросом, с применением ACCESS_TOKEN.
<br/>
Ответ: Данные по юзеру, контакты, в формате Json

При обращении с <span style="color: orange">POST</span> запросом, с применением ACCESS_TOKEN. 
Для изменения описания юзера. В теле ```{'title': 'Описание'}```. <br/>
Ответ: ```{"Status": true}```<br/><br/><br/>

<h3>Подтверждение почты</h3>
>api/v1/confirm/
> 
<br/><br/><br/>

<h3>Контактная информация</h3>
>api/v1/contact/
> 
При обращении с <span style="color: green">GET</span> запросом, с применением ACCESS_TOKEN.
<br/>
Ответ: Получение контактных данных по юзеру```[
    {
        "id": ,
        "city": "",
        "street": "",
        "house": "",
        "structure": "",
        "building": "",
        "apartment": "",
        "phone": ""
    },```

При обращении с <span style="color: orange">POST</span> запросом, с применением ACCESS_TOKEN.
Для добавления новых контактных данных юзера. В теле ```{'house': 'house', 'phone': '123'}```. <br/>
Ответ: ```{"Status": true}```

При обращении с <span style="color: blue">PUT</span> запросом, с применением ACCESS_TOKEN.
Для изменения существующих контактных данных юзера. В теле ```{'поле, которое хотите изменить': 'новое значение'}```. <br/>
Ответ: ```{"Status": true}```
<br/><br/><br/>

<h3>Оформление заказа</h3>
>api/v1/order/
> 
При обращении с <span style="color: green">GET</span> запросом, с применением ACCESS_TOKEN. Просмотр существующих заказов и товаров в нём.
<br/>
Ответ: Данные по заказам юзера```[
    {
        "id": ,
        "ordered_items": [
            {
                "id": ,
                "product_name": {
                    "id": ,
                    "quantity": 
                },
            }
        ],
        "state": "",
        "dt": "",
        "contact":
,
        "state": "new",
        "dt": "2023-12-18T14:13:09.095946Z",
        "contact": {
            "id": 1,
            "city": "Дом",
            "street": "дом",
            "house": "",
            "structure": "",
            "building": "",
            "apartment": "",
            "phone": "+79688323938"
        }```

При обращении с <span style="color: orange">POST</span> запросом, с применением ACCESS_TOKEN.
Добавление нового заказа но основании корзин  ```{'id': 'id корзины','contact':'id контактов'}```. <br/>
Ответ: ```{"Status": true}```

<br/><br/><br/>

<h3>Работа с корзиной</h3>
>api/v1/cart/

При обращении с <span style="color: green">GET</span> запросом, с применением ACCESS_TOKEN. Получение состава корзины оформленного на пользователя
<br/>
Ответ: Состав корзины```[
    {
        "id": ,
        "ordered_items": [
            {
                "id": ,
                "product_name": {
                    "id": ,
                    "quantity": 
                },
            }
        ],
        "state": "",
        "dt": "",
        "contact": ```

При обращении с <span style="color: orange">POST</span> запросом, с применением ACCESS_TOKEN.
Для добавления нового товара в корзину. В теле ```{'items': [{"product_name":"id товара", "quantity":"количество"}]}```. <br/>
Ответ: ```{"Status": true}```

При обращении с <span style="color: red">DELETE</span> запросом, с применением ACCESS_TOKEN. Для удаление товара из корзины
Для изменения описания юзера. В теле ```{'items': 'id товара'}```. <br/>
Ответ: ```{"Status": true}```

При обращении с <span style="color: blue">PUT</span> запросом, с применением ACCESS_TOKEN.
Для изменения описания юзера. В теле ```{'items': [{"product":"id продукта", "quantity":"количество"}]}```. <br/>
Ответ: ```{"Status": true}```
<br/><br/><br/>
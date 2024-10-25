# Получение данных о валютах с сайта ЦБ РФ

Задача: 
1) Получить динамику курсов корейской воны, евро и доллара с 1 января 2024 года с сайта https://cbr.ru/currency_base/dynamics/    
2) Соединить их в одну таблицу в MySQL, причем курс должен быть за каждый день, если за какой-то день на сайте ЦБ нет курса, то надо взять его с прошлого дня.  

## Установка

```bash
git clone https://github.com/VadimKusakin/currencies_data.git

cd currencies_data

pip install -r requirements.txt

echo -e "MYSQL_USER=login\nMYSQL_PASSWORD=pass\nMYSQL_HOST=localhost\nMYSQL_DATABASE=my_database" > .env

source .env

docker build --build-arg MYSQL_USER=$MYSQL_USER --build-arg MYSQL_PASSWORD=$MYSQL_PASSWORD -t my_mysql_image .

docker run -d \
    --name my_mysql_container \
    -e MYSQL_ROOT_PASSWORD=$MYSQL_PASSWORD \
    -e MYSQL_DATABASE=my_database \
    -p 3306:3306 \
    my_mysql_image
```
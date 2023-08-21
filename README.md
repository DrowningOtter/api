# api

Пример загрузки файла: curl -F file=@test.txt -X POST -H 'enctype:multipart/form-data ; Content-Type:multipart/form-data' http://localhost:5000/file/test.csv
http://localhost:5000/file/filename

Для получения списка файлов с информацией о колонках нужно отправить GET запрос на адрес http://localhost:5000/file
Для получения данных из конкретного файла URL будет http://localhost:5000/file/filename
Для фильтрации по столбцам использовать query parameter filter, например, http://localhost:5000/file/results.csv?filter=home_team,away_team
Для сортировки аналогично: http://localhost:5000/file/results.csv?sort=home_team,away_team
Можно совместить: http://localhost:5000/file/results.csv?filter=home_team,away_team&sort=home_team

Для удаления файла нужно отправить DELETE запрос на адрес http://localhost:5000/file/filename

#Развертывание
python3 -m venv venv 
source venv/bin/activate
cd api
pip install -r req.txt
python3 main.py

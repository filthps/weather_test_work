" Здесь хранятся функции для создания и обработки запросов "
" При вводе города  искать город в истории (базе данных)"
" Если город не найден в истории, искать его в 2gis "
" После полного ввода его названия получить географические координты (из истории или с 2gis) "
"После получения координат делается запрос на https://open-meteo.com/"
search_city_in_our_api = () = {
    let request = new XMLHttpRequest();
    request.open("GET", "")
};
search_city_in_2gis_api = () {};
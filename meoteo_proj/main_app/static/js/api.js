" Здесь хранятся функции для создания и обработки запросов "
" При вводе города  искать город в истории (базе данных)"
" Если город не найден в истории, искать его в 2gis "
" После полного ввода его названия получить географические координаты (из истории или с 2gis) "
"После получения координат делается запрос на https://open-meteo.com/"
import {NON_SUPPORT_MODE} from "/static/js/conf.js";


var search_city_in_2gis_api = () => {};
var get_current_timezone_offset = () => {
    let offset = new Date().getTimezoneOffset()
    let o = Math.abs(offset);
    return (offset < 0 ? "+" : "-") + ("00" + Math.floor(o / 60)).slice(-2) + ":" + ("00" + (o % 60)).slice(-2);
};
console.log(get_current_timezone_offset())

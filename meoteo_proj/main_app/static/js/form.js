"Форма реагирует на событие change выполняя запрос на api - Живой поиск"
"Форма по событию submit делает запрос на получение географических координат"
" https://catalog.api.2gis.com/2.0/region/search?q=Мо&fields=items.point&key=3a5c3351-ed98-4d29-92b0-30c8d01ad7aa   ищем города"
" https://catalog.api.2gis.com/3.0/items?q=Москва&type=adm_div.city&key=3a5c3351-ed98-4d29-92b0-30c8d01ad7aa&fields=items.point получаем координаты "
const RATE = 2; // Вызов на api не чаще 1 раза в n секунд

// locker
var lock = false;
var init_locker = () => {
    var lock = true;
    setTimeOut(() => {
        var lock = false;
    }, RATE);
};
// end locker
var get_cities_input_value = () => {
    return document.forms[0].getElementsByClassName("form-control")[0].value;
};
var create_request_body = (type, item) => {
    return JSON.stringify({
        "type": type,
        "item": item
    });
};
window.onload = () => {
    var search_city_names = (e) => {
        var request = new XMLHttpRequest();
        request.open("POST",  get_search_city_api_url(), true);
        request.onload = (event) => {
            if (!event.readyState == 4) {
                return
            }
            if (!event.target.status == 200) {
                return
            }
            let task_id = JSON.parse(event.target.response)["task_id"];
            push_new_task_in_queue(task_id, "search_city");
        };
        request.setRequestHeader("X-CSRFToken", get_token());
        request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        request.setRequestHeader("content-type", "application/json");
        let text = get_cities_input_value();
        if (!text.length) {
            return
        }
        remove_all_tasks_specific_type("search_city");
        request.send(create_request_body("search_city", text));
    };
    var replace_choices_list = () => {

    };
    document.forms[0].getElementsByClassName("form-control")[0].addEventListener("change", search_city_names);
};

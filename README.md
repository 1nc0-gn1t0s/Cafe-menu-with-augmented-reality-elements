Пашкова Екатерина - "Меню для кафе с элементами дополненной реальности"

Группа: 10 - И - 3

Электронная почта: eopashkova@edu.hse.ru

Telegram: https://t.me/lnc0_gn1t0

[ НАЗВАНИЕ ПРОЕКТА ]

“Меню для кафе с элементами дополненной реальности”

[ ПРОБЛЕМНОЕ ПОЛЕ ]

Ресторанная индустрия развивается с каждым годом все больше и больше, а владельцы маленьких кафе сталкиваются с проблемами продвижения своего заведения. Иногда у них не хватает средств на создание собственного сайта и даже на печать меню. Люди, приходя в эти места, не знают, как выглядит блюдо, и бывают разочарованы его внешним видом.

[ ЗАКАЗЧИК / ПОТЕНЦИАЛЬНАЯ АУДИТОРИЯ ]

Целевая аудитория этого проекта делится на две основные группы:
1) открытые к технологиям владельцы кафе (преимущественно небольших), которые сталкиваются с проблемой продвижения своих заведений за отсутствием денег на создание сайта и печать меню;
2) посетители этих заведений, которые желают увидеть, как будет выглядеть то или иное блюдо, перед заказом.

[ АППАРАТНЫЕ / ПРОГРАММНЫЕ ТРЕБОВАНИЯ ]

Если пользователь заходит на сайт с браузера, то понадобится только он сам: Chrome, Firefox, Opera, Yandex или Safari. В этом случае у пользователя не будет возможности воспользоваться меню с элементами дополненной реальности (только с фото) и вызвать официанта.
Если пользователь заходит по QR-коду или иному маркеру, который можно отсканировать в кафе, то эти возможности появляются, но в таком случае функциональные требования немного другое:
1) На устройстве должна быть камера (но учитывая, что пользователь заходит на сайт через QR-код или другой маркер, камера наверняка есть);
2) *iOS - версия 11 и выше;
3) *Android - версия 11 и выше;
4) Один из браузеров: Chrome, Firefox, Opera, Yandex или Safari.

[ ФУНКЦИОНАЛЬНЫЕ ТРЕБОВАНИЯ ]

Программный продукт будет предоставлять следующие возможности:
1) Отображение меню кафе в режиме дополненной реальности;
2) Сохранение истории заказов пользователя;
3) Подбор рекомендаций по блюдам и заведениям на основе предпочтений пользователя и его настройкам;
4) Создание и удаление аккаунтов пользователей;
5) Редактирование информации в профиле;
6) Добавление и удаление кафе или сети кафе;
7) Создание и удаление аккаунтов админов;
8) Создание и удаление аккаунтов управляющих кафе;
9) Добавление и удаление блюд со страницы админа;
10) Получение заказов и уведомлений при вызове официанта на аккаунт управляющего соответствующего кафе.

[ ПОХОЖИЕ / АНАЛОГИЧНЫЕ ПРОДУКТЫ ]

1) https://rest.tanukifamily.ru/catalog/food/rolly - сайт сети ресторанов Тануки. В нем не реализована технология просмотра меню в режиме дополненной реальности, поэтому человек может быть разочарован внешним видом блюд (есть их фотографии, но они не показывают, например, размер блюда и то, как оно выглядит на тарелке). Также этот сайт сделан только для ресторанов Тануки (которые являются довольно популярными), поэтому он не помогает продвигать небольшие кафе. Помимо этого, этот сервис не предоставляет рекомендаций блюд, основанных на прошлых заказах. Последний недостаток заключается в том, что у пользователя сразу при входе спрашивается адрес ресторана, в котором он сидит, а также номер его столика. Заполнив эти поля, появляется возможность позвать официанта, хотя за столиком в реальности может и не сидеть никто.
2) http://menuar.ru/ - сервис с задумкой, очень похожуй на задумку моего проекта: каждое блюдо показывается в режиме дополненной реальности, причем работает с этим сервисом довольно большое количество заведений по всему миру. Тем не менее, у мего есть свои минусы: во-первых, нет возможности использовать его веб-версию, нужно скачивать приложение. Это может быть неудобно для пользователей, которые ранее не пользовались этим приложением: его прийдется качать буквально на пять минут ради просмотра меню и заказа. Во-вторых, приложение не дает рекомендаций по кафе и блюдам. Это плохо как для пользователей, так и для владельцев кафе (особенно небольших и малоизвестных): первые не смогут узнать о заведениях, которые им могут понравиться, а вторые не смогут прорекломировать свои блюда. В-третьих, при входе в приложение сразу же открывается камера. Подразумевается, что пользователь отсканирует QR-код, чтобы перейти сразу на нужную страницу, но если человек не находится в кафе в данный момент, то это может быть для него неудобно (незачем запрашивать доступ к камере и открывать ее, если она не факт, что понадобится). Помимо этого в приложении нет возможности вызвать официанта.

[ ИНСТРУМЕНТЫ РАЗРАБОТКИ, ИНФОРМАЦИЯ О БД ]

1) Базы данных / MariaDB
2) Backend:
        Python 3.8 (и выше), Flask / PyCharm
3) Frontend: HTML, CSS, JavaScript

[ ЭТАПЫ РАЗРАБОТКИ ]

1) Создание пользовательских сценариев (до конца марта);
2) Планирование и реализация базы данных (апрель);
3) Создание backend-части сервера (май - июнь);
4) Реализация интерфейса (июль);
5) Тестирование и исправление ошибок (август);
6) Подготовка проекта к защите (сентябрь).

[ ВОЗМОЖНЫЕ РИСКИ ]

1) Нестабильное интернет-соединение у пользователя.
В зависимости от скорости интернета пользователя, будет использовано меню с элементами дополненной реальности разного качества. Чем лучше интернет-соединение, тем лучше качество блюд на камере.

2) Незаинтересованность кафе в технологиях.
Бывает такое, что люди считают бумажные версии тех или иных документов лучше электронных. Такое случается по разным причинам, но основная - своего рода боязнь что-то сломать или непонимание, куда и когда нажимать. Этот риск не особо зависит от проекта, скорее от самого пользователя и его привычек. И все же решение есть. В данной ситуации им будет создание максимально простого и интуитивно понятного интерфейса.

# lab1-task-2-
Лабораторна робота №1, завдання №2
Цей модуль призначений для того, щоб створити карту де будуть позначены 10 найближчих місць, де знімалися фільми(з файлу locations.list), в рік введений користувачем, відносно координати, які вводить користувач.
Для цього я використовувала кілька бібліотек: folium(для створення карти), pandas(для відкриття csv файлу), argparse(щоб прийняти аругменти від користувача), geopy(щоб визначити координати), haversine(щоб знайти відстань), csv(для створення csv файлу).
Функції:
1.flatten(lst)
Це функція з попередніх лабораторних, я використовувала її для того, щоб зробити один список, адже часто обрізала рядки з файлу, і для мене це був найкращий варіант, щоб в списку лише містилися типу str або float.
2.parser_list(path, year_of_films)
Змінна path використовується для того, щоб отримати шлях до файла locations.list, а year_of_films для того щоб обробляти лише рядки з фільмами, зняті в році, який введе користувач. У функції наведений складний алгоритм, як парсити список, щоб отримати список списків, зручний для використання. Він напевно все одно не буде коректно парсити кожен елемент, адже є досить багато шаблонів, як саме записана інформація про фільм. Звичайно, цей алгоритм варто оптимізувати.
3.turn_into_dict(list_of_films)
Ця функція для того, щоб перетворити список в словник, де ключем є місце розташування, а значення список зі списків фільмів, знятих в цьому місці. Це допомагає не шукати повторно координати для однакових місць.
4.adding_coordinates(dict_of_films)
В цій функції додаються координати за допомогою бібліотеки geopy. Вони додаються до списку елементів кожного фільма.
5.adding_length_of_way(dict_of_films,coordinates)
В цій функції додається відстань від координат, які ввів користувач, до локації знімання фільму. Також список сортується і обрізається до 10 елементів, адже потрібно вивести не більше 10 міток. Вкінці ми отримуємо останній список, який виглядає приблизно ось так [['"#1 Single"', '2006', 'NODATA', 'Los Angeles, California, USA', (34.0536909, -118.242766)]].
6. write_csv(final_list_of_movies)
Для зручності я записала цих 10 фільмів в csv файл, адже так простіше будувати карту. Для цього я використала бібліотеку csv.
Далі відбувається виклик функцій для створення файлу movies.csv
За допомогою інформації з коротких теоретичних відомостей, я створила карту map.html з 3-ох шарів. Останнім шаром я додала інформацію про населення з коротких теоретичних відомостей, і так відповідно розфарбовані країни.
На карті є мітки, які на жаль, накладаються, адже я багато фільмів знятих в однакових місцях.
![image](https://user-images.githubusercontent.com/92806105/153639309-57643cf3-0c40-41b5-b214-05c27854bcb2.png)
Якщо натиснути на мітку, то буде виведена інформація про ці мітки.
![image](https://user-images.githubusercontent.com/92806105/153639572-746232f8-a56b-4598-a6d3-f7c7166b26c7.png)
Ось приклад запуску
![image](https://user-images.githubusercontent.com/92806105/153639819-d05cae01-318d-4cd8-a46a-9461ab39ff70.png)
loc.list це файл з меншою кількістю рядків.


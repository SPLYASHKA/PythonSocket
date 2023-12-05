# PythonSocket

Это онлайн змейка.

## Running

1. Clone the repo: `git clone https://github.com/SPLYASHKA/PythonSocket.git`
2. `cd PythonSocket`
3. `git checkout dev`
3. `pip install pygame`
4. `python3 client.py`

## Playing
Control by WASD or arrow

Игра состоит из последовательности 3 уровней, по итогам которых определяется победитель

### 1. Shared food

Два независимых поля, единственное что объединяет змеек, когда ест одна из них, размер и скорость меняется у всех

### 2. One field

Одно поле - две змеи, врезался в другую змею - проиграл

### 3. Bite another

[♫Another one bites the dust♫](https://open.spotify.com/track/2k1yPYf9WGA4LiqcLVwtzn?si=6a9d49ce36a94dc6)

Отличия от прошлого уровня:

1. Можно пройти через стену и выйти с противоположной стороны
2. Можно кусать конец чужой змейки
3. Есть ограничение по времени (если время окончилось побеждает более длинная змея)

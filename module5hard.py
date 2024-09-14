import time


class User:
    def __init__(self, nickname: str, password: int, age: int):
        self.nickname = nickname  # имя пользователя, строка
        self.password = password  # в хешированном виде, число
        self.age = age  # возраст, число

    def __hash__(self):
        return hash(self.password)

    def __str__(self):
        return self.nickname


class Video:
    def __init__(self, title: str, duration: int, time_now: int = 0, adult_mode: bool = False):
        self.title = title  # заголовок, строка
        self.duration = duration  # продолжительность, секунды
        self.time_now = time_now  # секунда остановки (изначально 0)
        self.adult_mode = adult_mode  # ограничение по возрасту, bool (False по умолчанию)

    def __eq__(self, other):
        return self.title == other.title

    def __contains__(self, item):
        return item in self.title


class UrTube:
    def __init__(self):
        self.users = []  # список объектов User
        self.videos = []  # список объектов Video
        self.current_user = None  # текущий пользователь, User

    def log_in(self, nickname: str, password: int):
        for user in self.users:
            if nickname == user.nickname and password == user.password:
                self.current_user = user
                return

    def register(self, nickname: str, password: int, age: int):
        for user in self.users:
            if nickname == user.nickname:
                print(f'Пользователь {nickname} уже существует')
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user

    def log_out(self):
        self.current_user = None

    def add(self, *args):  # args - tuple, внутри которого лежат Video
        for movie in args:  # movie это объект класса Video
            if movie.title not in [video.title for video in self.videos]:
                self.videos.append(movie)

    def get_videos(self, text: str):
        list_movie = []
        for video in self.videos:
            if text.upper() in video.title.upper():
                list_movie.append(video.title)
        return list_movie

    def watch_video(self, movie: str):
        if self.current_user:
            for video in self.videos:
                if self.current_user and self.current_user.age < 18:
                    print('Вам нет 18 лет, пожалуйста покиньте страницу')
                    return
                if movie in video.title:
                    for i in range(1, 11):
                        print(i, end=' ')
                        time.sleep(1)
                        video.time_now += 1
                    video.time_now = 0
                    print('Конец видео')

        else:
            print('Войдите в аккаунт, чтобы смотреть видео')


if __name__ == '__main__':
    ur = UrTube()
    v1 = Video('Лучший язык программирования 2024 года', 200)
    v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

    # Добавление видео
    ur.add(v1, v2)

    # Проверка поиска
    print(ur.get_videos('лучший'))
    print(ur.get_videos('ПРОГ'))

    # Проверка на вход пользователя и возрастное ограничение
    ur.watch_video('Для чего девушкам парень программист?')
    ur.register('vasya_pupkin', 'lolkekcheburek', 13)
    ur.watch_video('Для чего девушкам парень программист?')
    ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
    ur.watch_video('Для чего девушкам парень программист?')

    # Проверка входа в другой аккаунт
    ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
    print(ur.current_user)

    # Попытка воспроизведения несуществующего видео
    ur.watch_video('Лучший язык программирования 2024 года!')

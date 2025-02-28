
import time
import threading
from queue import Queue
import random

class Table:
    def __init__(self,number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self,name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(random.randint(3,10))


class Cafe:
    threads = []
    def __init__(self,*tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        guests = list(guests)
        for i in range(len(self.tables)):
            self.tables[i].guest = guests[i]
            th = guests[i]
            self.threads.append(th)
            th.start()
            print(f'{guests[i].name} сел(-а) за стол номер {self.tables[i].number}')
        if len(list(guests)) > len(self.tables):
            for i in range(len(self.tables),len(guests)):
                self.queue.put(guests[i])
                print(f'{guests[i].name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() or any([table.guest for table in self.tables]):
            for table in self.tables:
                if not table.guest is None and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                if self.queue.empty() and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'{table.guest} из очереди> вышел(-ла) из очереди и сел(-а)'
                          f' за стол номер {table.number}')
                    th = table.guest
                    th.start()
                    self.threads.append(th)


# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
 'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
 'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()




import sys

class BusStop:
    def __init__(self, name: str, latitude: float, longitude: float, time_to_next: int):
        self.name = name                      
        self.coordinates = (latitude, longitude)  
        self.time_to_next = time_to_next      
        self.next = None                      

class BusRoute:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_stop(self, name: str, latitude: float, longitude: float, time_to_next: int):
        new_stop = BusStop(name, latitude, longitude, time_to_next)
        if not self.head:
            self.head = new_stop
            self.tail = new_stop
        else:
            self.tail.next = new_stop
            self.tail = new_stop

    def total_route_time(self) -> int:
        total_time = 0
        current = self.head
        while current and current.next:  
            total_time += current.time_to_next
            current = current.next
        return total_time

    def find_stop_after_n(self, start_stop_name: str, n: int) -> str:
        current = self.head
        while current and current.name.lower() != start_stop_name.lower():
            current = current.next
        
        if not current:
            return f"Ошибка: Остановка '{start_stop_name}' не найдена в маршруте."

        for _ in range(n):
            if current.next:
                current = current.next
            else:
                return f"Маршрут завершился раньше. Автобус доедет только до конечной: '{current.name}'."
        
        return f"Через {n} ост. автобус будет на станции: '{current.name}'."

    def reverse_route(self):
        if not self.head or not self.head.next:
            return  

        stops_list = []
        current = self.head
        while current:
            stops_list.append(current)
            current = current.next

        self.head = stops_list[-1]
        self.tail = stops_list[0]
        
        for i in range(len(stops_list) - 1, 0, -1):
            stops_list[i].next = stops_list[i - 1]
            stops_list[i].time_to_next = stops_list[i - 1].time_to_next
            
        stops_list[0].next = None
        stops_list[0].time_to_next = 0

    def find_stops_within_time(self, max_time: int) -> list:
        reachable_stops = []
        current = self.head
        accumulated_time = 0

        while current:
            if accumulated_time <= max_time:
                reachable_stops.append((current.name, accumulated_time))
            else:
                break
            accumulated_time += current.time_to_next
            current = current.next
            
        return reachable_stops

    def print_route_table(self):
        if not self.head:
            print("Маршрут пуст. Сначала добавьте остановки.")
            return

        header = f"| {'Название остановки':<25} | {'Координаты':<22} | {'Время до след. (мин)':<20} |"
        separator = "-" * len(header)
        
        print(separator)
        print(header)
        print(separator)

        current = self.head
        while current:
            coord_str = f"{current.coordinates[0]}, {current.coordinates[1]}"
            print(f"| {current.name:<25} | {coord_str:<22} | {current.time_to_next:<20} |")
            current = current.next
            
        print(separator)

def main():
    route = BusRoute()

    while True:
        print("\n      MENU")
        print("1. Добавить остановку")
        print("2. Расчет общего времени маршрута")
        print("3. Определение, где будет автобус через N остановок")
        print("4. Построение обратного маршрута")
        print("5. Найти остановки, до которых автобус доедет за заданное время")
        print("6. Вывести маршрут в виде таблицы с выравниванием колонок")
        print("0. Выход")
        print()

        choice = input("Выберите команду: ").strip()
        print("-" * 50)

        if choice == "1":
            name = input("Введите название остановки: ").strip()
            try:
                lat = float(input("Введите широту (координата X): "))
                lon = float(input("Введите долготу (координата Y): "))
                time_next = int(input("Введите время до следующей остановки (в минутах): "))
                
                route.add_stop(name, lat, lon, time_next)
                print(f"Успешно: Остановка '{name}' добавлена!")
            except ValueError:
                print("Ошибка ввода! Координаты должны быть числами, а время — целым числом.")

        elif choice == "2":
            print(f"Общее время маршрута: {route.total_route_time()} минут.")

        elif choice == "3":
            if not route.head:
                print("Маршрут пуст.")
                continue
            start_stop = input("Введите название начальной остановки: ").strip()
            try:
                n = int(input("Введите количество остановок (N): "))
                print(route.find_stop_after_n(start_stop, n))
            except ValueError:
                print("Ошибка! Количество остановок должно быть целым числом.")

        elif choice == "4":
            route.reverse_route()
            print("Обратный маршрут построен успешно!")

        elif choice == "5":
            if not route.head:
                print("Маршрут пуст.")
                continue
            try:
                max_t = int(input("Введите максимальное время пути (в минутах): "))
                stops = route.find_stops_within_time(max_t)
                print(f"Остановки, доступные за {max_t} мин:")
                for stop_name, t in stops:
                    print(f" - {stop_name} (время в пути: {t} мин.)")
            except ValueError:
                print("Ошибка! Время должно быть целым числом.")

        elif choice == "6":
            route.print_route_table()

        elif choice == "0":
            print("Выход из программы. До свидания!")
            sys.exit()
            
        else:
            print("Неверная команда! Пожалуйста, выберите пункт от 0 до 6.")
if __name__ == "__main__":
    main()

import os
from models import Client, Administrator, Service, Request, Review

class ConstructionApp:
    def __init__(self):
        # Предопределённые клиенты (id, name, email, password, phone, address)
        self.clients = [
            Client(1, "Иван Иванов", "ivan@mail.com", "egoista", 79991112233, "ул. Ленина, д.52"),
            Client(2, "Василиса Васильевна", "vasia@mail.com", "password", 79992223344, "ул. Пушкина, д.2")
        ]
        # Предопределённые администраторы (id, name, email, password)
        self.admins = [
            Administrator(101, "Махач Саидович", "fifa@yandex.ru", "ronaldo"),
            Administrator(102, "Кузя Кузнецова", "olga@mail.com", "cool_admin")
        ]
        self.services = [
            Service(1, "Проектирование зданий", "Проектирование коммерческих и жилых зданий."),
            Service(2, "Ремонт помещений", "Ремонт офисных и жилых помещений."),
            Service(3, "Строительство под ключ", "Полное строительство с отделкой под ключ.")
        ]
        self.all_requests = []  # Глобальный список заявок
        self.all_reviews = []   # Глобальный список отзывов

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def login_menu(self):
        self.clear_screen()
        print("=== Вход в систему ===")
        email = input("Email: ")
        password = input("Пароль: ")

        user = None
        # Поиск среди клиентов
        for client in self.clients:
            if client.email == email and client.password == password:
                user = client
                break
        # Если не найден, поиск среди администраторов
        if not user:
            for admin in self.admins:
                if admin.email == email and admin.password == password:
                    user = admin
                    break

        if user:
            print(f"Добро пожаловать, {user.name}!")
            input("Нажмите Enter для продолжения...")
            if user.role == "Client":
                self.client_menu(user)
            elif user.role == "Administrator":
                self.admin_menu(user)
        else:
            print("Неверный email или пароль!")
            input("Нажмите Enter чтобы попробовать снова...")

    def run(self):
        while True:
            self.clear_screen()
            print("=== Строительная фирма ===")
            print("1. Войти в систему")
            print("2. Сброс пароля")
            print("3. Выход")
            choice = input("Выберите действие: ")
            if choice == "1":
                self.login_menu()
            elif choice == "2":
                self.reset_password_menu()
            elif choice == "3":
                print("До свидания!")
                break
            else:
                print("Неверный ввод!")
                input("Нажмите Enter чтобы продолжить...")

    def reset_password_menu(self):
        self.clear_screen()
        email = input("Введите ваш email для сброса пароля: ")
        user_found = None
        for user in self.clients + self.admins:
            if user.email == email:
                user_found = user
                break
        if user_found:
            user_found.resetPassword(email)
        else:
            print("Пользователь не найден.")
        input("Нажмите Enter чтобы продолжить...")

    def client_menu(self, client):
        while True:
            self.clear_screen()
            print(f"=== Меню клиента: {client.name} ===")
            print("1. Просмотреть услуги")
            print("2. Создать заявку")
            print("3. Отследить статус заявки")
            print("4. Оставить отзыв")
            print("5. Выйти")
            choice = input("Выберите действие: ")
            if choice == "1":
                self.show_services()
            elif choice == "2":
                self.handle_create_request(client)
            elif choice == "3":
                self.handle_track_request(client)
            elif choice == "4":
                self.handle_leave_review(client)
            elif choice == "5":
                client.logout()
                break
            else:
                print("Неверный ввод!")
                input("Нажмите Enter чтобы продолжить...")

    def admin_menu(self, admin):
        while True:
            self.clear_screen()
            print(f"=== Меню администратора: {admin.name} ===")
            print("1. Просмотреть все заявки")
            print("2. Обновить статус заявки")
            print("3. Принять заявку")
            print("4. Отклонить заявку")
            print("5. Просмотреть все отзывы")
            print("6. Выйти")
            choice = input("Выберите действие: ")
            if choice == "1":
                self.show_all_requests()
            elif choice == "2":
                self.handle_update_request_status(admin)
            elif choice == "3":
                self.handle_accept_request(admin)
            elif choice == "4":
                self.handle_reject_request(admin)
            elif choice == "5":
                self.show_all_reviews()
            elif choice == "6":
                admin.logout()
                break
            else:
                print("Неверный ввод!")
                input("Нажмите Enter чтобы продолжить...")

    def show_services(self):
        self.clear_screen()
        print("=== Список услуг ===")
        for service in self.services:
            service.display_info()
        input("\nНажмите Enter чтобы вернуться в меню...")

    def handle_create_request(self, client):
        self.clear_screen()
        print("=== Создание заявки ===")
        print("Выберите тип услуги:")
        for service in self.services:
            print(f"{service.id}. {service.getName()}")
        service_choice = input("Введите номер услуги: ")
        selected_service = None
        for service in self.services:
            if str(service.id) == service_choice:
                selected_service = service
                break
        if not selected_service:
            print("Неверный выбор услуги.")
            input("Нажмите Enter чтобы вернуться...")
            return
        details = input("Введите детали заявки: ")
        # Используем имя услуги как тип заявки
        request_id = client.createRequest(selected_service.getName(), details)
        # Добавляем заявку в глобальный список заявок
        for req in client.requests:
            if req.getId() == request_id:
                self.all_requests.append(req)
                break
        input("Нажмите Enter чтобы вернуться в меню...")

    def handle_track_request(self, client):
        self.clear_screen()
        print("=== Отслеживание статуса заявки ===")
        try:
            req_id = int(input("Введите ID заявки: "))
            status = client.trackRequestStatus(req_id)
            print(f"Статус заявки: {status}")
        except:
            print("Ошибка при вводе ID заявки!")
        input("Нажмите Enter чтобы вернуться в меню...")

    def handle_leave_review(self, client):
        self.clear_screen()
        print("=== Оставить отзыв ===")
        text = input("Введите текст отзыва: ")
        try:
            rating = int(input("Введите оценку (1-5): "))
            if 1 <= rating <= 5:
                client.leaveReview(text, rating)
                # Добавляем последний отзыв клиента в глобальный список
                self.all_reviews.append(client.reviews[-1])
            else:
                print("Оценка должна быть от 1 до 5!")
        except:
            print("Ошибка при введении оценки!")
        input("Нажмите Enter чтобы вернуться в меню...")

    def show_all_requests(self):
        self.clear_screen()
        print("=== Все заявки ===")
        if not self.all_requests:
            print("Нет заявок.")
        else:
            for req in self.all_requests:
                req.display_info()
        input("\nНажмите Enter чтобы вернуться в меню...")

    def handle_update_request_status(self, admin):
        self.clear_screen()
        print("=== Обновление статуса заявки ===")
        if not self.all_requests:
            print("Нет заявок для обновления.")
            input("Нажмите Enter чтобы вернуться...")
            return
        try:
            req_id = int(input("Введите ID заявки: "))
            request = None
            for req in self.all_requests:
                if req.getId() == req_id:
                    request = req
                    break
            if not request:
                print("Заявка не найдена.")
            else:
                new_status = input("Введите новый статус: ")
                admin.updateRequestStatus(request, new_status)
        except:
            print("Ошибка ввода!")
        input("Нажмите Enter чтобы вернуться в меню...")

    def handle_accept_request(self, admin):
        self.clear_screen()
        print("=== Принять заявку ===")
        if not self.all_requests:
            print("Нет заявок для принятия.")
            input("Нажмите Enter чтобы вернуться...")
            return
        try:
            req_id = int(input("Введите ID заявки: "))
            request = None
            for req in self.all_requests:
                if req.getId() == req_id:
                    request = req
                    break
            if not request:
                print("Заявка не найдена.")
            else:
                admin.acceptRequest(request)
        except:
            print("Ошибка ввода!")
        input("Нажмите Enter чтобы вернуться в меню...")

    def handle_reject_request(self, admin):
        self.clear_screen()
        print("=== Отклонить заявку ===")
        if not self.all_requests:
            print("Нет заявок для отклонения.")
            input("Нажмите Enter чтобы вернуться...")
            return
        try:
            req_id = int(input("Введите ID заявки: "))
            request = None
            for req in self.all_requests:
                if req.getId() == req_id:
                    request = req
                    break
            if not request:
                print("Заявка не найдена.")
            else:
                reason = input("Введите причину отклонения: ")
                admin.rejectRequest(request, reason)
        except:
            print("Ошибка ввода!")
        input("Нажмите Enter чтобы вернуться в меню...")

    def show_all_reviews(self):
        self.clear_screen()
        print("=== Все отзывы ===")
        if not self.all_reviews:
            print("Нет отзывов.")
        else:
            for review in self.all_reviews:
                review.display_info()
        input("\nНажмите Enter чтобы вернуться в меню...")

if __name__ == "__main__":
    app = ConstructionApp()
    app.run()

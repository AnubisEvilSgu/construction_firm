from datetime import datetime

class User:
    """Базовый класс пользователя"""
    def __init__(self, id: int, name: str, email: str, password: str, role: str):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def login(self, email: str, password: str) -> bool:
        if self.email == email and self.password == password:
            print("Поздравляем, авторизация прошла успешна!")
            return True
        print("Неправильный email или пароль!")
        return False

    def logout(self):
        print("Вы вышли из системы.")

    def resetPassword(self, email: str):
        if self.email == email:
            print(f"Ссылка для сброса пароля отправлена на {email}.")
        else:
            print("Пользователь с таким email не найден.")

    def getId(self) -> int:
        return self.id


class Client(User):
    """Класс клиента"""
    def __init__(self, id: int, name: str, email: str, password: str, phone: int, address: str):
        super().__init__(id, name, email, password, role="Client")
        self.phone = phone
        self.address = address
        self.requests = []
        self.reviews = []

    def createRequest(self, serviceType: str, details: str):
        request_id = len(self.requests) + 1  # Локальный id заявки
        new_request = Request(request_id, self, serviceType, details)
        self.requests.append(new_request)
        print(f"Заявка создана с ID: {new_request.getId()}")
        return new_request.getId()

    def trackRequestStatus(self, requestId: int) -> str:
        for req in self.requests:
            if req.getId() == requestId:
                return req.status
        return "Заявка с таким ID не найдена."

    def leaveReview(self, text: str, rating: int):
        review_id = len(self.reviews) + 1
        new_review = Review(review_id, self, text, rating)
        self.reviews.append(new_review)
        print("Отзыв успешно оставлен.")


class Administrator(User):
    """Класс администратора"""
    def __init__(self, id: int, name: str, email: str, password: str):
        super().__init__(id, name, email, password, role="Administrator")

    def updateRequestStatus(self, request, status: str):
        request.updateStatus(status)
        print(f"Статус заявки {request.getId()} обновлён на '{request.status}'.")

    def acceptRequest(self, request):
        request.updateStatus("Принята")
        print(f"Заявка {request.getId()} принята.")

    def rejectRequest(self, request, reason: str):
        request.updateStatus(f"Отклонена: {reason}")
        print(f"Заявка {request.getId()} отклонена. Причина: {reason}")


class Service:
    """Класс услуги"""
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

    def getName(self) -> str:
        return self.name

    def display_info(self):
        print(f"\nУслуга #{self.id}: {self.name}")
        print(f"Описание: {self.description}")


class Request:
    """Класс заявки"""
    def __init__(self, id: int, client: Client, serviceType: str, details: str, status: str = "Новая"):
        self.id = id
        self.client = client
        self.serviceType = serviceType
        self.details = details
        self.status = status
        self.creation_date = datetime.now()

    def updateStatus(self, newStatus: str):
        self.status = newStatus

    def getId(self) -> int:
        return self.id

    def getDetails(self) -> str:
        return self.details

    def display_info(self):
        print(f"\nЗаявка #{self.id}")
        print(f"Клиент: {self.client.name}")
        print(f"Тип услуги: {self.serviceType}")
        print(f"Детали: {self.details}")
        print(f"Статус: {self.status}")
        print(f"Дата создания: {self.creation_date.strftime('%d.%m.%Y')}")


class Review:
    """Класс отзыва"""
    def __init__(self, id: int, client: Client, text: str, rating: int):
        self.id = id
        self.client = client
        self.text = text
        self.rating = rating
        self.date = datetime.now()

    def display_info(self):
        print(f"\nОтзыв #{self.id}")
        print(f"Клиент: {self.client.name}")
        print(f"Дата: {self.date.strftime('%d.%m.%Y')}")
        print(f"Оценка: {self.rating}/5")
        print(f"Текст: {self.text}")

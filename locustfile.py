from locust import HttpUser, between, task


class ZombieDeliveryUser(HttpUser):
    # Час "думки" користувача між запитами (від 1 до 3 секунд)
    wait_time = between(1, 3)

    @task(3)
    def view_home_page(self):
        """Імітація користувача, який заходить на головну сторінку MVP"""
        self.client.get("/")

    @task(1)
    def test_login(self):
        """Імітація спроби входу користувача в систему"""
        self.client.post(
            "/auth/login",
            data={
                "username": "survivor@zombie.com",
                "password": "securepassword123",
            },
        )
from locust import task, between, FastHttpUser

class QuickstartUser(FastHttpUser):
    wait_time = between(1, 2)

    @task
    def test(self):
        self.client.post("/api/v2/login", data={"username":"admin", "password":"admin"})


from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def test(self):
        self.client.get("/api/v2/test1/")


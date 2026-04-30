"""Locust load testing configuration."""
from locust import HttpUser, task, between
import random
import json


class APIUser(HttpUser):
    """Simulated API user for load testing."""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """Initialize user session."""
        self.token = None
        self.login()
    
    def login(self):
        """Authenticate and get token."""
        response = self.client.post("/auth/login", json={
            "email": f"test{random.randint(1, 100)}@test.com",
            "password": "testpassword123"
        })
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
    
    def get_headers(self):
        """Get authorization headers."""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    @task(5)
    def get_movies(self):
        """Get movies list."""
        self.client.get("/movies", headers=self.get_headers())
    
    @task(3)
    def get_movie(self):
        """Get single movie."""
        movie_id = random.randint(1, 100)
        self.client.get(f"/movies/{movie_id}", headers=self.get_headers())
    
    @task(2)
    def get_trending(self):
        """Get trending content."""
        self.client.get("/trending", headers=self.get_headers())
    
    @task(2)
    def get_recommendations(self):
        """Get recommendations."""
        self.client.get("/recommendations", headers=self.get_headers())
    
    @task(1)
    def get_feed(self):
        """Get user feed."""
        self.client.get("/feed", headers=self.get_headers())
    
    @task(1)
    def health_check(self):
        """Check API health."""
        self.client.get("/health")


class AnonymousUser(HttpUser):
    """Simulated anonymous user for load testing."""
    
    wait_time = between(2, 5)
    
    @task(3)
    def get_movies(self):
        """Get public movies."""
        self.client.get("/movies")
    
    @task(2)
    def health_check(self):
        """Check health."""
        self.client.get("/health")
    
    @task(1)
    def get_trending(self):
        """Get trending."""
        self.client.get("/trending")

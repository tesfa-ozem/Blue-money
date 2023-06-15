# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_registration():
    mutation = """
    mutation {
        register(email: "alphatesfa789@gmail.com", password: "Abbc18") {
            id
            email
        }
    }
    """

    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    assert "errors" not in response.json()
    assert "data" in response.json()
    # Add additional assertions if needed


def test_login():
    mutation = """
    mutation = {
    login(email:"alphatesfa789@gmail.com", password:"Abbc18"){
   ... on LoginSuccess {

    accessToken
    refreshToken
    }
    ... on LoginError {
      message
    }
  }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    assert "errors" not in response.json()
    assert "data" in response.json()

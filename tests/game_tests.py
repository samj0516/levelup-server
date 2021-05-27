import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
       
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        self.gametype = GameType()
        self.gametype.type = "Board game"
        self.gametype.save()


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "type": 1,
            "difficulty_level": 5,
            "name": "Clue",
            "maker": "Milton Bradley",
            "max_players": 6,
            "min_players": 2,
            "gamer": 1
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response['name'], data['name'])
        self.assertEqual(json_response["maker"], data['maker'])
        self.assertEqual(json_response["difficulty_level"],data['difficulty_level'])
        self.assertEqual(json_response["max_players"],data['max_players'])
        self.assertEqual(json_response['min_players'], data['min_players'])
        self.assertEqual(json_response['gamer']['id'], data['gamer'])
        self.assertEqual(json_response['type']['id'], data['type'])

    
    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.type = self.gametype
        game.difficulty_level = 5
        game.name = "Monopoly"
        game.maker = "Milton Bradley"
        game.max_players = 6
        game.min_players = 2
        game.gamer_id = 1

        game.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        # Assert that the values are correct
        self.assertEqual(json_response['name'], "Monopoly")
        self.assertEqual(json_response["maker"], "Milton Bradley")
        self.assertEqual(json_response["difficulty_level"], 5)
        self.assertEqual(json_response["max_players"],6)
        self.assertEqual(json_response['min_players'], 2)
        self.assertEqual(json_response['gamer']['id'], 1)
        self.assertEqual(json_response['type']['id'], 1)

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.type = self.gametype
        game.difficulty_level = 5
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.max_players = 4
        game.min_players = 4
        game.gamer_id = 1
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "type": 1,
            "difficulty_level": 2,
            "name": "Sorry",
            "maker": "Hasbro",
            "max_players": 6,
            "min_players": 2,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["name"], "Sorry")
        self.assertEqual(json_response["maker"], "Hasbro")
        self.assertEqual(json_response["difficulty_level"], 2)
        self.assertEqual(json_response["max_players"], 6)
        self.assertEqual(json_response["min_players"], 2)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.type = self.gametype
        game.difficulty_level = 5
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.max_players = 6
        game.min_players = 2
        game.gamer_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
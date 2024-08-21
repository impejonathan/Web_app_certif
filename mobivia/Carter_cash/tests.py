from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch


from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class ProtectedPagesTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test123???')

    def test_protected_page_redirect(self):
        response = self.client.get(reverse('prediction'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('prediction')}")

    def test_successful_login_and_access(self):
        login = self.client.login(username='test', password='test123???')
        self.assertTrue(login)
        response = self.client.get(reverse('prediction'))
        self.assertEqual(response.status_code, 200)



class PredictionAPITest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test123???')
        self.client.login(username='test', password='test123???')

    @patch('requests.post')
    def test_prediction_api(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"prediction": "Résultat prédiction"}

        data = {
            "Descriptif": "MILESTONE GREENSPORT",
            "Note": "3",
            "Marque": "MILESTONE",
            "Consommation": "D",
            "Indice_Pluie": "B",
            "Bruit": 70,
            "Saisonalite": "Été",
            "Type_Vehicule": "Tourisme",
            "Runflat": "Non",
            "Largeur": 175,
            "Hauteur": 55,
            "Diametre": 15,
            "Charge": 77,
            "Vitesse": "T"
        }

        response = self.client.post(reverse('prediction'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Résultat prédiction', response.content.decode())



class ProtectedPagesRedirectTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test123???')

    def test_prediction_page_redirect_when_not_logged_in(self):
        response = self.client.get(reverse('prediction'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('prediction')}")

    def test_chatbot_page_redirect_when_not_logged_in(self):
        response = self.client.get(reverse('gpt'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('gpt')}")

    def test_variation_page_redirect_when_not_logged_in(self):
        response = self.client.get(reverse('variation'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('variation')}")

    def test_prediction_page_access_when_logged_in(self):
        self.client.login(username='test', password='test123???')
        response = self.client.get(reverse('prediction'))
        self.assertEqual(response.status_code, 200)

    def test_chatbot_page_access_when_logged_in(self):
        self.client.login(username='test', password='test123???')
        response = self.client.get(reverse('gpt'))
        self.assertEqual(response.status_code, 200)

    def test_variation_page_access_when_logged_in(self):
        self.client.login(username='test', password='test123???')
        response = self.client.get(reverse('variation'))
        self.assertEqual(response.status_code, 200)

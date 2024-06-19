from django.test import TestCase, Client
from django.urls import reverse
from Carter_cash import views

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()



    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_voiture_page(self):
        response = self.client.get(reverse('voiture'))
        self.assertEqual(response.status_code, 200)

    def test_trouver_pneu(self):
        response = self.client.get(reverse('trouver_pneu'))
        self.assertEqual(response.status_code, 200)

    def test_dimension_page(self):
        response = self.client.get(reverse('dimension'))
        self.assertEqual(response.status_code, 200)

    def test_prediction_view(self):
        response = self.client.get(reverse('prediction'))
        self.assertEqual(response.status_code, 200)

    def test_chatbot_view(self):
        response = self.client.get(reverse('gpt'))
        self.assertEqual(response.status_code, 200)

    def test_variation_page(self):
        response = self.client.get(reverse('variation'))
        self.assertEqual(response.status_code, 200)
        
        
        
        
        
    # def test_db_query(self):
    #     cnxn = views.get_db_connection()
    #     cursor = cnxn.cursor()
    #     cursor.execute("SELECT * FROM [dbo].[Produit]")
    #     rows = cursor.fetchall()
    #     self.assertGreater(len(rows), 0)
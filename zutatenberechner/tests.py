from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import geckodriver_autoinstaller
from rest_framework.test import APIRequestFactory
from .models import Card, Recipe, Ingredient


class SeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        geckodriver_autoinstaller.install()
        self.driver = WebDriver()
        self.driver.implicitly_wait(10)
        Card.objects.create(
            title="title1",
            description="desc1",
            picture="zutatenberechner/images/cards/food-865102_960_720.webp",
        )
        Recipe.objects.create(name="dummy-recipe1", description="dummy-desc1")

    def tearDown(self):
        self.driver.quit()

    def test_rezept_erstellen(self):
        """Test case to create a recipe into the database

        After filling up the forms test if the recipe and ingredient exist.
        Also test if redirected to the calculator site.
        """
        self.driver.get("%s%s" % (self.live_server_url, "/berechner/"))
        self.driver.find_element_by_link_text("Rezept erstellen").click()

        self.driver.find_element_by_name("name").send_keys("recipe1")
        self.driver.find_element_by_name("description").send_keys("desc1")

        self.driver.find_element_by_name("ingredients-0-name").send_keys("ing1")
        self.driver.find_element_by_name("ingredients-0-quantity").send_keys("2")
        self.driver.find_element_by_name("ingredients-0-unit").send_keys("Stück")

        self.driver.find_element_by_link_text("+ Zutat").click()

        self.driver.find_element_by_name("ingredients-1-name").send_keys("ing2")
        self.driver.find_element_by_name("ingredients-1-quantity").send_keys("2")
        self.driver.find_element_by_name("ingredients-1-unit").send_keys("Stück")

        self.driver.find_element_by_id("button_erstellen").click()

        self.assertIn("Berechner - Zutatenberechner", self.driver.page_source)

        self.assertTrue(Recipe.objects.filter(name="recipe1").exists())
        self.assertTrue(Ingredient.objects.filter(name="ing1").exists())
        self.assertTrue(Ingredient.objects.filter(name="ing2").exists())

    def test_rezept_hinzufügen(self):
        """Test case to add a recipe into the table which calculates the ingredients

        Search the dummy recipe and click the addButton.
        """
        self.driver.get("%s%s" % (self.live_server_url, "/berechner/"))
        self.driver.find_element_by_id("searchfield").send_keys("dummy-recipe1")
        self.driver.find_element_by_id("addButton").click()

        self.assertIn("dummy-recipe1", self.driver.page_source)

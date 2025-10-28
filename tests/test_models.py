import unittest
from src.common.db.models import Law, Article

class TestModels(unittest.TestCase):

    def test_law_model_creation(self):
        # Test if a Law object can be created
        law = Law(
            law_id="TEST001",
            law_name="Test Law",
            promulgation_number="12345",
        )
        self.assertEqual(law.law_id, "TEST001")
        self.assertEqual(law.law_name, "Test Law")

    def test_article_model_creation(self):
        # Test if an Article object can be created
        article = Article(
            article_number="1",
            article_title="Test Article",
            content="This is a test."
        )
        self.assertEqual(article.article_number, "1")
        self.assertEqual(article.content, "This is a test.")

    def test_relationship(self):
        # Test the relationship between Law and Article
        law = Law(law_id="RELTEST", law_name="Relationship Test Law")
        article1 = Article(article_number="1", article_title="First Article")
        article2 = Article(article_number="2", article_title="Second Article")

        law.articles.append(article1)
        law.articles.append(article2)

        self.assertEqual(len(law.articles), 2)
        self.assertEqual(law.articles[0].article_title, "First Article")
        self.assertEqual(article1.law, law)

if __name__ == '__main__':
    unittest.main()

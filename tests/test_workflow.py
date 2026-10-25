from src.graphs.meli_workflow import MeliWorkflow


class FakeMeli:
    def search_products(self, query, site_id, limit):
        return [{"id": "MLA1", "price": 100}, {"id": "MLA2", "price": 200}]
    def get_item(self, item_id):
        return {"id": item_id, "title": "Test item", "price": 120, "currency_id": "ARS",
                "available_quantity": 4}
    def close(self):
        pass


class FakeBedrock:
    def generate_json(self, prompt, **kwargs):
        return {"title": "Test item", "description": "Known facts only",
                "bullet_points": ["One"], "keywords": ["test"], "seo_score": 0.8}


def test_analyze_workflow_uses_live_client_results():
    result = MeliWorkflow(meli_client=FakeMeli(), bedrock_client=FakeBedrock()).analyze("test")
    assert result["status"] == "success"
    assert result["analysis"]["avg_price"] == 150


def test_listing_workflow_validates_model_output():
    result = MeliWorkflow(meli_client=FakeMeli(), bedrock_client=FakeBedrock()).generate_listing("Test item")
    assert result["listing"]["title"] == "Test item"

import httpx
import pytest

from src.tools.meli_client import MercadoLibreAPIError, MercadoLibreClient, RateLimitExceededError


def test_search_uses_site_query_and_limit():
    def handler(request):
        assert request.url.path == "/sites/MLA/search"
        assert request.url.params["q"] == "teclado"
        assert request.url.params["limit"] == "5"
        return httpx.Response(200, json={"results": [{"id": "MLA1"}]})
    http = httpx.Client(transport=httpx.MockTransport(handler))
    client = MercadoLibreClient(base_url="https://example.test", client=http)
    assert client.search_products("teclado", "MLA", 5) == [{"id": "MLA1"}]
    client.close()
    http.close()


@pytest.mark.parametrize("status,expected", [(429, RateLimitExceededError), (500, MercadoLibreAPIError)])
def test_http_errors_are_explicit(status, expected):
    http = httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(status, text="failure")))
    client = MercadoLibreClient(base_url="https://example.test", client=http)
    with pytest.raises(expected):
        client.get_item("MLA1")
    client.close()
    http.close()


def test_empty_query_rejected():
    client = MercadoLibreClient(base_url="https://example.test")
    with pytest.raises(ValueError):
        client.search_products(" ")
    client.close()

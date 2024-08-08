import aiohttp

class HTMLFetcher:
    """Fetches HTML content from web pages."""

    @staticmethod
    async def get_page_content(target_url: str) -> str:
        """Retrieve HTML content from the specified URL."""
        async with aiohttp.ClientSession() as session:
            async with session.get(target_url) as response:
                return await response.text()

class WebPageRetriever:
    """Manages the retrieval of web page content."""

    def __init__(self, target_url: str):
        """Initialize with target URL."""
        self.target_url = target_url
        self.fetcher = HTMLFetcher()

    async def fetch_content(self) -> str:
        """Fetch and return the content of the target URL."""
        return await self.fetcher.get_page_content(self.target_url)
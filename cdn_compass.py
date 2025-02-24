import sys
import asyncio
import socket
import tldextract
import argparse
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from bs4 import BeautifulSoup

async def get_cdn_info(url):
    """Uses WHOIS & Reverse DNS to detect CDN providers dynamically."""
    try:
        hostname = tldextract.extract(url).fqdn
        ip = socket.gethostbyname(hostname)
        reverse_dns = socket.getfqdn(ip)
        return f"{url} -> {reverse_dns} ({ip})"
    except Exception:
        return f"{url} -> Unknown"

async def find_cdn_links(website_url):
    """Scans a website for ALL CDN resources while bypassing HTTP2 issues."""
    cdn_links = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-http2"  # Force HTTP/1.1
        ])
        page = await browser.new_page(ignore_https_errors=True)

        # Apply stealth to bypass bot detection
        await stealth_async(page)

        # Set real browser headers to mimic human behavior
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://google.com",
        })

        try:
            await page.goto(website_url, timeout=60000, wait_until="domcontentloaded")
            content = await page.content()
        except Exception as e:
            print(f"[!] Failed to load {website_url}: {e}", file=sys.stderr)
            await browser.close()
            return []

        # Extract URLs from all script, link, and img tags
        soup = BeautifulSoup(content, "html.parser")
        for tag in soup.find_all(["script", "link", "img"]):
            src = tag.get("src") or tag.get("href")
            if src and "http" in src:
                cdn_links.add(src)

        await browser.close()

    # Get WHOIS/CDN Info for extracted links
    cdn_results = await asyncio.gather(*[get_cdn_info(url) for url in cdn_links])
    return cdn_results

async def main():
    """Reads URLs from CLI arguments, stdin (pipe), or prompts user input, then finds ALL CDN targets."""
    parser = argparse.ArgumentParser(description="Compass CDN Scanner")
    parser.add_argument("-u", "--url", help="Target website URL", required=False)
    args = parser.parse_args()

    urls = []

    # If URL is passed as an argument, use it
    if args.url:
        urls.append(args.url)
    
    # If no URL in args, check stdin (piping)
    elif not sys.stdin.isatty():
        urls = [line.strip() for line in sys.stdin if line.strip()]
    
    # If neither CLI args nor stdin, ask user
    else:
        website_url = input("[?] Enter a website URL: ").strip()
        if website_url:
            urls.append(website_url)

    if not urls:
        print("[!] No input URLs provided.", file=sys.stderr)
        sys.exit(1)

    for url in urls:
        cdn_links = await find_cdn_links(url)
        if cdn_links:
            for link in cdn_links:
                print(link)

if __name__ == "__main__":
    asyncio.run(main())
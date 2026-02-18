import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
from weasyprint import HTML
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import re

BASE = "https://www.tutorialspoint.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CATEGORIES = {
    1: ("Programming Languages", BASE + "/computer_programming_tutorials.htm"),
    2: ("Latest Technologies", BASE + "/latest_technologies.htm"),
    3: ("Machine Learning", BASE + "/machine_learning_tutorials.htm"),
    4: ("Computer Science", BASE + "/computer_science_tutorials.htm"),
    5: ("Web Development", BASE + "/web_development_tutorials.htm"),
    6: ("Mobile Development", BASE + "/mobile_development_tutorials.htm"),
    7: ("Databases", BASE + "/database_tutorials.htm"),
}

def safe_filename(name):
    name = re.sub(r"[^\w\s]", "", name)
    return re.sub(r"\s+", "_", name.strip())

def choose_category():
    print("\nAvailable Categories:\n")
    print("0. Download ALL Categories\n")
    for k, v in CATEGORIES.items():
        print(f"{k}. {v[0]}")

    choice = input("\nSelect category number: ").strip()
    if not choice.isdigit():
        return None

    choice = int(choice)
    if choice == 0:
        return "ALL"

    return CATEGORIES.get(choice)

def scan_category(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    tutorials = []
    seen = set()

    for a in soup.select("div.col-md-3 a[href$='/index.htm']"):
        title = a.select_one("h3.lib-content-title")
        if not title:
            continue

        link = urljoin(BASE, a["href"])
        if link in seen:
            continue

        seen.add(link)
        tutorials.append({
            "title": title.get_text(strip=True),
            "url": link
        })

    return tutorials

def get_chapters(index_url):
    r = requests.get(index_url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    chapters = []
    for a in soup.select("ul.toc.chapters a"):
        href = a.get("href")
        if href:
            chapters.append({
                "title": a.get_text(strip=True),
                "url": urljoin(BASE, href)
            })
    return chapters

def fix_images(container, page_url):
    for img in container.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src:
            img["src"] = urljoin(page_url, src)

def extract_content(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    main = soup.find("div", id="mainContent")
    if not main:
        return ""

    for tag in main.select(
        "script, style, .tutorial-menu, .library-page-bottom-nav, "
        ".google-right-ad, .bottom-library-ads, .cover"
    ):
        tag.decompose()

    fix_images(main, url)
    return str(main)

def extract_chapters_parallel(chapters, workers=5):
    results = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(extract_content, c["url"]): c for c in chapters}
        for f in tqdm(as_completed(futures), total=len(futures), desc="Downloading chapters"):
            c = futures[f]
            try:
                results.append((c["title"], f.result()))
            except:
                pass
    return results

def build_html(tutorial):
    html = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>",
        "body{font-family:Arial;line-height:1.6}",
        "h2{page-break-before:always}",
        "pre{background:#f4f4f4;padding:10px}",
        "img{max-width:100%;display:block;margin:10px auto}",
        "</style></head><body>",
        f"<h1>{tutorial['title']}</h1>"
    ]

    chapters = get_chapters(tutorial["url"])
    contents = extract_chapters_parallel(chapters)

    for title, content in contents:
        html.append(f"<h2>{title}</h2>")
        html.append(content)

    html.append("</body></html>")
    return "\n".join(html)

def main():
    selection = choose_category()
    if not selection:
        print("Invalid selection")
        return

    overwrite = None
    auto_all = selection == "ALL"

    categories = list(CATEGORIES.values()) if auto_all else [selection]

    for cat_name, cat_url in categories:
        print(f"\nScanning category: {cat_name}")
        tutorials = scan_category(cat_url)

        if not tutorials:
            continue

        selected = tutorials if auto_all else choose_tutorials(tutorials)

        for t in selected:
            fname = safe_filename(t["title"])
            html_path = os.path.join(OUTPUT_DIR, f"{fname}.html")
            pdf_path = os.path.join(OUTPUT_DIR, f"{fname}.pdf")

            if os.path.exists(pdf_path):
                if overwrite is None:
                    ans = input("\nFile exists. Overwrite all? [y/n]: ").lower()
                    overwrite = ans == "y"
                if not overwrite:
                    continue

            print(f"Processing {t['title']}")
            html = build_html(t)

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)

            HTML(html_path, base_url=BASE).write_pdf(pdf_path)

    print("\nDONE")

def choose_tutorials(tutorials):
    print("\nAvailable Tutorials:\n")
    print("0. Download ALL\n")
    for i, t in enumerate(tutorials, 1):
        print(f"{i}. {t['title']}")

    choice = input("\nSelect tutorials: ").strip()
    if choice == "0":
        return tutorials

    selected = []
    for p in choice.split(","):
        if p.strip().isdigit():
            idx = int(p) - 1
            if 0 <= idx < len(tutorials):
                selected.append(tutorials[idx])
    return selected

if __name__ == "__main__":
    main()

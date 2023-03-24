import logging

from bs4 import BeautifulSoup

from dootheme import Dootheme
from helper import helper
from settings import CONFIG

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


class Crawler:
    def crawl_soup(self, url):
        logging.info(f"Crawling {url}")

        html = helper.download_url(url)
        soup = BeautifulSoup(html.content, "html.parser")

        return soup

    def get_film_links(
        self,
        soup: BeautifulSoup,
        post_type: str = "tvshows",
    ) -> dict:
        film_links = {}
        if post_type == "tvshows":
            series_center = soup.find("div", class_="series-center")
            if series_center:
                fullsfeatures = series_center.find_all("div", class_="fullsfeature")
                for fullsfeature in fullsfeatures:
                    span = fullsfeature.find("span")
                    episode_title = "" if not span else span.text.strip()

                    episode_links = {}
                    lis = fullsfeature.find_all("li")
                    for li in lis:
                        a_fsctab = li.find("a", class_="fsctab")
                        if not a_fsctab:
                            continue

                        link_server = li.text.strip()
                        link_href = a_fsctab.get("href")
                        episode_links[link_server] = link_href

                    film_links[episode_title] = episode_links
        else:
            primary_nav_wrap = soup.find("nav", {"id": "primary_nav_wrap"})
            child_lis = primary_nav_wrap.select("ul > li", recursive=False)

            for li in child_lis:
                child_ul = li.find("ul")
                if not child_ul:
                    continue

                server_links = {}
                child_ul_lis = child_ul.find_all("li")
                for child_ul_li in child_ul_lis:
                    link = child_ul_li.find("a")
                    if link:
                        name = child_ul_li.text.strip()
                        server_links[name] = link.get("href")

                child_ul.extract()
                server_name = li.text.strip()

                film_links[server_name] = server_links

        return film_links

    def crawl_film(
        self,
        href: str,
        title: str,
        cover_img_src: str,
        post_type: str = "tvshows",
    ):
        soup = self.crawl_soup(href)
        fmain = soup.find("div", class_="fmain")

        description = helper.get_description_from(fmain=fmain)

        trailer_id = helper.get_trailer_id(soup)
        extra_info = helper.get_extra_info_from(fmain=fmain)

        if not title:
            helper.error_log(
                msg=f"No title was found\n{href}", log_file="base.no_title.log"
            )
            return

        film_data = {
            "title": title,
            "description": description,
            "post_type": post_type,
            "trailer_id": trailer_id,
            "fondo_player": cover_img_src,
            "poster_url": cover_img_src,
            "extra_info": extra_info,
        }

        # extra_key_file = f"json/{post_type}_extra.json"
        # extra_key = []
        # if Path(extra_key_file).is_file():
        #     extra_key = json.loads(open(extra_key_file, "r").read())

        # new_extra_key = list(set([*extra_key, *film_data["extra_info"].keys()]))
        # with open(extra_key_file, "w") as f:
        #     f.write(json.dumps(new_extra_key, indent=4, ensure_ascii=False))

        film_links = self.get_film_links(soup, post_type)
        return [film_data, film_links]

    def crawl_page(
        self, url: str = CONFIG.FRENCH_STREAM_SERIES, post_type: str = "tvshows"
    ):
        soup = self.crawl_soup(url)
        if not soup:
            return 0

        dle_content = soup.find("div", {"id": "dle-content"})
        if not dle_content:
            return 0

        shorts = dle_content.find_all("div", class_="short")
        if not shorts:
            return 0

        for short in shorts:
            try:
                a_element = short.find("a", class_="short-poster")

                href = a_element.get("href")
                if "http" not in href:
                    href = CONFIG.FRENCH_STREAM_HOMEPAGE + href

                title = a_element.find("div", class_="short-title")
                title = "" if not title else title.text.replace("\n", "").strip()

                cover_img_src = a_element.find("img")
                cover_img_src = "" if not cover_img_src else cover_img_src.get("src")

                film_data, film_links = self.crawl_film(
                    href=href,
                    title=title,
                    cover_img_src=cover_img_src,
                    post_type=post_type,
                )

                Dootheme(film_data, film_links).insert_film()
            except Exception as e:
                helper.error_log(f"Failed to get href\n{short}\n{e}", "page.log")

        return 1


if __name__ == "__main__":
    Crawler().crawl_page(CONFIG.FRENCH_STREAM_SERIES + "/page/111/")
    # Crawler().crawl_page(CONFIG.FRENCH_STREAM_MOVIES, post_type="movies")
    # Crawler_Site().crawl_episodes(
    #     1, "https://series9.la/film/country-queen-season-1/watching.html", "", "", ""
    # )

    # Crawler_Site().crawl_film("https://series9.la/film/the-masked-dancer-season-2-uk")
    # Crawler_Site().crawl_film(
    #     "https://series9.la/film/the-curse-of-oak-island-season-10"
    # )
    # Crawler_Site().crawl_film("https://series9.la//film/crossing-lines-season-3-wds")

    # Crawler_Site().crawl_film(
    #     "https://series9.la//film/ghost-adventures-bwm", post_type="post"
    # )

    # Crawler_Site().crawl_film("https://series9.la//film/ghost-adventures-season-1-utc")

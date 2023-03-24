import base64
import logging
import re
from datetime import datetime, timedelta
from html import escape
from pathlib import Path
from time import sleep

from phpserialize import serialize, unserialize
from slugify import slugify

from _db import database
from helper import helper
from settings import CONFIG

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)

EPISODE_COVER = False

KEY_MAPPING = {
    "Réalisé par": "dtcreator",
    "Avec": "dtcast",
    "Acteurs": "dtcast",
    "Genre": "genres",
    "Réalisateur": "dtcreator",
}


TAXONOMIES = {
    "movies": [
        "genres",
        "dtcast",
        # "cast_tv",
        # "gueststar",
        "dtdirector",
        # "directors_tv",
        # "country",
        "dtyear",
    ],
    "tvshows": [
        "genres",
        # "cast",
        "dtcast",
        # "gueststar",
        # "directors",
        "dtcreator",
        # "country",
        "dtyear",
    ],
}


class DoothemeHelper:
    def get_episode_title_and_language_and_number(self, episode_title: str) -> str:
        title = episode_title.lower()

        if title.endswith("en vf"):
            language = "VF"
            title = title.replace("en vf", "").strip()

        elif title.endswith("en vostfr"):
            language = "VOSTFR"
            title = title.replace("en vostfr", "").strip()
        else:
            language = "VO"

        pattern = r"épisode\s(\d+(\.\d+)?)"
        match = re.search(pattern, title)
        if match:
            number = match.group(1)
        else:
            self.error_log(
                msg=f"Unknown episode number for: {title}",
                log_file="toroplay_get_episode_title_and_language_and_number.log",
            )
            number = ""

        title = title.title()

        return [title, language, number]

    def generate_trglinks(
        self,
        server: str,
        link: str,
        lang: str = "English",
        quality: str = "HD",
    ) -> str:
        if "http" not in link:
            link = "https:" + link

        server_term_id, isNewServer = self.insert_terms(
            post_id=0, terms=server, taxonomy="server"
        )

        lang_term_id, isNewLang = self.insert_terms(
            post_id=0, terms=lang, taxonomy="language"
        )

        quality_term_id, isNewQuality = self.insert_terms(
            post_id=0, terms=quality, taxonomy="quality"
        )

        link_data = {
            "type": "1",
            "server": str(server_term_id),
            "lang": int(lang_term_id),
            "quality": int(quality_term_id),
            "link": base64.b64encode(bytes(escape(link), "utf-8")).decode("utf-8"),
            "date": self.get_timeupdate().strftime("%d/%m/%Y"),
        }
        link_data_serialized = serialize(link_data).decode("utf-8")

        return f's:{len(link_data_serialized)}:"{link_data_serialized}";'

    def format_text(self, text: str) -> str:
        return text.strip("\n").replace('"', "'").strip()

    def error_log(self, msg: str, log_file: str = "failed.log"):
        datetime_msg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Path("log").mkdir(parents=True, exist_ok=True)
        with open(f"log/{log_file}", "a") as f:
            print(f"{datetime_msg} LOG:  {msg}\n{'-' * 80}", file=f)

    def get_season_number(self, strSeason: str) -> int:
        strSeason = strSeason.split(" ")[0]
        res = ""
        for ch in strSeason:
            if ch.isdigit():
                res += ch

        return res

    def get_episode_title_and_language_and_number(self, episode_title: str) -> str:
        title = episode_title.lower()

        if title.endswith("en vf"):
            language = "VF"
            title = title.replace("en vf", "").strip()

        elif title.endswith("en vostfr"):
            language = "VOSTFR"
            title = title.replace("en vostfr", "").strip()
        else:
            language = "VO"

        pattern = r"épisode\s(\d+(\.\d+)?)"
        match = re.search(pattern, title)
        if match:
            number = match.group(1)
        else:
            self.error_log(
                msg=f"Unknown episode number for: {title}",
                log_file="toroplay_get_episode_title_and_language_and_number.log",
            )
            number = ""

        title = title.title()

        return [title, language, number]

    def get_title_and_season_number(self, title: str) -> list:
        title = title
        season_number = "1"

        try:
            for seasonSplitText in CONFIG.SEASON_SPLIT_TEXTS:
                if seasonSplitText in title:
                    title, season_number = title.split(seasonSplitText)
                    break

        except Exception as e:
            self.error_log(
                msg=f"Failed to find title and season number\n{title}\n{e}",
                log_file="toroplay.get_title_and_season_number.log",
            )

        return [
            self.format_text(title),
            self.get_season_number(self.format_text(season_number)),
        ]

    def insert_postmeta(self, postmeta_data: list, table: str = "postmeta"):
        database.insert_into(
            table=f"{CONFIG.TABLE_PREFIX}{table}", data=postmeta_data, is_bulk=True
        )

    def generate_film_data(
        self,
        title,
        description,
        post_type,
        trailer_id,
        fondo_player,
        poster_url,
        extra_info,
    ):
        post_data = {
            "description": description,
            "title": title,
            "post_type": post_type,
            # "id": "202302",
            "youtube_id": f"{trailer_id}",
            # "serie_vote_average": extra_info["IMDb"],
            # "episode_run_time": extra_info["Duration"],
            "fondo_player": fondo_player,
            "poster_url": poster_url,
            # "category": extra_info["Genre"],
            # "stars": extra_info["Actor"],
            # "director": extra_info["Director"],
            # "release-year": [extra_info["Release"]],
            # "country": extra_info["Country"],
        }

        key_mapping = {
            "Réalisé par": "cast",
            "Avec": "cast",
            "Acteurs": "cast",
            "Genre": "category",
            "Date de sortie": "annee",
            "Réalisateur": "directors",
        }

        for info_key in key_mapping.keys():
            if info_key in extra_info.keys():
                post_data[key_mapping[info_key]] = extra_info[info_key]

        for info_key in ["cast", "directors"]:
            if info_key in post_data.keys():
                post_data[f"{info_key}_tv"] = post_data[info_key]

        return post_data

    def get_timeupdate(self) -> datetime:
        timeupdate = datetime.now() - timedelta(hours=7)

        return timeupdate

    def generate_post(self, post_data: dict) -> tuple:
        timeupdate = self.get_timeupdate()
        data = (
            0,
            timeupdate.strftime("%Y/%m/%d %H:%M:%S"),
            timeupdate.strftime("%Y/%m/%d %H:%M:%S"),
            post_data["description"],
            post_data["title"],
            "",
            "publish",
            "open",
            "open",
            "",
            slugify(post_data["title"]),
            "",
            "",
            timeupdate.strftime("%Y/%m/%d %H:%M:%S"),
            timeupdate.strftime("%Y/%m/%d %H:%M:%S"),
            "",
            0,
            "",
            0,
            post_data["post_type"],
            "",
            0,
        )
        return data

    def insert_post(self, post_data: dict) -> int:
        data = self.generate_post(post_data)
        post_id = database.insert_into(table=f"{CONFIG.TABLE_PREFIX}posts", data=data)
        return post_id

    def insert_film(self, post_data: dict) -> int:
        try:
            post_id = self.insert_post(post_data)
            timeupdate = self.get_timeupdate()

            postmeta_data = [
                (post_id, "_edit_last", "1"),
                (post_id, "_edit_lock", f"{int(timeupdate.timestamp())}:1"),
                # _thumbnail_id
                (post_id, "tr_post_type", "2"),
                (post_id, "field_title", post_data["title"]),
                # (
                #     post_id,
                #     "field_trailer",
                #     CONFIG.YOUTUBE_IFRAME.format(post_data["youtube_id"]),
                # ),
                (
                    post_id,
                    "poster_hotlink",
                    post_data["poster_url"],
                ),
                (
                    post_id,
                    "backdrop_hotlink",
                    post_data["fondo_player"],
                ),
            ]

            if "rating" in post_data.keys():
                postmeta_data.append((post_id, "rating", post_data["rating"]))

            tvseries_postmeta_data = [
                (
                    post_id,
                    "number_of_seasons",
                    "0",
                ),
                (
                    post_id,
                    "number_of_episodes",
                    "0",
                ),
            ]
            movie_postmeta_data = []

            if "annee" in post_data.keys():
                annee = (
                    post_id,
                    "field_date",
                    post_data["annee"][0],
                )

                tvseries_postmeta_data.append(annee)
                movie_postmeta_data.append(annee)

            if "field_runtime" in post_data.keys():
                tvseries_postmeta_data.append(
                    (
                        post_id,
                        "field_runtime",
                        "a:1:{i:0;i:" + post_data["field_runtime"] + ";}",
                    )
                )

                movie_postmeta_data.append(
                    (post_id, "field_runtime", f"{post_data['field_runtime']}m"),
                )

            if post_data["post_type"] == "series":
                postmeta_data.extend(tvseries_postmeta_data)
            else:
                postmeta_data.extend(movie_postmeta_data)

            self.insert_postmeta(postmeta_data)

            for taxonomy in CONFIG.TAXONOMIES[post_data["post_type"]]:
                if taxonomy in post_data.keys() and post_data[taxonomy]:
                    self.insert_terms(
                        post_id=post_id, terms=post_data[taxonomy], taxonomy=taxonomy
                    )

            return post_id
        except Exception as e:
            self.error_log(
                f"Failed to insert film\n{e}", log_file="toroplay.insert_film.log"
            )

    def format_condition_str(self, equal_condition: str) -> str:
        return equal_condition.replace("\n", "").strip().lower()

    def insert_terms(
        self,
        post_id: int,
        terms: str,
        taxonomy: str,
        is_title: str = False,
        term_slug: str = "",
    ):
        terms = [term.strip() for term in terms.split(",")] if not is_title else [terms]
        termIds = []
        for term in terms:
            term_slug = slugify(term_slug) if term_slug else slugify(term)
            cols = "tt.term_taxonomy_id, tt.term_id"
            table = (
                f"{CONFIG.TABLE_PREFIX}term_taxonomy tt, {CONFIG.TABLE_PREFIX}terms t"
            )
            condition = f't.slug = "{term_slug}" AND tt.term_id=t.term_id AND tt.taxonomy="{taxonomy}"'

            be_term = database.select_all_from(
                table=table, condition=condition, cols=cols
            )
            if not be_term:
                term_id = database.insert_into(
                    table=f"{CONFIG.TABLE_PREFIX}terms",
                    data=(term, term_slug, 0),
                )
                term_taxonomy_id = database.insert_into(
                    table=f"{CONFIG.TABLE_PREFIX}term_taxonomy",
                    data=(term_id, taxonomy, "", 0, 0),
                )
                termIds = [term_taxonomy_id, True]
            else:
                term_taxonomy_id = be_term[0][0]
                term_id = be_term[0][1]
                termIds = [term_taxonomy_id, False]

            try:
                database.insert_into(
                    table=f"{CONFIG.TABLE_PREFIX}term_relationships",
                    data=(post_id, term_taxonomy_id, 0),
                )
            except:
                pass

        return termIds


doohelper = DoothemeHelper()


class Dootheme:
    def __init__(self, film: dict, film_links: dict):
        self.film = film
        self.film["quality"] = self.film["extra_info"].get("Quality", "HD")

        self.film_links = film_links

    def format_slug(self, slug: str) -> str:
        return slug.replace("’", "").replace("'", "")

    def format_condition_str(self, equal_condition: str) -> str:
        return equal_condition.replace("\n", "").strip().lower()

    def insert_postmeta(self, postmeta_data: list, table: str = "postmeta"):
        logging.info(f"Inserting postmeta into table {table}")
        database.insert_into(
            table=f"{CONFIG.TABLE_PREFIX}{table}", data=postmeta_data, is_bulk=True
        )

    def insert_terms(self, post_id: int, terms: list, taxonomy: str):
        termIds = []
        for term in terms:
            term_name = self.format_condition_str(term)
            cols = "tt.term_taxonomy_id, tt.term_id"
            table = (
                f"{CONFIG.TABLE_PREFIX}term_taxonomy tt, {CONFIG.TABLE_PREFIX}terms t"
            )
            condition = f't.name = "{term_name}" AND tt.term_id=t.term_id AND tt.taxonomy="{taxonomy}"'

            be_term = database.select_all_from(
                table=table, condition=condition, cols=cols
            )
            if not be_term:
                term_id = database.insert_into(
                    table=f"{CONFIG.TABLE_PREFIX}terms",
                    data=(term, slugify(term), 0),
                )
                termIds = [term_id, True]
                term_taxonomy_id = database.insert_into(
                    table=f"{CONFIG.TABLE_PREFIX}term_taxonomy",
                    data=(term_id, taxonomy, "", 0, 0),
                )
            else:
                term_taxonomy_id = be_term[0][0]
                term_id = be_term[0][1]
                termIds = [term_id, False]

            try:
                database.insert_into(
                    table=f"{CONFIG.TABLE_PREFIX}term_relationships",
                    data=(post_id, term_taxonomy_id, 0),
                )
            except:
                pass

        return termIds

    def insert_movie_details(self, post_id):
        if not self.film_links:
            return

        logging.info("Inserting movie players")
        movie_links = {}
        for server_name, server_links in self.film_links.items():
            for language, link in server_links.items():
                if not link:
                    continue

                movie_links.setdefault(language, {})
                movie_links[language][server_name] = link

        postmeta_data = [
            (
                post_id,
                "repeatable_fields",
                self.generate_repeatable_fields(movie_links),
            )
        ]

        if (
            "Country" in self.film["extra_info"].keys()
            and self.film["extra_info"]["Country"]
        ):
            postmeta_data.append(
                (post_id, "Country", self.film["extra_info"]["Country"][0]),
            )

        self.insert_postmeta(postmeta_data)

    def generate_film_data(
        self,
        title,
        description,
        post_type,
        trailer_id,
        fondo_player,
        poster_url,
        extra_info,
    ):
        post_data = {
            "description": description,
            "title": title,
            "post_type": post_type,
            # "id": "202302",
            "youtube_id": "[]",
            # "serie_vote_average": extra_info["IMDb"],
            # "episode_run_time": extra_info["Duration"],
            "dt_backdrop": fondo_player,
            "dt_poster": poster_url,
            # "imdbRating": extra_info["IMDb"],
            # "stars": extra_info["Actor"],
            # "director": extra_info["Director"],
            # "release-year": [extra_info["Release"]],
            # "country": extra_info["Country"],
        }

        for info_key in KEY_MAPPING.keys():
            if info_key in extra_info.keys():
                post_data[KEY_MAPPING[info_key]] = extra_info[info_key].split(",")
        if "Date de sortie" in extra_info.keys():
            post_data["dtyear"] = [extra_info["Date de sortie"]]

        if "dtcreator" in post_data.keys():
            post_data["dtdirector"] = post_data["dtcreator"]

        return post_data

    def get_timeupdate(self) -> datetime:
        timeupdate = datetime.now() - timedelta(hours=7)

        return timeupdate

    def generate_post(self, post_data: dict) -> tuple:
        timeupdate = self.get_timeupdate()
        data = (
            0,
            timeupdate.strftime("%Y/%m/%d %H:%M:%S"),
            (timeupdate - timedelta(hours=2)).strftime("%Y/%m/%d %H:%M:%S"),
            post_data["description"],
            post_data["title"],
            "",
            "publish",
            "open",
            "open",
            "",
            slugify(self.format_slug(post_data["title"])),
            "",
            "",
            timeupdate.strftime("%Y/%m/%d %H:%M:%S"),
            (timeupdate - timedelta(hours=2)).strftime("%Y/%m/%d %H:%M:%S"),
            "",
            0,
            "",
            0,
            post_data["post_type"],
            "",
            0,
        )
        return data

    def insert_post(self, post_data: dict) -> int:
        data = self.generate_post(post_data)
        post_id = database.insert_into(table=f"{CONFIG.TABLE_PREFIX}posts", data=data)
        return post_id

    def insert_film_to_database(self, post_data: dict) -> int:
        try:
            post_id = self.insert_post(post_data)
            timeupdate = self.get_timeupdate()

            postmeta_data = [
                (
                    post_id,
                    "youtube_id",
                    post_data["youtube_id"],
                ),
                (
                    post_id,
                    "dt_poster",
                    post_data["dt_poster"],
                ),
                (
                    post_id,
                    "dt_backdrop",
                    post_data["dt_backdrop"],
                ),
                (post_id, "original_name", post_data["title"]),
                (post_id, "_edit_last", "1"),
                (post_id, "_edit_lock", f"{int(timeupdate.timestamp())}:1"),
                # _thumbnail_id
                # (
                #     post_id,
                #     "poster_hotlink",
                #     post_data["poster_url"],
                # ),
                # (
                #     post_id,
                #     "backdrop_hotlink",
                #     post_data["fondo_player"],
                # ),
            ]

            tvseries_postmeta_data = [
                (post_id, "ids", post_id),
                (post_id, "clgnrt", "1"),
            ]
            movie_postmeta_data = []

            if "episode_run_time" in post_data.keys():
                movie_postmeta_data.append(
                    (post_id, "runtime", post_data["episode_run_time"]),
                )

            for key in ["episode_run_time", "imdbRating"]:
                if key in post_data.keys():
                    tvseries_postmeta_data.append(
                        (
                            post_id,
                            key,
                            post_data[key],
                        )
                    )

            if post_data["post_type"] == "tvshows":
                postmeta_data.extend(tvseries_postmeta_data)
            else:
                postmeta_data.extend(movie_postmeta_data)

            self.insert_postmeta(postmeta_data)

            for taxonomy in TAXONOMIES[post_data["post_type"]]:
                if taxonomy in post_data.keys() and post_data[taxonomy]:
                    self.insert_terms(
                        post_id=post_id, terms=post_data[taxonomy], taxonomy=taxonomy
                    )

            return post_id
        except Exception as e:
            helper.error_log(f"Failed to insert film\n{e}")

    def insert_root_film(self) -> list:
        condition_post_title = self.film["post_title"].replace("'", "''")
        condition = f"""post_title = '{condition_post_title}' AND post_type='{self.film["post_type"]}'"""
        be_post = database.select_all_from(
            table=f"{CONFIG.TABLE_PREFIX}posts", condition=condition
        )
        if not be_post:
            logging.info(f'Inserting root film: {self.film["post_title"]}')
            post_data = self.generate_film_data(
                self.film["post_title"],
                self.film["description"],
                self.film["post_type"],
                self.film["trailer_id"],
                self.film["fondo_player"],
                self.film["poster_url"],
                self.film["extra_info"],
            )

            return [self.insert_film_to_database(post_data), True]
        else:
            return [be_post[0][0], False]

    def update_season_number_of_episodes(self, season_term_id, number_of_episodes):
        try:
            condition = f"term_id={season_term_id} AND meta_key='number_of_episodes'"
            be_number_of_episodes = database.select_all_from(
                table=f"{CONFIG.TABLE_PREFIX}termmeta",
                condition=condition,
                cols="meta_value",
            )[0][0]
            if int(be_number_of_episodes) < number_of_episodes:
                database.update_table(
                    table=f"{CONFIG.TABLE_PREFIX}termmeta",
                    set_cond=f"meta_value={number_of_episodes}",
                    where_cond=condition,
                )
        except Exception as e:
            helper.error_log(
                msg=f"Error while update_season_number_of_episodes\nSeason {season_term_id} - Number of episodes {number_of_episodes}\n{e}",
                log_file="torotheme.update_season_number_of_episodes.log",
            )

    def generate_repeatable_fields(self, video_links: dict) -> str:
        video_players = {}
        i = 0
        for language, server_links in video_links.items():
            for server_name, link in server_links.items():
                video_players[i] = {
                    "name": f"{language} - {server_name}".upper(),
                    # "select": "iframe", URL Embed
                    "select": "dtshcode",
                    "idioma": "",
                    # "url": link, URL Embed
                    "url": CONFIG.IFRAME.format(link),
                }
                i += 1

        video_players_serialize = serialize(video_players)

        return video_players_serialize.decode("utf-8")

    def format_serie_film_links(self):
        new_film_links = {}
        for episode_title, episode_links in self.film_links.items():
            is_has_link = False
            for server, link in episode_links.items():
                if link:
                    is_has_link = True
                    break

            if not is_has_link:
                continue

            (
                episode_title,
                language,
                episode_number,
            ) = doohelper.get_episode_title_and_language_and_number(
                episode_title=episode_title
            )
            if not episode_number:
                continue

            new_film_links.setdefault(episode_number, {})
            new_film_links[episode_number]["title"] = episode_title

            new_film_links[episode_number].setdefault("video_links", {})
            new_film_links[episode_number]["video_links"][language] = episode_links

        return new_film_links

    def insert_episodes(self, post_id: int, season_id: int):
        self.film_links = self.format_serie_film_links()

        # self.update_season_number_of_episodes(season_id, lenEpisodes)

        for episode_number, episode in self.film_links.items():
            episode_title = episode["title"]

            episode_name = (
                self.film["post_title"]
                + f': {self.film["season_number"]}x{episode_number}'
            )
            condition_post_title = episode_name.replace("'", "''")
            condition = (
                f"""post_title = '{condition_post_title}' AND post_type='episodes'"""
            )
            be_post = database.select_all_from(
                table=f"{CONFIG.TABLE_PREFIX}posts", condition=condition
            )
            if not be_post:
                logging.info(f"Inserting episodes: {episode_name}")
                post_data = self.generate_film_data(
                    episode_name,
                    "",
                    "episodes",
                    self.film["trailer_id"],
                    self.film["fondo_player"],
                    self.film["poster_url"],
                    self.film["extra_info"],
                )

                episode_id = self.insert_post(post_data)
                episode_postmeta = [
                    (
                        episode_id,
                        "temporada",
                        self.film["season_number"],
                    ),
                    (
                        episode_id,
                        "episodio",
                        episode_number,
                    ),
                    (
                        episode_id,
                        "serie",
                        self.film["post_title"],
                    ),
                    (
                        episode_id,
                        "episode_name",
                        episode_title,
                    ),
                    (episode_id, "ids", post_id),
                    (episode_id, "clgnrt", "1"),
                    (
                        episode_id,
                        "repeatable_fields",
                        self.generate_repeatable_fields(episode["video_links"]),
                    ),
                    (episode_id, "_edit_last", "1"),
                    (
                        episode_id,
                        "_edit_lock",
                        f"{int(self.get_timeupdate().timestamp())}:1",
                    ),
                ]

                if EPISODE_COVER:
                    episode_postmeta.append(
                        (
                            episode_id,
                            "dt_backdrop",
                            self.film["poster_url"],
                        )
                    )

                # if "air_date" in self.film.keys():
                #     episode_postmeta.append(
                #         (
                #             episode_id,
                #             "air_date",
                #             self.film["air_date"],
                #         )
                #     )

                self.insert_postmeta(episode_postmeta)

    def insert_season(self, post_id: int):
        season_name = self.film["post_title"] + ": Season " + self.film["season_number"]
        condition_post_title = season_name.replace("'", "''")
        condition = f"""post_title = '{condition_post_title}' AND post_type='seasons'"""
        be_post = database.select_all_from(
            table=f"{CONFIG.TABLE_PREFIX}posts", condition=condition
        )
        if not be_post:
            logging.info(f"Inserting season: {season_name}")
            post_data = self.generate_film_data(
                season_name,
                self.film["description"],
                "seasons",
                self.film["trailer_id"],
                self.film["fondo_player"],
                self.film["poster_url"],
                self.film["extra_info"],
            )

            season_id = self.insert_post(post_data)
            season_postmeta = [
                (
                    season_id,
                    "temporada",
                    self.film["season_number"],
                ),
                (
                    season_id,
                    "serie",
                    self.film["post_title"],
                ),
                (
                    season_id,
                    "dt_poster",
                    self.film["poster_url"],
                ),
                (season_id, "ids", post_id),
                (season_id, "clgnrt", "1"),
                (season_id, "_edit_last", "1"),
                (
                    season_id,
                    "_edit_lock",
                    f"{int(self.get_timeupdate().timestamp())}:1",
                ),
            ]

            # if "air_date" in self.film.keys():
            #     season_postmeta.append(
            #         (
            #             season_id,
            #             "air_date",
            #             self.film["air_date"],
            #         )
            #     )

            self.insert_postmeta(season_postmeta)

            return season_id
        else:
            return be_post[0][0]

    def insert_film(self):
        (
            self.film["post_title"],
            self.film["season_number"],
        ) = doohelper.get_title_and_season_number(self.film["title"])

        post_id, isNewPostInserted = self.insert_root_film()
        logging.info("Root film ID: %s", post_id)

        if self.film["post_type"] != "tvshows":
            if isNewPostInserted:
                self.insert_movie_details(post_id)
        else:
            season_term_id = self.insert_season(post_id)
            self.insert_episodes(post_id, season_term_id)

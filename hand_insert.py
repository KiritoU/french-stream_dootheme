import logging

from toroplay import Toroplay

film_data = {
    "title": "Game Of Thrones - Season 1",
    "description": "Game of Thrones is based on the novel A Game of Thrones by George R R Martin. Lord Eddard Stark is summoned to court by his old friend, King Robert Baratheon, to serve as the King';;s Hand. Across the narrow sea in Essos, the exiled Prince Viserys Targaryen forges a new alliance to regain the Iron Throne. But in a land where seasons can last a lifetime, winter is coming...and beyond the Great Wall that protects them, a forgotten evil has returned.",
    "post_type": "tvshows",
    "trailer_id": "iGp_N3Ir7Do",
    "fondo_player": "https://cdn.themovieseries.net/",
    "poster_url": "https://cdn.themovieseries.net//game-of-thrones-season-1-zni/cover.png",
    "extra_info": {
        "Genre": ["Drama", "History", "War"],
        "Actor": ["Peter Dinklage", "Kit Harington", "Emilia Clarke"],
        "Director": ["D.B. Weiss, David Benioff"],
        "Country": ["United States"],
        "Duration": "44",
        "Quality": "HD",
        "Release": "2013",
        "IMDb": "9.5",
    },
}

episodes_data = {
    "10": {
        "title": "Game Of Thrones - Season 1 Episode 10: Fire and Blood",
        "links": [
            "//membed.net/streaming.php?id=NDkyMTY=&title=Game+Of+Thrones+-+Season+1+Episode+10%3A+Fire+and+Blood&typesub=SUB&sub=L2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTEwLWZpcmUtYW5kLWJsb29kL2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTEwLWZpcmUtYW5kLWJsb29kLnZ0dA==&cover=",
            "//membed.net/embedplus?id=NDkyMTY=&token=vGPGi5gMkXL5Acnthxd8kw&expires=1669472728",
            "https://hydrax.net/watch?v=X8AW7PmgR",
            "https://mixdrop.co/e/rw4qvew3fwd66?sub1=https://sub.movie-series.net/game-of-thrones-season-1-episode-10-fire-and-blood/game-of-thrones-season-1-episode-10-fire-and-blood.vtt&sub1_label=English",
            "https://sbplay2.xyz/e/nc0kbntsjnw1?caption_1=https://sub.movie-series.net/game-of-thrones-season-1-episode-10-fire-and-blood/game-of-thrones-season-1-episode-10-fire-and-blood.vtt&sub_1=English",
            "https://dood.wf/e/b5aaog321o1h?c1_file=https://sub.movie-series.net/game-of-thrones-season-1-episode-10-fire-and-blood/game-of-thrones-season-1-episode-10-fire-and-blood.vtt&c1_label=English",
        ],
    },
    "9": {
        "title": "Game Of Thrones - Season 1 Episode 09: Baelor",
        "links": [
            "//membed.net/streaming.php?id=NDkyMTU=&title=Game+Of+Thrones+-+Season+1+Episode+09%3A+Baelor&typesub=SUB&sub=L2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTA5LWJhZWxvci9nYW1lLW9mLXRocm9uZXMtc2Vhc29uLTEtZXBpc29kZS0wOS1iYWVsb3IudnR0&cover=",
            "//membed.net/embedplus?id=NDkyMTU=&token=e-gCCYCrWRd3HX-lTD-anw&expires=1669472728",
            "https://hydrax.net/watch?v=CXKzko3HTd",
            "https://mixdrop.co/e/knrg76gpsvdnwn?sub1=https://sub.movie-series.net/game-of-thrones-season-1-episode-09-baelor/game-of-thrones-season-1-episode-09-baelor.vtt&sub1_label=English",
            "https://sbplay2.xyz/e/gr9cbkvbwjjy?caption_1=https://sub.movie-series.net/game-of-thrones-season-1-episode-09-baelor/game-of-thrones-season-1-episode-09-baelor.vtt&sub_1=English",
            "https://dood.wf/e/8bqai7hqppc2?c1_file=https://sub.movie-series.net/game-of-thrones-season-1-episode-09-baelor/game-of-thrones-season-1-episode-09-baelor.vtt&c1_label=English",
        ],
    },
    "8": {
        "title": "Game Of Thrones - Season 1 Episode 08: The Pointy End ",
        "links": [
            "//membed.net/streaming.php?id=NDkyMTQ=&title=Game+Of+Thrones+-+Season+1+Episode+08%3A+The+Pointy+End+&typesub=SUB&sub=L2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTA4LXRoZS1wb2ludHktZW5kL2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTA4LXRoZS1wb2ludHktZW5kLnZ0dA==&cover=",
            "//membed.net/embedplus?id=NDkyMTQ=&token=21obqVBynn0_eiURbOTY6A&expires=1669472728",
            "https://hydrax.net/watch?v=on_cIJk8Ln",
            "https://mixdrop.co/e/3nxrx47ehgz880?sub1=https://sub.movie-series.net/game-of-thrones-season-1-episode-08-the-pointy-end/game-of-thrones-season-1-episode-08-the-pointy-end.vtt&sub1_label=English",
            "https://sbplay2.xyz/e/bjcaj516uf3i?caption_1=https://sub.movie-series.net/game-of-thrones-season-1-episode-08-the-pointy-end/game-of-thrones-season-1-episode-08-the-pointy-end.vtt&sub_1=English",
            "https://dood.wf/e/h6mkut8fzocl?c1_file=https://sub.movie-series.net/game-of-thrones-season-1-episode-08-the-pointy-end/game-of-thrones-season-1-episode-08-the-pointy-end.vtt&c1_label=English",
        ],
    },
    "7": {
        "title": "Game Of Thrones - Season 1 Episode 07: You Win Or You Die",
        "links": [
            "//membed.net/streaming.php?id=NDkyMTM=&title=Game+Of+Thrones+-+Season+1+Episode+07%3A+You+Win+Or+You+Die&typesub=SUB&sub=L2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTA3LXlvdS13aW4tb3IteW91LWRpZS9nYW1lLW9mLXRocm9uZXMtc2Vhc29uLTEtZXBpc29kZS0wNy15b3Utd2luLW9yLXlvdS1kaWUudnR0&cover=&sub_es=true",
            "//membed.net/embedplus?id=NDkyMTM=&token=ZNR5ohS2mw-Y-TaPHiIfsg&expires=1669472728",
            "https://hydrax.net/watch?v=MpRAiSGmG",
            "https://mixdrop.co/e/gnxj4xm9hw4dxlx?sub1=https://sub.movie-series.net/game-of-thrones-season-1-episode-07-you-win-or-you-die/game-of-thrones-season-1-episode-07-you-win-or-you-die.vtt&sub1_label=English",
            "https://sbplay2.xyz/e/btuu0lyfzv4d?caption_1=https://sub.movie-series.net/game-of-thrones-season-1-episode-07-you-win-or-you-die/game-of-thrones-season-1-episode-07-you-win-or-you-die.vtt&sub_1=English",
            "https://dood.wf/e/g4mhg2kdstt9?c1_file=https://sub.movie-series.net/game-of-thrones-season-1-episode-07-you-win-or-you-die/game-of-thrones-season-1-episode-07-you-win-or-you-die.vtt&c1_label=English",
        ],
    },
    "6": {
        "title": "Game Of Thrones - Season 1 Episode 06: A Golden Crown",
        "links": [
            "//membed.net/streaming.php?id=NDkyMTI=&title=Game+Of+Thrones+-+Season+1+Episode+06%3A+A+Golden+Crown&typesub=SUB&sub=L2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTA2LWEtZ29sZGVuLWNyb3duL2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTA2LWEtZ29sZGVuLWNyb3duLnZ0dA==&cover=",
            "//membed.net/embedplus?id=NDkyMTI=&token=45Q26p_d8ckU5w2aNGAEBg&expires=1669472728",
            "https://hydrax.net/watch?v=68Ra6f2-0N",
            "https://mixdrop.co/e/knrgwk7vfdz1j1?sub1=https://sub.movie-series.net/game-of-thrones-season-1-episode-06-a-golden-crown/game-of-thrones-season-1-episode-06-a-golden-crown.vtt&sub1_label=English",
            "https://sbplay2.xyz/e/d237lpo9vpwa?caption_1=https://sub.movie-series.net/game-of-thrones-season-1-episode-06-a-golden-crown/game-of-thrones-season-1-episode-06-a-golden-crown.vtt&sub_1=English",
            "https://dood.wf/e/hv0882ib7m9o?c1_file=https://sub.movie-series.net/game-of-thrones-season-1-episode-06-a-golden-crown/game-of-thrones-season-1-episode-06-a-golden-crown.vtt&c1_label=English",
        ],
    },
    "5": {
        "title": "Game Of Thrones - Season 1 Episode 05: The Wolf and The Lion",
        "links": [
            "//membed.net/streaming.php?id=NDkyMTE=&title=Game+Of+Thrones+-+Season+1+Episode+05%3A+The+Wolf+and+The+Lion&typesub=SUB&sub=L2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTA1LXRoZS13b2xmLWFuZC10aGUtbGlvbi9nYW1lLW9mLXRocm9uZXMtc2Vhc29uLTEtZXBpc29kZS0wNS10aGUtd29sZi1hbmQtdGhlLWxpb24udnR0&cover=",
            "//membed.net/embedplus?id=NDkyMTE=&token=YG7joBSJAY5MwBGPTCF5iw&expires=1669472728",
            "https://hydrax.net/watch?v=hZg-j7qR_",
            "https://mixdrop.co/e/0vwowmmjskk7l8z?sub1=https://sub.movie-series.net/game-of-thrones-season-1-episode-05-the-wolf-and-the-lion/game-of-thrones-season-1-episode-05-the-wolf-and-the-lion.vtt&sub1_label=English",
            "https://sbplay2.xyz/e/t4w6wl1ivzwy?caption_1=https://sub.movie-series.net/game-of-thrones-season-1-episode-05-the-wolf-and-the-lion/game-of-thrones-season-1-episode-05-the-wolf-and-the-lion.vtt&sub_1=English",
            "https://dood.wf/e/397qatu8vufh?c1_file=https://sub.movie-series.net/game-of-thrones-season-1-episode-05-the-wolf-and-the-lion/game-of-thrones-season-1-episode-05-the-wolf-and-the-lion.vtt&c1_label=English",
        ],
    },
    "4": {
        "title": "Game Of Thrones - Season 1 Episode 04: Cripples, Bastards and Broken Things",
        "links": [
            "//membed.net/streaming.php?id=NDkyMTA=&title=Game+Of+Thrones+-+Season+1+Episode+04%3A+Cripples%2C+Bastards+and+Broken+Things&typesub=SUB&sub=L2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTA0LWNyaXBwbGVzLWJhc3RhcmRzLWFuZC1icm9rZW4tdGhpbmdzL2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTA0LWNyaXBwbGVzLWJhc3RhcmRzLWFuZC1icm9rZW4tdGhpbmdzLnZ0dA==&cover=",
            "//membed.net/embedplus?id=NDkyMTA=&token=fL5ydhEBoBx-ObVe-zKW_w&expires=1669472728",
            "https://hydrax.net/watch?v=RLOR9Tqpi",
            "https://mixdrop.co/e/3nx179lrbmm9zqz?sub1=https://sub.movie-series.net/game-of-thrones-season-1-episode-04-cripples-bastards-and-broken-things/game-of-thrones-season-1-episode-04-cripples-bastards-and-broken-things.vtt&sub1_label=English",
            "https://sbplay2.xyz/e/0dtm7ux2fnia?caption_1=https://sub.movie-series.net/game-of-thrones-season-1-episode-04-cripples-bastards-and-broken-things/game-of-thrones-season-1-episode-04-cripples-bastards-and-broken-things.vtt&sub_1=English",
            "https://dood.wf/e/vqm5jnxzpsdr?c1_file=https://sub.movie-series.net/game-of-thrones-season-1-episode-04-cripples-bastards-and-broken-things/game-of-thrones-season-1-episode-04-cripples-bastards-and-broken-things.vtt&c1_label=English",
        ],
    },
    "3": {
        "title": "Game Of Thrones - Season 1 Episode 03: Lord Snow",
        "links": [
            "//membed.net/streaming.php?id=NDkyMDk=&title=Game+Of+Thrones+-+Season+1+Episode+03%3A+Lord+Snow&typesub=SUB&sub=L2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTAzLWxvcmQtc25vdy9nYW1lLW9mLXRocm9uZXMtc2Vhc29uLTEtZXBpc29kZS0wMy1sb3JkLXNub3cudnR0&cover=&sub_es=true",
            "//membed.net/embedplus?id=NDkyMDk=&token=Vl2dcoJ8P9HcgJZdu8sOxA&expires=1669472728",
            "https://hydrax.net/watch?v=jrBkm0yKpM",
            "https://mixdrop.co/e/wnr87njwu3v9mo?sub1=https://sub.movie-series.net/game-of-thrones-season-1-episode-03-lord-snow/game-of-thrones-season-1-episode-03-lord-snow.vtt&sub1_label=English",
            "https://sbplay2.xyz/e/nvgqhibjry1y?caption_1=https://sub.movie-series.net/game-of-thrones-season-1-episode-03-lord-snow/game-of-thrones-season-1-episode-03-lord-snow.vtt&sub_1=English",
            "https://dood.wf/e/71w2jfimkql7?c1_file=https://sub.movie-series.net/game-of-thrones-season-1-episode-03-lord-snow/game-of-thrones-season-1-episode-03-lord-snow.vtt&c1_label=English",
        ],
    },
    "2": {
        "title": "Game Of Thrones - Season 1 Episode 02: The Kingsroad",
        "links": [
            "//membed.net/streaming.php?id=NDkyMDg=&title=Game+Of+Thrones+-+Season+1+Episode+02%3A+The+Kingsroad&typesub=SUB&sub=L2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTAyLXRoZS1raW5nc3JvYWQvZ2FtZS1vZi10aHJvbmVzLXNlYXNvbi0xLWVwaXNvZGUtMDItdGhlLWtpbmdzcm9hZC52dHQ=&cover=",
            "//membed.net/embedplus?id=NDkyMDg=&token=Y8tgFiDxe22_B9xX1u1vxQ&expires=1669472728",
            "https://mixdrop.co/e/3nx17k7mf06d7r?sub1=https://sub.movie-series.net/game-of-thrones-season-1-episode-02-the-kingsroad/game-of-thrones-season-1-episode-02-the-kingsroad.vtt&sub1_label=English",
            "https://sbplay2.xyz/e/5s3nw2pj814x?caption_1=https://sub.movie-series.net/game-of-thrones-season-1-episode-02-the-kingsroad/game-of-thrones-season-1-episode-02-the-kingsroad.vtt&sub_1=English",
            "https://dood.wf/e/slttga2j1bgr?c1_file=https://sub.movie-series.net/game-of-thrones-season-1-episode-02-the-kingsroad/game-of-thrones-season-1-episode-02-the-kingsroad.vtt&c1_label=English",
        ],
    },
    "1": {
        "title": "Game Of Thrones - Season 1 Episode 01: Winter is Coming",
        "links": [
            "//membed.net/streaming.php?id=NDkyMDc=&title=Game+Of+Thrones+-+Season+1+Episode+01%3A+Winter+is+Coming&typesub=SUB&sub=L2dhbWUtb2YtdGhyb25lcy1zZWFzb24tMS1lcGlzb2RlLTAxLXdpbnRlci1pcy1jb21pbmcvZ2FtZS1vZi10aHJvbmVzLXNlYXNvbi0xLWVwaXNvZGUtMDEtd2ludGVyLWlzLWNvbWluZy52dHQ=&cover=",
            "//membed.net/embedplus?id=NDkyMDc=&token=_Yo4FTvmZ5Pigp0fpQY46w&expires=1669472728",
            "https://hydrax.net/watch?v=6nVOtUmM5L",
            "https://mixdrop.co/e/7r6gvr38il3ew6?sub1=https://sub.movie-series.net/game-of-thrones-season-1-episode-01-winter-is-coming/game-of-thrones-season-1-episode-01-winter-is-coming.vtt&sub1_label=English",
            "https://sbplay2.xyz/e/p9z25ko5pjrk?caption_1=https://sub.movie-series.net/game-of-thrones-season-1-episode-01-winter-is-coming/game-of-thrones-season-1-episode-01-winter-is-coming.vtt&sub_1=English",
            "https://dood.wf/e/e13cx7n9klfo?c1_file=https://sub.movie-series.net/game-of-thrones-season-1-episode-01-winter-is-coming/game-of-thrones-season-1-episode-01-winter-is-coming.vtt&c1_label=English",
        ],
    },
}

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


def main():
    Toroplay(film_data, episodes_data).insert_film()


if __name__ == "__main__":
    main()

"""Fetch technical scores for a recent Grand Prix series from skatingscores."""


from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import time

BASE_URL = "https://skatingscores.com"
EVENTS = [
    "1920/gpcan",
    "1920/gpchn",
    "1920/gpjpn",
    "1920/gpfra",
    "1920/gpusa",
    "1920/gpf",
    "1920/4cc",
    "2021/natjpn",
    "2021/natusa"
]
GENDERS = ["men", "ladies"]
PROGRAMS = ["short", "long"]
OUTPUT_FILE = "scores.csv"


def main():
    urls = get_urls(BASE_URL, EVENTS, GENDERS, PROGRAMS)
    print("Fetching data...")
    soups = fetch_soups(urls)
    print("Processing data...")
    scores = get_df_from_soups(soups)
    print(f"Writing data to {OUTPUT_FILE}")
    scores.to_csv(OUTPUT_FILE)


def get_urls(base_url, events, genders, programs):
   return [
        f"{base_url}/{event}/{gender}/{program}"
        for event in events
        for gender in genders
        for program in programs
    ]
 

def fetch_html(url):
   time.sleep(0.2)  # to avoid overloading the skatingscores server
   try:
      r = requests.get(url)
      r.raise_for_status()   
      return r.content
   except requests.exceptions.HTTPError as err:
      raise SystemExit(err)


def fetch_soups(urls):
    return [BeautifulSoup(fetch_html(url), 'html.parser') for url in urls]


def get_skates(soup):
    return soup.find_all("div", {"class": "skat-wrap"})


def get_event_name(soup):
    return re.sub(r'[^A-Za-z0-9 ]+', '',  soup.find("h1").text).lstrip()


def parse_table_row(row, make_numeric=True):
    return [td.text for td in row.find_all("td")]


def get_df_from_soups(soups):
    return pd.concat(
       [get_df_from_soup(soup) for soup in soups], ignore_index=True
    )


def get_df_from_soup(soup):
    event = get_event_name(soup)
    skates = get_skates(soup)
    out = pd.DataFrame()
    for skate in skates:
       name, country = get_name_and_country(skate)
       score_table = get_score_table(skate)
       score_df = get_df_from_skate(event, name, country, score_table)
       out = pd.concat([out, score_df], ignore_index=True)
    return out


def get_df_from_skate(event, name, country, score_table):
    n_judge = len(score_table[0]) - 7
    judge_cols = [str(i+1) for i in range(n_judge)]
    pre_cols = ["order", "element", "notes", "base_value", "late", "goe_total"]
    post_cols = ["aggregate_score"]
    cols = pre_cols + judge_cols + post_cols
    return (
        pd.DataFrame(score_table, columns=cols)
        .assign(late=lambda df: df["late"].map({"x": True, "": False}))
        .melt(id_vars=pre_cols+post_col, var_name="judge", value_name="score")
        .assign(event=event_name, name=name, country=country)
        .apply(pd.to_numeric, errors="ignore", downcast="integer")
    )


def get_score_table(skate_soup):
    exclude = {"head", "tally"}
    rows = list(filter(
        lambda r: len(set(r.attrs["class"]) & exclude) == 0,
        skate_soup
        .find("div", class_="ptab2-wrap")
        .find("table")
        .find_all("tr")
    ))
    return [[td.text for td in r.find_all("td")] for r in rows]


def get_name_and_country(skate_soup):
    headlinks = (
        skate_soup
        .find("div", class_="ptab1-wrap")
        .find("table")
        .find("tr", class_="head")
        .find_all("a")
    )
    name = " ".join([n.capitalize() for n in headlinks[0].text.split(" ")])
    country = headlinks[1].text
    return name, country


if __name__ == "__main__":
    main()

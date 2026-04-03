import http.client
import json
import time
import pandas as pd
from datetime import datetime, timedelta

conn = http.client.HTTPConnection("scores24.live")

over_target = 74
slug = "01-12-2024-roman-wiza-robert-szymik"

loop_h2h_payload = "{\"operationName\":\"MatchH2HGamesMatches\",\"query\":\"query MatchH2HGamesMatches($matchSlug: String!, $sportSlug: String!, $langSlug: LangEnum!, $leagueSlug: String, $limit: Int, $skip: Int, $meetingType: MeetingTypeEnum!, $teamType: TeamTypeEnum, $excludeLive: Boolean!, $withFriendly: Boolean, $isHorseRacing: Boolean!, $withMarkets: Boolean!, $withStatistics: Boolean!) {\\n  TeamMatches(\\n    exclude_live: $excludeLive\\n    lang: $langSlug\\n    sport_slug: $sportSlug\\n    match_slug: $matchSlug\\n    league_slug: $leagueSlug\\n    team_type: $teamType\\n    limit: $limit\\n    skip: $skip\\n    meeting_type: $meetingType\\n    match_status: past\\n    with_friendly: $withFriendly\\n  ) {\\n    ...NewCalendarMatch\\n    ...MatchStatistic @include(if: $withStatistics)\\n    __typename\\n  }\\n}\\nfragment NewCalendarMatch on Match {\\n  ...MatchCacheFragment\\n  ...HorseMatch @include(if: $isHorseRacing)\\n  ...MarketsFragment @include(if: $withMarkets)\\n  gameState: game_state {\\n    home: home_score\\n    away: away_score\\n    __typename\\n  }\\n  type\\n  broadcasts {\\n    livestream\\n    __typename\\n  }\\n  addMinute: add_minute\\n  serving\\n  sportSlug: sport_slug\\n  gameScore: game_score\\n  resultScore: result_score\\n  hasOdds: has_odds\\n  hasH2h: has_h2h\\n  hasSquads: has_squads\\n  hasStandings: has_standings\\n  hasPrediction: has_prediction\\n  resultScores: result_scores {\\n    awayTiebreakScore: away_tiebreak_score\\n    homeTiebreakScore: home_tiebreak_score\\n    type\\n    value\\n     __typename\\n  }\\n  server\\n  leagueSlug: league_slug\\n  cards {\\n    color\\n    team\\n    __typename\\n  }\\n  country {\\n    iso\\n    slug\\n    __typename\\n  }\\n  tournamentName: tournament_name\\n  uniqueTournament: unique_tournament {\\n    ...LeagueCacheFragment\\n    slug\\n    shortName: short_name\\n    __typename\\n  }\\n  uniqueTournamentName: unique_tournament_name\\n  teams {\\n    ...TeamCacheFragment\\n    id\\n    name\\n    logo\\n    country {\\n      iso\\n      __typename\\n    }\\n    __typename\\n  }\\n  status {\\n    code\\n    __typename\\n  }\\n  isLive: is_live\\n  isFinished: is_finished\\n  minute\\n  tiebreak\\n  winner\\n  __typename\\n}\\nfragment HorseMatch on Match {\\n  surface\\n  name\\n  distance\\n  purse\\n  uniqueTournament: unique_tournament {\\n    going\\n    __typename\\n  }\\n  teams {\\n    name\\n    slug\\n    jockeyName: jockey_name\\n    jockeySlug: jockey_slug\\n    trainerName: trainer_name\\n    trainerSlug: trainer_slug\\n    odd\\n    sp\\n    wgt\\n    wgtLbs: wgt_lbs\\n    age\\n    rating\\n    position\\n    distance\\n    gender\\n    __typename\\n  }\\n  __typename\\n}\\nfragment MarketsFragment on Match {\\n  markets {\\n    bookmaker {\\n      ...BookmakerCacheFragment\\n      slug\\n      name\\n      logo\\n      favicon\\n      legal\\n      color\\n      url\\n      __typename\\n    }\\n    name\\n    value\\n    __typename\\n  }\\n  bkmUrls: bkm_urls {\\n    bookmaker\\n    url\\n    __typename\\n  }\\n  __typename\\n}\\nfragment BookmakerCacheFragment on Bookmaker {\\n  slug\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment MatchCacheFragment on Match {\\n  slug\\n  matchDate: match_date\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment LeagueCacheFragment on League {\\n  slug\\n  langSlug: lang_slug\\n  sportSlug: sport_slug\\n  __typename\\n}\\nfragment TeamCacheFragment on Team {\\n  slug\\n  langSlug: lang_slug\\n  name\\n  temporarilyQualified: temporarily_qualified\\n  __typename\\n}\\nfragment MatchStatistic on Match {\\n  statistic {\\n    filteredPeriods: filtered_periods(\\n      period_types: [\\n\\\"total\\\"]\\n      stat_types: [\\n\\\"corner_kicks\\\", \\n\\\"cards_given\\\", \\n\\\"fouls\\\", \\n\\\"yellow_cards\\\", \\n\\\"xg\\\"]\\n    ) {\\n      type\\n      items {\\n        type\\n        team1Value: team1_value\\n        team2Value: team2_value\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\",\"variables\":{\"excludeLive\":true,\"isHorseRacing\":false,\"langSlug\":\"en\",\"limit\":30,\"matchSlug\":\"" + slug + "\",\"meetingType\":\"join\",\"skip\":0,\"sportSlug\":\"table-tennis\",\"withFriendly\":false,\"withMarkets\":false,\"withStatistics\":false}}"


headers = {
    'cookie': "testValue=2; userOddFormat=EU; machineTimezone=GMT-5; promo-proxy-_subid=3vlo9fmvk359e; promo-proxy-2a34b=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1wic3RyZWFtc1wiOntcIjgxOTNcIjoxNzMyNjI0NDg0fSxcImNhbXBhaWduc1wiOntcIjUwXCI6MTczMjYyNDQ4NH0sXCJ0aW1lXCI6MTczMjYyNDQ4NH0ifQ.1iqw6laGaWsmusXuGPdJLYDrmvvjbn8hZEMl2trf1Iw; promo-proxy-_token=uuid_3vlo9fmvk359e_3vlo9fmvk359e6745c064368c79.69394983; s24-session=XD5dH5TTzkWMjiwyebaBRUfs0uQAsDlR6mpHoozG; latestWidth=1079",
    'accept': "application/graphql-response+json, application/graphql+json, application/json, text/event-stream, multipart/mixed",
    'accept-language': "en-US,en;q=0.9",
    'content-type': "application/json",
    'origin': "https://scores24.live",
    'priority': "u=1, i",
    'referer': "https://scores24.live/en/table-tennis/l-tt-elite-series-1",
    'sec-ch-ua-mobile': "?0",
    'sec-fetch-dest': "empty",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "same-origin",
    'sec-gpc': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    'x-bot-identifier': "client",
    'x-country': "us-nc",
    'x-ssr-ip': "98.24.160.108",
    'x-user-cache': "W2ZO6w9f6OdiBrEL9DMH",
    'x-user-ip': "98.24.160.108"
    }
    
conn.request("POST", "/graphql", loop_h2h_payload, headers)

res = conn.getresponse()
data = res.read()

json_resp = json.loads(data.decode("utf-8"))

match_play = []


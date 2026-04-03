import http.client
import json
import time
import pandas as pd # type: ignore
from datetime import datetime, timedelta
import statistics
import math
from chump import Application
import sys


def run_data_script():
    conn = http.client.HTTPSConnection("scores24.live")
    app = Application("hidden")
    user = app.get_user("hidden")

    dateNow = "2025-01-01 02:00:00"

    print("Running Table Tennis Plays Job")

    over_target = 74
    upcoming_limit = "300"
    best_plays_over = 8
    best_plays_under = 2

    upcoming_payload = "{\"operationName\":\"LeagueH2HMatches\",\"query\":\"query LeagueH2HMatches($datebetween: [String]!, $orderby: [String!]!, $sportSlug: String!, $langSlug: String!, $limit: Int!, $skip: Int!, $leagueSlug: String, $meetingType: String, $withLive: Boolean, $isHorseRacing: Boolean!, $withMarkets: Boolean!, $withStatistics: Boolean!, $excludeCanceled: Boolean, $matchStatus: String) {   MatchList(     datebetween: $datebetween     orderby: $orderby     sport_slug: $sportSlug     lang: $langSlug     limit: $limit     skip: $skip     league_slug: $leagueSlug     meeting_type: $meetingType     live: $withLive     exclude_canceled: $excludeCanceled     match_status: $matchStatus   ) {     ...NewCalendarMatch     ...MatchStatistic @include(if: $withStatistics)     __typename   } } fragment NewCalendarMatch on Match {   ...MatchCacheFragment   ...HorseMatch @include(if: $isHorseRacing)   ...MarketsFragment @include(if: $withMarkets)   gameState: game_state {     home: home_score     away: away_score     __typename   }   type   broadcasts {     livestream     __typename   }   addMinute: add_minute   serving   sportSlug: sport_slug   gameScore: game_score   resultScore: result_score   hasOdds: has_odds   hasH2h: has_h2h   hasSquads: has_squads   hasStandings: has_standings   hasPrediction: has_prediction   resultScores: result_scores {     awayTiebreakScore: away_tiebreak_score     homeTiebreakScore: home_tiebreak_score     type     value     __typename   }   server   leagueSlug: league_slug   cards {     color     team     __typename   }   country {     iso     slug     __typename   }   tournamentName: tournament_name   uniqueTournament: unique_tournament {     ...LeagueCacheFragment     slug     shortName: short_name     __typename   }   uniqueTournamentName: unique_tournament_name   teams {     ...TeamCacheFragment     id     name     logo     country {       iso       __typename     }     __typename   }   status {     code     __typename   }   isLive: is_live   isFinished: is_finished   minute   tiebreak   winner   __typename } fragment HorseMatch on Match {   surface   name   distance   purse   uniqueTournament: unique_tournament {     going     __typename   }   teams {     name     slug     jockeyName: jockey_name     jockeySlug: jockey_slug     trainerName: trainer_name     trainerSlug: trainer_slug     odd     sp     wgt     wgtLbs: wgt_lbs     age     rating     position     distance     gender     __typename   }   __typename } fragment MarketsFragment on Match {   markets {     bookmaker {       ...BookmakerCacheFragment       slug       name       logo       favicon       legal       color       url       __typename     }     name     value     __typename   }   bkmUrls: bkm_urls {     bookmaker     url     __typename   }   __typename } fragment BookmakerCacheFragment on Bookmaker {   slug   langSlug: lang_slug   __typename } fragment MatchCacheFragment on Match {   slug   matchDate: match_date   langSlug: lang_slug   __typename } fragment LeagueCacheFragment on League {   slug   langSlug: lang_slug   sportSlug: sport_slug   __typename } fragment TeamCacheFragment on Team {   slug   langSlug: lang_slug   name   temporarilyQualified: temporarily_qualified   __typename } fragment MatchStatistic on Match {   statistic {     filteredPeriods: filtered_periods(       period_types: [ \\\"total\\\"]       stat_types: [ \\\"corner_kicks\\\",  \\\"cards_given\\\",  \\\"fouls\\\",  \\\"yellow_cards\\\",  \\\"xg\\\"]     ) {       type       items {         type         team1Value: team1_value         team2Value: team2_value         __typename       }       __typename     }     __typename   }   __typename }\",\"variables\":{\"datebetween\":[\"2024-11-28 02:00:00\",\"\"],\"excludeCanceled\":true,\"isHorseRacing\":false,\"langSlug\":\"en\",\"leagueSlug\":\"tt-elite-series-1\",\"limit\":" + upcoming_limit + ",\"matchStatus\":\"not_started\",\"meetingType\":\"join\",\"orderby\":[\"match_date\",\"asc\"],\"skip\":0,\"sportSlug\":\"table-tennis\",\"withLive\":false,\"withMarkets\":false,\"withStatistics\":false}}"

    h2h_payload = "{\"operationName\":\"MatchH2HGamesMatches\",\"query\":\"query MatchH2HGamesMatches($matchSlug: String!, $sportSlug: String!, $langSlug: LangEnum!, $leagueSlug: String, $limit: Int, $skip: Int, $meetingType: MeetingTypeEnum!, $teamType: TeamTypeEnum, $excludeLive: Boolean!, $withFriendly: Boolean, $isHorseRacing: Boolean!, $withMarkets: Boolean!, $withStatistics: Boolean!) {\\n  TeamMatches(\\n    exclude_live: $excludeLive\\n    lang: $langSlug\\n    sport_slug: $sportSlug\\n    match_slug: $matchSlug\\n    league_slug: $leagueSlug\\n    team_type: $teamType\\n    limit: $limit\\n    skip: $skip\\n    meeting_type: $meetingType\\n    match_status: past\\n    with_friendly: $withFriendly\\n  ) {\\n    ...NewCalendarMatch\\n    ...MatchStatistic @include(if: $withStatistics)\\n    __typename\\n  }\\n}\\nfragment NewCalendarMatch on Match {\\n  ...MatchCacheFragment\\n  ...HorseMatch @include(if: $isHorseRacing)\\n  ...MarketsFragment @include(if: $withMarkets)\\n  gameState: game_state {\\n    home: home_score\\n    away: away_score\\n    __typename\\n  }\\n  type\\n  broadcasts {\\n    livestream\\n    __typename\\n  }\\n  addMinute: add_minute\\n  serving\\n  sportSlug: sport_slug\\n  gameScore: game_score\\n  resultScore: result_score\\n  hasOdds: has_odds\\n  hasH2h: has_h2h\\n  hasSquads: has_squads\\n  hasStandings: has_standings\\n  hasPrediction: has_prediction\\n  resultScores: result_scores {\\n    awayTiebreakScore: away_tiebreak_score\\n    homeTiebreakScore: home_tiebreak_score\\n    type\\n    value\\n     __typename\\n  }\\n  server\\n  leagueSlug: league_slug\\n  cards {\\n    color\\n    team\\n    __typename\\n  }\\n  country {\\n    iso\\n    slug\\n    __typename\\n  }\\n  tournamentName: tournament_name\\n  uniqueTournament: unique_tournament {\\n    ...LeagueCacheFragment\\n    slug\\n    shortName: short_name\\n    __typename\\n  }\\n  uniqueTournamentName: unique_tournament_name\\n  teams {\\n    ...TeamCacheFragment\\n    id\\n    name\\n    logo\\n    country {\\n      iso\\n      __typename\\n    }\\n    __typename\\n  }\\n  status {\\n    code\\n    __typename\\n  }\\n  isLive: is_live\\n  isFinished: is_finished\\n  minute\\n  tiebreak\\n  winner\\n  __typename\\n}\\nfragment HorseMatch on Match {\\n  surface\\n  name\\n  distance\\n  purse\\n  uniqueTournament: unique_tournament {\\n    going\\n    __typename\\n  }\\n  teams {\\n    name\\n    slug\\n    jockeyName: jockey_name\\n    jockeySlug: jockey_slug\\n    trainerName: trainer_name\\n    trainerSlug: trainer_slug\\n    odd\\n    sp\\n    wgt\\n    wgtLbs: wgt_lbs\\n    age\\n    rating\\n    position\\n    distance\\n    gender\\n    __typename\\n  }\\n  __typename\\n}\\nfragment MarketsFragment on Match {\\n  markets {\\n    bookmaker {\\n      ...BookmakerCacheFragment\\n      slug\\n      name\\n      logo\\n      favicon\\n      legal\\n      color\\n      url\\n      __typename\\n    }\\n    name\\n    value\\n    __typename\\n  }\\n  bkmUrls: bkm_urls {\\n    bookmaker\\n    url\\n    __typename\\n  }\\n  __typename\\n}\\nfragment BookmakerCacheFragment on Bookmaker {\\n  slug\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment MatchCacheFragment on Match {\\n  slug\\n  matchDate: match_date\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment LeagueCacheFragment on League {\\n  slug\\n  langSlug: lang_slug\\n  sportSlug: sport_slug\\n  __typename\\n}\\nfragment TeamCacheFragment on Team {\\n  slug\\n  langSlug: lang_slug\\n  name\\n  temporarilyQualified: temporarily_qualified\\n  __typename\\n}\\nfragment MatchStatistic on Match {\\n  statistic {\\n    filteredPeriods: filtered_periods(\\n      period_types: [\\n\\\"total\\\"]\\n      stat_types: [\\n\\\"corner_kicks\\\", \\n\\\"cards_given\\\", \\n\\\"fouls\\\", \\n\\\"yellow_cards\\\", \\n\\\"xg\\\"]\\n    ) {\\n      type\\n      items {\\n        type\\n        team1Value: team1_value\\n        team2Value: team2_value\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\",\"variables\":{\"excludeLive\":true,\"isHorseRacing\":false,\"langSlug\":\"en\",\"limit\":50,\"matchSlug\":\"29-11-2024-bart-omiej-wi-niewski-blazej-szczepanek\",\"meetingType\":\"join\",\"skip\":0,\"sportSlug\":\"table-tennis\",\"withFriendly\":false,\"withMarkets\":false,\"withStatistics\":true}}"


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

    conn.request("POST", "/graphql", upcoming_payload, headers)


    res = conn.getresponse()
    data = res.read()

    json_resp = json.loads(data.decode("utf-8"))

    all_plays_array = []
    best_plays_array = []
    four_round_plays_array = []
    first_set_plays_array = []
    spread_plays_array = []
    message_notification =  ""
    first_set_notification = ""

    for index, game in enumerate(json_resp["data"]["MatchList"]):
        # print(f"{index}" + ": " + game["slug"] + " : " + game["matchDate"])
        game_object = {}
        loop_h2h_payload = "{\"operationName\":\"MatchH2HGamesMatches\",\"query\":\"query MatchH2HGamesMatches($matchSlug: String!, $sportSlug: String!, $langSlug: LangEnum!, $leagueSlug: String, $limit: Int, $skip: Int, $meetingType: MeetingTypeEnum!, $teamType: TeamTypeEnum, $excludeLive: Boolean!, $withFriendly: Boolean, $isHorseRacing: Boolean!, $withMarkets: Boolean!, $withStatistics: Boolean!) {\\n  TeamMatches(\\n    exclude_live: $excludeLive\\n    lang: $langSlug\\n    sport_slug: $sportSlug\\n    match_slug: $matchSlug\\n    league_slug: $leagueSlug\\n    team_type: $teamType\\n    limit: $limit\\n    skip: $skip\\n    meeting_type: $meetingType\\n    match_status: past\\n    with_friendly: $withFriendly\\n  ) {\\n    ...NewCalendarMatch\\n    ...MatchStatistic @include(if: $withStatistics)\\n    __typename\\n  }\\n}\\nfragment NewCalendarMatch on Match {\\n  ...MatchCacheFragment\\n  ...HorseMatch @include(if: $isHorseRacing)\\n  ...MarketsFragment @include(if: $withMarkets)\\n  gameState: game_state {\\n    home: home_score\\n    away: away_score\\n    __typename\\n  }\\n  type\\n  broadcasts {\\n    livestream\\n    __typename\\n  }\\n  addMinute: add_minute\\n  serving\\n  sportSlug: sport_slug\\n  gameScore: game_score\\n  resultScore: result_score\\n  hasOdds: has_odds\\n  hasH2h: has_h2h\\n  hasSquads: has_squads\\n  hasStandings: has_standings\\n  hasPrediction: has_prediction\\n  resultScores: result_scores {\\n    awayTiebreakScore: away_tiebreak_score\\n    homeTiebreakScore: home_tiebreak_score\\n    type\\n    value\\n     __typename\\n  }\\n  server\\n  leagueSlug: league_slug\\n  cards {\\n    color\\n    team\\n    __typename\\n  }\\n  country {\\n    iso\\n    slug\\n    __typename\\n  }\\n  tournamentName: tournament_name\\n  uniqueTournament: unique_tournament {\\n    ...LeagueCacheFragment\\n    slug\\n    shortName: short_name\\n    __typename\\n  }\\n  uniqueTournamentName: unique_tournament_name\\n  teams {\\n    ...TeamCacheFragment\\n    id\\n    name\\n    logo\\n    country {\\n      iso\\n      __typename\\n    }\\n    __typename\\n  }\\n  status {\\n    code\\n    __typename\\n  }\\n  isLive: is_live\\n  isFinished: is_finished\\n  minute\\n  tiebreak\\n  winner\\n  __typename\\n}\\nfragment HorseMatch on Match {\\n  surface\\n  name\\n  distance\\n  purse\\n  uniqueTournament: unique_tournament {\\n    going\\n    __typename\\n  }\\n  teams {\\n    name\\n    slug\\n    jockeyName: jockey_name\\n    jockeySlug: jockey_slug\\n    trainerName: trainer_name\\n    trainerSlug: trainer_slug\\n    odd\\n    sp\\n    wgt\\n    wgtLbs: wgt_lbs\\n    age\\n    rating\\n    position\\n    distance\\n    gender\\n    __typename\\n  }\\n  __typename\\n}\\nfragment MarketsFragment on Match {\\n  markets {\\n    bookmaker {\\n      ...BookmakerCacheFragment\\n      slug\\n      name\\n      logo\\n      favicon\\n      legal\\n      color\\n      url\\n      __typename\\n    }\\n    name\\n    value\\n    __typename\\n  }\\n  bkmUrls: bkm_urls {\\n    bookmaker\\n    url\\n    __typename\\n  }\\n  __typename\\n}\\nfragment BookmakerCacheFragment on Bookmaker {\\n  slug\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment MatchCacheFragment on Match {\\n  slug\\n  matchDate: match_date\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment LeagueCacheFragment on League {\\n  slug\\n  langSlug: lang_slug\\n  sportSlug: sport_slug\\n  __typename\\n}\\nfragment TeamCacheFragment on Team {\\n  slug\\n  langSlug: lang_slug\\n  name\\n  temporarilyQualified: temporarily_qualified\\n  __typename\\n}\\nfragment MatchStatistic on Match {\\n  statistic {\\n    filteredPeriods: filtered_periods(\\n      period_types: [\\n\\\"total\\\"]\\n      stat_types: [\\n\\\"corner_kicks\\\", \\n\\\"cards_given\\\", \\n\\\"fouls\\\", \\n\\\"yellow_cards\\\", \\n\\\"xg\\\"]\\n    ) {\\n      type\\n      items {\\n        type\\n        team1Value: team1_value\\n        team2Value: team2_value\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\",\"variables\":{\"excludeLive\":true,\"isHorseRacing\":false,\"langSlug\":\"en\",\"limit\":30,\"matchSlug\":\"" + game["slug"] + "\",\"meetingType\":\"join\",\"skip\":0,\"sportSlug\":\"table-tennis\",\"withFriendly\":false,\"withMarkets\":false,\"withStatistics\":false}}"
        home_payload = "{\"operationName\":\"MatchH2HGamesMatches\",\"query\":\"query MatchH2HGamesMatches($matchSlug: String!, $sportSlug: String!, $langSlug: LangEnum!, $leagueSlug: String, $limit: Int, $skip: Int, $meetingType: MeetingTypeEnum!, $teamType: TeamTypeEnum, $excludeLive: Boolean!, $withFriendly: Boolean, $isHorseRacing: Boolean!, $withMarkets: Boolean!, $withStatistics: Boolean!) {\\n  TeamMatches(\\n    exclude_live: $excludeLive\\n    lang: $langSlug\\n    sport_slug: $sportSlug\\n    match_slug: $matchSlug\\n    league_slug: $leagueSlug\\n    team_type: $teamType\\n    limit: $limit\\n    skip: $skip\\n    meeting_type: $meetingType\\n    match_status: past\\n    with_friendly: $withFriendly\\n  ) {\\n    ...NewCalendarMatch\\n    ...MatchStatistic @include(if: $withStatistics)\\n    __typename\\n  }\\n}\\nfragment NewCalendarMatch on Match {\\n  ...MatchCacheFragment\\n  ...HorseMatch @include(if: $isHorseRacing)\\n  ...MarketsFragment @include(if: $withMarkets)\\n  gameState: game_state {\\n    home: home_score\\n    away: away_score\\n    __typename\\n  }\\n  type\\n  broadcasts {\\n    livestream\\n    __typename\\n  }\\n  addMinute: add_minute\\n  serving\\n  sportSlug: sport_slug\\n  gameScore: game_score\\n  resultScore: result_score\\n  hasOdds: has_odds\\n  hasH2h: has_h2h\\n  hasSquads: has_squads\\n  hasStandings: has_standings\\n  hasPrediction: has_prediction\\n  resultScores: result_scores {\\n    awayTiebreakScore: away_tiebreak_score\\n    homeTiebreakScore: home_tiebreak_score\\n    type\\n    value\\n    __typename\\n  }\\n  server\\n  leagueSlug: league_slug\\n  cards {\\n    color\\n    team\\n    __typename\\n  }\\n  country {\\n    ...CountryFragment\\n    __typename\\n  }\\n  tournamentName: tournament_name\\n  uniqueTournament: unique_tournament {\\n    ...LeagueCacheFragment\\n    slug\\n    shortName: short_name\\n    __typename\\n  }\\n  uniqueTournamentName: unique_tournament_name\\n  teams {\\n    ...TeamCacheFragment\\n    id\\n    name\\n    logo\\n    country {\\n      iso\\n      __typename\\n    }\\n    __typename\\n  }\\n  status {\\n    code\\n    __typename\\n  }\\n  isLive: is_live\\n  isFinished: is_finished\\n  minute\\n  tiebreak\\n  winner\\n  __typename\\n}\\nfragment HorseMatch on Match {\\n  surface\\n  name\\n  distance\\n  purse\\n  uniqueTournament: unique_tournament {\\n    going\\n    __typename\\n  }\\n  teams {\\n    name\\n    slug\\n    jockeyName: jockey_name\\n    jockeySlug: jockey_slug\\n    trainerName: trainer_name\\n    trainerSlug: trainer_slug\\n    odd\\n    sp\\n    wgt\\n    wgtLbs: wgt_lbs\\n    age\\n    rating\\n    position\\n    distance\\n    gender\\n    __typename\\n  }\\n  __typename\\n}\\nfragment MarketsFragment on Match {\\n  markets {\\n    bookmaker {\\n      ...BookmakerCacheFragment\\n      slug\\n      name\\n      logo\\n      favicon\\n      legal\\n      color\\n      url\\n      __typename\\n    }\\n    name\\n    value\\n    __typename\\n  }\\n  bkmUrls: bkm_urls {\\n    bookmaker\\n    url\\n    __typename\\n  }\\n  __typename\\n}\\nfragment BookmakerCacheFragment on Bookmaker {\\n  slug\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment MatchCacheFragment on Match {\\n  slug\\n  matchDate: match_date\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment CountryFragment on Country {\\n  name\\n  slug\\n  iso\\n  __typename\\n}\\nfragment LeagueCacheFragment on League {\\n  slug\\n  langSlug: lang_slug\\n  sportSlug: sport_slug\\n  __typename\\n}\\nfragment TeamCacheFragment on Team {\\n  slug\\n  langSlug: lang_slug\\n  name\\n  temporarilyQualified: temporarily_qualified\\n  __typename\\n}\\nfragment MatchStatistic on Match {\\n  statistic {\\n    filteredPeriods: filtered_periods(\\n      period_types: [\\n\\\"total\\\"]\\n      stat_types: [\\n\\\"corner_kicks\\\", \\n\\\"cards_given\\\", \\n\\\"fouls\\\", \\n\\\"yellow_cards\\\", \\n\\\"xg\\\"]\\n    ) {\\n      type\\n      items {\\n        type\\n        team1Value: team1_value\\n        team2Value: team2_value\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\",\"variables\":{\"excludeLive\":true,\"isHorseRacing\":false,\"langSlug\":\"en\",\"limit\":15,\"matchSlug\":\"" + game["slug"] + "\",\"meetingType\":\"join\",\"skip\":0,\"sportSlug\":\"table-tennis\",\"teamType\":\"home\",\"withFriendly\":true,\"withMarkets\":false,\"withStatistics\":false}}"
        away_payload = "{\"operationName\":\"MatchH2HGamesMatches\",\"query\":\"query MatchH2HGamesMatches($matchSlug: String!, $sportSlug: String!, $langSlug: LangEnum!, $leagueSlug: String, $limit: Int, $skip: Int, $meetingType: MeetingTypeEnum!, $teamType: TeamTypeEnum, $excludeLive: Boolean!, $withFriendly: Boolean, $isHorseRacing: Boolean!, $withMarkets: Boolean!, $withStatistics: Boolean!) {\\n  TeamMatches(\\n    exclude_live: $excludeLive\\n    lang: $langSlug\\n    sport_slug: $sportSlug\\n    match_slug: $matchSlug\\n    league_slug: $leagueSlug\\n    team_type: $teamType\\n    limit: $limit\\n    skip: $skip\\n    meeting_type: $meetingType\\n    match_status: past\\n    with_friendly: $withFriendly\\n  ) {\\n    ...NewCalendarMatch\\n    ...MatchStatistic @include(if: $withStatistics)\\n    __typename\\n  }\\n}\\nfragment NewCalendarMatch on Match {\\n  ...MatchCacheFragment\\n  ...HorseMatch @include(if: $isHorseRacing)\\n  ...MarketsFragment @include(if: $withMarkets)\\n  gameState: game_state {\\n    home: home_score\\n    away: away_score\\n    __typename\\n  }\\n  type\\n  broadcasts {\\n    livestream\\n    __typename\\n  }\\n  addMinute: add_minute\\n  serving\\n  sportSlug: sport_slug\\n  gameScore: game_score\\n  resultScore: result_score\\n  hasOdds: has_odds\\n  hasH2h: has_h2h\\n  hasSquads: has_squads\\n  hasStandings: has_standings\\n  hasPrediction: has_prediction\\n  resultScores: result_scores {\\n    awayTiebreakScore: away_tiebreak_score\\n    homeTiebreakScore: home_tiebreak_score\\n    type\\n    value\\n    __typename\\n  }\\n  server\\n  leagueSlug: league_slug\\n  cards {\\n    color\\n    team\\n    __typename\\n  }\\n  country {\\n    ...CountryFragment\\n    __typename\\n  }\\n  tournamentName: tournament_name\\n  uniqueTournament: unique_tournament {\\n    ...LeagueCacheFragment\\n    slug\\n    shortName: short_name\\n    __typename\\n  }\\n  uniqueTournamentName: unique_tournament_name\\n  teams {\\n    ...TeamCacheFragment\\n    id\\n    name\\n    logo\\n    country {\\n      iso\\n      __typename\\n    }\\n    __typename\\n  }\\n  status {\\n    code\\n    __typename\\n  }\\n  isLive: is_live\\n  isFinished: is_finished\\n  minute\\n  tiebreak\\n  winner\\n  __typename\\n}\\nfragment HorseMatch on Match {\\n  surface\\n  name\\n  distance\\n  purse\\n  uniqueTournament: unique_tournament {\\n    going\\n    __typename\\n  }\\n  teams {\\n    name\\n    slug\\n    jockeyName: jockey_name\\n    jockeySlug: jockey_slug\\n    trainerName: trainer_name\\n    trainerSlug: trainer_slug\\n    odd\\n    sp\\n    wgt\\n    wgtLbs: wgt_lbs\\n    age\\n    rating\\n    position\\n    distance\\n    gender\\n    __typename\\n  }\\n  __typename\\n}\\nfragment MarketsFragment on Match {\\n  markets {\\n    bookmaker {\\n      ...BookmakerCacheFragment\\n      slug\\n      name\\n      logo\\n      favicon\\n      legal\\n      color\\n      url\\n      __typename\\n    }\\n    name\\n    value\\n    __typename\\n  }\\n  bkmUrls: bkm_urls {\\n    bookmaker\\n    url\\n    __typename\\n  }\\n  __typename\\n}\\nfragment BookmakerCacheFragment on Bookmaker {\\n  slug\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment MatchCacheFragment on Match {\\n  slug\\n  matchDate: match_date\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment CountryFragment on Country {\\n  name\\n  slug\\n  iso\\n  __typename\\n}\\nfragment LeagueCacheFragment on League {\\n  slug\\n  langSlug: lang_slug\\n  sportSlug: sport_slug\\n  __typename\\n}\\nfragment TeamCacheFragment on Team {\\n  slug\\n  langSlug: lang_slug\\n  name\\n  temporarilyQualified: temporarily_qualified\\n  __typename\\n}\\nfragment MatchStatistic on Match {\\n  statistic {\\n    filteredPeriods: filtered_periods(\\n      period_types: [\\n\\\"total\\\"]\\n      stat_types: [\\n\\\"corner_kicks\\\", \\n\\\"cards_given\\\", \\n\\\"fouls\\\", \\n\\\"yellow_cards\\\", \\n\\\"xg\\\"]\\n    ) {\\n      type\\n      items {\\n        type\\n        team1Value: team1_value\\n        team2Value: team2_value\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\",\"variables\":{\"excludeLive\":true,\"isHorseRacing\":false,\"langSlug\":\"en\",\"limit\":15,\"matchSlug\":\"" + game["slug"] + "\",\"meetingType\":\"join\",\"skip\":0,\"sportSlug\":\"table-tennis\",\"teamType\":\"away\",\"withFriendly\":true,\"withMarkets\":false,\"withStatistics\":false}}"

        conn.request("POST", "/graphql", loop_h2h_payload, headers)

        h2h_res = conn.getresponse()
        h2h_data = h2h_res.read()
        h2h_json_res = json.loads(h2h_data.decode("utf-8"))

#        conn.request("POST", "/graphql", home_payload, headers)

#        home_res = conn.getresponse()
#        home_data = home_res.read()
#        home_json_res = json.loads(home_data.decode("utf-8"))

#        conn.request("POST", "/graphql", away_payload, headers)

#        away_res = conn.getresponse()
#        away_data = away_res.read()
#        away_json_res = json.loads(away_data.decode("utf-8"))

        game_counter = 0
        over_counter = 0
        four_round_counter = 0
        bet_amt = "0.25u"
        out_of_5 = 0
        out_of_10 = 0
        out_of_15 = 0
        out_of_20 = 0
        out_of_25 = 0
        out_of_30 = 0
        home_wins = 0
        total_out_of_5 = "XXX"
        total_out_of_10 = "XXX"
        total_out_of_15 = "XXX"
        total_out_of_25 = "XXX"
        total_out_of_20 = "XXX"
        total_out_of_30 = "XXX"
        raw_total_out_of_5 = 0
        raw_total_out_of_10 = 0
        raw_total_out_of_15 = 0
        scores_array = []
        home_scores_array = []
        away_scores_array = []
        game_totals_array = []
        home_game_totals = []
        away_game_totals = []
        dataset_array = []
        dates_array = []
        game_object = {}
        confidence_floor = 0
        confidence_ceiling = 0
        confidence_interval = 0
        average_score = 0
        home_team_1st_set_counter = 0
        home_team_spread_counter = 0
        away_team_spread_counter = 0
        target = ""
        if(len(h2h_json_res["data"]["TeamMatches"]) > 0):
            for index, elem in enumerate(h2h_json_res["data"]["TeamMatches"]):
                # print(elem["slug"] + " : " + elem["matchDate"] + " : " + elem["resultScore"])
                temp_total_score = 0
                game_total = 0
                game_counter += 1
                home_total_score = 0
                away_total_score = 0
                if(elem["resultScores"]):
                    for match in elem["resultScores"]:
                        if (match["type"] != "FT"):
                            split_list = match["value"].split(":")
                            if(match['type'] == '1'):
                                if(int(split_list[0]) - int(split_list[1]) > 2 and index < 12):
                                    home_team_spread_counter += 1
                                if(int(split_list[1]) - int(split_list[0]) > 2 and index < 12):
                                    away_team_spread_counter += 1
                                if(int(split_list[0]) > int(split_list[1])):
                                    home_team_1st_set_counter += 1
                            temp_total_score  +=  sum([int(i) for i in split_list if type(i) == int or i.isdigit()])
                            home_total_score += int(split_list[0])
                            away_total_score += int(split_list[1])
                        else:
                            split_game_total = match["value"].split(":")
                            if(int(split_game_total[0]) > int(split_game_total[1])):
                                home_wins += 1
                            game_total +=  sum([int(i) for i in split_game_total if type(i) == int or i.isdigit()])
                            home_game_totals.append(int(split_game_total[0]))
                            away_game_totals.append(int(split_game_total[1]))

                home_scores_array.append(home_total_score)
                away_scores_array.append(away_total_score)
                

                # {
                #   Labels: [dates],
                #   datasets: {
                #       labels: [],
                #       data: [scores]
                #   } 
                # } 
                game_totals_array.append(game_total)            
                scores_array.append(temp_total_score)
                dates_array.append((datetime.strptime(elem["matchDate"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'))
                dataset_array = [
                    {
                        "label": game["teams"][0]["name"],
                        "data": home_scores_array
                    },
                    {
                        "label": game["teams"][1]["name"],
                        "data": away_scores_array
                    }
                ]
                game_dataset_array = [
                    {
                        "label": game["teams"][0]["name"],
                        "data": home_game_totals 
                    },
                    {
                        "label": game["teams"][1]["name"],
                        "data": away_game_totals
                    }
                ]

                if(temp_total_score  > 74):
                    over_counter += 1

                if(index < 5):
                    if(temp_total_score > 74):
                        out_of_5 += 1
                    total_out_of_5 = f"{out_of_5} / {index + 1}"
                elif(index >= 5 and index < 10):
                    if(temp_total_score > 74):
                        out_of_10 += 1
                    total_out_of_10 = f"{out_of_5 + out_of_10} / {index + 1}"
                elif(index >= 10 and index < 15):
                    if(temp_total_score > 74):
                        out_of_15 += 1
                    total_out_of_15 = f"{out_of_5 + out_of_10 + out_of_15} / {index + 1}"
                elif(index >= 15 and index < 20):
                    if(temp_total_score > 74):
                        out_of_20 += 1
                    total_out_of_20 = f"{out_of_5 + out_of_10 + out_of_15 + out_of_20} / {index + 1}"
                elif(index >= 20 and index < 25):
                    if(temp_total_score > 74):
                        out_of_25 += 1
                    total_out_of_25 = f"{out_of_5 + out_of_10 + out_of_15 + out_of_20 + out_of_25} / {index + 1}"
                else:
                    if(temp_total_score > 74):
                        out_of_30 += 1
                    total_out_of_30 = f"{out_of_5 + out_of_10 + out_of_15 + out_of_20 + out_of_25 + out_of_30} / {index + 1}"

                if(game_total >= 4):
                    four_round_counter += 1

            # print(elem["teams"][0]["name"] + " vs. " + elem["teams"][1]["name"] + f" - Total Points: {total} - Total Games: {game_total}")


        raw_total_out_of_5 = out_of_5
        raw_total_out_of_10 = out_of_5 + out_of_10
        raw_total_out_of_15 = raw_total_out_of_10 + out_of_15
        raw_total_out_of_20 = raw_total_out_of_15 + out_of_20
        raw_total_out_of_25 = raw_total_out_of_20 + out_of_25
        raw_total_out_of_30 = raw_total_out_of_25 + out_of_30

        divisor_10 = 10 if game_counter > 10 else game_counter
        divisor_15 = 15 if game_counter > 15 else game_counter


        if(game_counter > 0):
            # print(scores_array)
            std_dev = statistics.pstdev(scores_array)
            average_score = statistics.mean(scores_array)
            # print("avg", average_score)
            # print("std deviation", std_dev)
            # Confidence Level:
            # 70%	1.036
            # 75%	1.150
            # 80%	1.282
            # 85%	1.440
            # 90%	1.645
            # 95%	1.960 ***
            # 98%	2.326
            # 99%	2.576
            # 99.5%	2.807
            # 99.9%	3.291
            # 99.99%	3.891
            # 99.999%	4.417

            confidence_interval = (1.960 * (std_dev / math.sqrt(game_counter)))

            confidence_floor = average_score - confidence_interval
            confidence_ceiling = average_score + confidence_interval

            if(game_counter >= 11):
                if(raw_total_out_of_10 == 7):
                    if((.7 <= (raw_total_out_of_15/divisor_15) < .80) and (70 <= confidence_floor <= 78.5)):
                        if(raw_total_out_of_5 < 4):
                            bet_amt = "0.25u"
                        else:
                            bet_amt = "0.25u"
                    elif(raw_total_out_of_15/divisor_15 >= .80 and confidence_floor < 78.5):
                        bet_amt = "1u"
                    elif(raw_total_out_of_15/divisor_15 >= .80 and confidence_floor > 78.5):
                        bet_amt = "1u"
                    elif(raw_total_out_of_15 == 11 and raw_total_out_of_5 == 5):
                        bet_amt = "1u"
                if(raw_total_out_of_10 == 8):
                    bet_amt= "0.25u" if raw_total_out_of_5 < 4 else "1u"
                    if((.75 <= (raw_total_out_of_15/divisor_15) < .80) and (70 <= confidence_floor <= 78.5)):
                        bet_amt = "1u"
                    elif(raw_total_out_of_15/divisor_15 >= .80 and confidence_floor < 78):
                        bet_amt = "1.25u"
                    elif(raw_total_out_of_15/divisor_15 >= .80 and confidence_floor >= 78):
                        bet_amt = "1.5u"
                    elif(raw_total_out_of_15 == 11 and raw_total_out_of_5 >= 4):
                        bet_amt = "1u"
                if(raw_total_out_of_10 == 9):
                    bet_amt = "1u"
                    if((.7 <= (raw_total_out_of_15/divisor_15) < .80) and (70 <= confidence_floor <= 78.5)):
                        bet_amt = "1.25u"
                    elif(raw_total_out_of_15/divisor_15 >= .80 and confidence_floor < 78.5):
                        bet_amt = "1.5u"
                    elif(.80 < raw_total_out_of_15/divisor_15 < .90 and confidence_floor < 78.5):
                        bet_amt = "1.5u"
                    elif(.80 < raw_total_out_of_15/divisor_15 < .90 and confidence_floor >= 78.5):
                        bet_amt = "1.75u"
                    elif(raw_total_out_of_15/divisor_15 >= .90):
                        bet_amt = "2u"
                if(raw_total_out_of_10 == 10):
                    bet_amt="1.25u"
                    if((.7 <= (raw_total_out_of_15/divisor_15) < .80) and (70 <= confidence_floor <= 78.5)):
                        bet_amt = "1.5u"
                    elif(raw_total_out_of_15/divisor_15 >= .80 and confidence_floor < 78.5):
                        bet_amt = "1.75u"
                    elif(raw_total_out_of_15/divisor_15 >= .80 and confidence_floor >= 78.5):
                        bet_amt = "2u"
            
            if(5<= game_counter < 11):
                if(over_counter == game_counter):
                    bet_amt = "0.5u"

            if(confidence_floor < 70 and bet_amt in ["1u", "1.25u", "1.5u", "1.75u", "2u"]):
                bet_amt = "0.75u"

            if(over_counter/game_counter < .7 and bet_amt in ["1u", "1.25u", "1.5u", "1.75u", "2u"]):
                bet_amt = "0.75u"
            
            if(raw_total_out_of_5 < 3 and bet_amt in ["1u", "1.25u", "1.5u", "1.75u", "2u"]):
                bet_amt = "0.75u"
            
            # if(raw_total_out_of_15 <= 3 and game_counter > 13 and (over_counter/game_counter) <= .30 and raw_total_out_of_5 == 1):
            #     bet_amt = "1u UNDER"
            # elif(raw_total_out_of_10 <= 2 and raw_total_out_of_15 <= 4 and game_counter >=10 and (over_counter/game_counter) <= .30):
            #     bet_amt = "0.75u"

            

            if(game["teams"][0]["name"] in ["Bartlomiej Wisniewski", "Jaroslaw Rolak"] and game["teams"][1]["name"] in ["Bartlomiej Wisniewski", "Jaroslaw Rolak"]):
                target = "set o18.5/+3.5"
            else:
                target = "74.5"

#            if(game_counter >= 12):
#                if(confidence_floor > 73.5 and confidence_floor < 79.5):
#                    if(((over_counter/game_counter) >= .7) and ((over_counter/game_counter) < .9) and ((out_of_10 + out_of_15 + out_of_5) < 12)):
#                        bet_amt = "1u"
#                    elif(((over_counter/game_counter) >= .9) or ((out_of_10 + out_of_15 + out_of_5 >= 12))):
#                        bet_amt = "1.25u"
#                elif(confidence_floor >= 79.5 and confidence_floor < 84.5):
#                    if((over_counter/game_counter) >= .7 and ((over_counter/game_counter) < .8) and ((out_of_10 + out_of_15 + out_of_5) < 12)):
#                        bet_amt = "1.25u"
#                    elif(((over_counter/game_counter) >= .8) or ((out_of_10 + out_of_15 + out_of_5 >= 12))):
#                        bet_amt = "1.5u"
#                elif(confidence_floor >= 84.5):
#                    if((over_counter/game_counter) >= .7 and ((over_counter/game_counter) < .85) and ((out_of_10 + out_of_15 + out_of_5) < 12)):
#                        bet_amt = "1.5u"
#                    elif((over_counter/game_counter) >= .85 or ((out_of_5 + out_of_10 + out_of_15) >= 12)):
#                        bet_amt = "2u"

            game_object = {
                "date": (datetime.strptime(game["matchDate"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'),
                "home_player": game["teams"][0]["name"],
                "away_player": game["teams"][1]["name"],
                "confidence": f"{average_score:.1f} ±{confidence_interval:.3f}",
                "ci_interval": f"[{confidence_floor:.1f} - {confidence_ceiling:.1f}]",
                "target": target,
                "bet_amt": bet_amt,
                "total_over": f"{over_counter} / {game_counter}",
                "hit_rate": f"{(over_counter/game_counter) * 100:.2f}%",
                "last_5": total_out_of_5,
                "last_10": total_out_of_10,
                "last_15": total_out_of_15,
                "last_20": total_out_of_20,
                "last_25": total_out_of_25,
                "last_30": total_out_of_30,
                "over_four": f"{four_round_counter} / {game_counter}",
                "four_rate": f"{(four_round_counter/game_counter) * 100:.2f}%",
                "slug": game["slug"],
                "home_wins": f"{home_wins} / {game_counter}",
                "home_wins_percent": f"{(home_wins/game_counter) * 100:.2f}%",
                "four_round": round(four_round_counter/game_counter, 2),
                "home_team_1st": home_team_1st_set_counter,
                "home_team_1st_percent": f"{(home_team_1st_set_counter/game_counter) * 100:.2f}%",
                "home_team_1st_raw": round(home_team_1st_set_counter/game_counter, 2),
                "home_team_spread": home_team_spread_counter,
                "home_team_spread_percent": round(home_team_spread_counter/game_counter, 2),
                "away_team_1st": game_counter - home_team_1st_set_counter,
                "away_team_1st_percent": round((game_counter - home_team_1st_set_counter)/game_counter, 2),
                "away_team_1st_raw": round((game_counter - home_team_1st_set_counter)/game_counter, 2),
                "away_team_spread": away_team_spread_counter,
                "away_team_spread_percent": round(away_team_spread_counter/game_counter, 2),
                "score_array": scores_array,
                "raw_last_5": raw_total_out_of_5,
                "raw_last_10": raw_total_out_of_10,
                "raw_last_15": raw_total_out_of_15,
                "raw_last_20": raw_total_out_of_20,
                "raw_last_25": raw_total_out_of_25,
                "raw_last_30": raw_total_out_of_30,
                "raw_hit_rate": round(over_counter/game_counter, 2),
                "raw_total_over": over_counter,
                "average_score": round(average_score, 2),
                "confidence_interval": round(confidence_interval, 2),
                "confidence_floor": round(confidence_floor, 2),
                "confidence_ceiling": round(confidence_ceiling, 2),
                "dataset_array": dataset_array,
                "labels": dates_array,
                "game_dataset_array": game_dataset_array,
                "game_totals_array": game_totals_array
            }

            if(bet_amt not in ["0.25u", "0.5u", "0.75u"]):
                best_plays_array.append(game_object)
                message_notification += f"{game_object['date']}\n{game_object['home_player']} vs. {game_object['away_player']}\nOVER 74.5 - Bet Amt:{game_object['bet_amt']}\n{game_object['confidence']} - {game_object['ci_interval']}\n\n"

            if((((four_round_counter/game_counter) * 100) >= 90) and game_counter >= 10):
                four_round_plays_array.append(game_object)

            if(((home_team_1st_set_counter/game_counter) > .80 or ((game_counter-home_team_1st_set_counter)/game_counter) > .80) and game_counter >= 10):
                first_set_plays_array.append(game_object)
                first_set_notification += f"{game_object['date']}\n{game_object['home_player']} vs. {game_object['away_player']}\nFirst Set win - Bet Amt: 0.5u\nHome: {game_object['home_team_1st_percent']} -- Away: {game_object['away_team_1st_percent']}\n\n"
            
            if(game_counter > 6 and ((home_team_spread_counter/game_counter) > .65 or (away_team_spread_counter/game_counter) > .65)):
                spread_plays_array.append(game_object)

            all_plays_array.append(game_object)

        # print(game["slug"] + f": Over - {over_counter} / {game_counter} | Last 5 - {out_of_5} / 5 | Last 10 - {out_of_10 + out_of_5} / 10")


    write_json = json.dumps(best_plays_array, indent=4)
    with open("data/table-tennis-best-plays.json", "w") as outfile:
        outfile.write(write_json)

    write_all_json = json.dumps(all_plays_array, indent=4)
    with open("data/table-tennis-all-plays.json", "w") as outfile:
        outfile.write(write_all_json)

    df = pd.json_normalize(all_plays_array)

    df.to_csv('data/tt-all-plays-updated.csv', index=False)

    message = user.send_message(
                    title= "TT Data Script Has Completed",
                    message=message_notification[0:900]
    )

    df = pd.json_normalize(best_plays_array)

    df.to_csv('data/tt-best-plays-updated.csv', index=False)

    df = pd.json_normalize(four_round_plays_array)

    df.to_csv('data/tt-four-or-more-plays-updated.csv', index=False)

    df = pd.json_normalize(first_set_plays_array)

    df.to_csv('data/tt-first-set-plays.csv', index=False)

    df = pd.json_normalize(spread_plays_array)

    df.to_csv('data/tt-spread-plays.csv', index=False)

    # if(len(first_set_plays_array) > 0):
    #    user.send_message(
    #        title="TT Upcoming First Set Plays",
    #        message=first_set_notification[0:900]
    #    )

    # conn.request("POST", "/graphql", h2h_payload, headers)

    # res2 = conn.getresponse()
    # data2 = res2.read()
    # h2h_json_resp = json.loads(data2.decode("utf-8"))

    # print(h2h_json_resp["data"]["TeamMatches"][0])
    # for elem in h2h_json_resp["data"]["TeamMatches"]:
    #     total = 0
    #     for match in elem["resultScores"]:
    #        split_list = match["value"].split(":")
    #        total += sum([int(i) for i in split_list if type(i)== int or i.isdigit()])
    #     print(elem["slug"] + " : " + elem["matchDate"] + " : " + f"{total}" + " : " + elem["resultScore"])
    # print(data.decode("utf-8"))


if __name__ == "__main__":
    # Get the function argument from the command line
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else "World"

        if function_name == "run_data_script":
            run_data_script()
        else:
            print(f"Function '{function_name}' not found.")
    else:
        print("No function name provided.")

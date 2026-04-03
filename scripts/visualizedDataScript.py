import http.client
import json
import time
import pandas as pd # type: ignore
from datetime import datetime, timedelta
import statistics
import math
from chump import Application
import sys


def run_script():
    try:
        conn = http.client.HTTPSConnection("scores24.live")
        app = Application("ahey4sok8gixmc2e5xqfynky4ah1x4")
        user = app.get_user("u6ypbjv8t8jqzoodhktnkriw5bjz12")

        dateNow = "2024-11-28 02:00:00"

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

        h2h_plays_array = []
        h_plays_array = []
        a_plays_array = []

        for index, game in enumerate(json_resp["data"]["MatchList"]):
            h2h_game_object = {}
            h_game_object = {}
            a_game_object = {}

            loop_h2h_payload = "{\"operationName\":\"MatchH2HGamesMatches\",\"query\":\"query MatchH2HGamesMatches($matchSlug: String!, $sportSlug: String!, $langSlug: LangEnum!, $leagueSlug: String, $limit: Int, $skip: Int, $meetingType: MeetingTypeEnum!, $teamType: TeamTypeEnum, $excludeLive: Boolean!, $withFriendly: Boolean, $isHorseRacing: Boolean!, $withMarkets: Boolean!, $withStatistics: Boolean!) {\\n  TeamMatches(\\n    exclude_live: $excludeLive\\n    lang: $langSlug\\n    sport_slug: $sportSlug\\n    match_slug: $matchSlug\\n    league_slug: $leagueSlug\\n    team_type: $teamType\\n    limit: $limit\\n    skip: $skip\\n    meeting_type: $meetingType\\n    match_status: past\\n    with_friendly: $withFriendly\\n  ) {\\n    ...NewCalendarMatch\\n    ...MatchStatistic @include(if: $withStatistics)\\n    __typename\\n  }\\n}\\nfragment NewCalendarMatch on Match {\\n  ...MatchCacheFragment\\n  ...HorseMatch @include(if: $isHorseRacing)\\n  ...MarketsFragment @include(if: $withMarkets)\\n  gameState: game_state {\\n    home: home_score\\n    away: away_score\\n    __typename\\n  }\\n  type\\n  broadcasts {\\n    livestream\\n    __typename\\n  }\\n  addMinute: add_minute\\n  serving\\n  sportSlug: sport_slug\\n  gameScore: game_score\\n  resultScore: result_score\\n  hasOdds: has_odds\\n  hasH2h: has_h2h\\n  hasSquads: has_squads\\n  hasStandings: has_standings\\n  hasPrediction: has_prediction\\n  resultScores: result_scores {\\n    awayTiebreakScore: away_tiebreak_score\\n    homeTiebreakScore: home_tiebreak_score\\n    type\\n    value\\n     __typename\\n  }\\n  server\\n  leagueSlug: league_slug\\n  cards {\\n    color\\n    team\\n    __typename\\n  }\\n  country {\\n    iso\\n    slug\\n    __typename\\n  }\\n  tournamentName: tournament_name\\n  uniqueTournament: unique_tournament {\\n    ...LeagueCacheFragment\\n    slug\\n    shortName: short_name\\n    __typename\\n  }\\n  uniqueTournamentName: unique_tournament_name\\n  teams {\\n    ...TeamCacheFragment\\n    id\\n    name\\n    logo\\n    country {\\n      iso\\n      __typename\\n    }\\n    __typename\\n  }\\n  status {\\n    code\\n    __typename\\n  }\\n  isLive: is_live\\n  isFinished: is_finished\\n  minute\\n  tiebreak\\n  winner\\n  __typename\\n}\\nfragment HorseMatch on Match {\\n  surface\\n  name\\n  distance\\n  purse\\n  uniqueTournament: unique_tournament {\\n    going\\n    __typename\\n  }\\n  teams {\\n    name\\n    slug\\n    jockeyName: jockey_name\\n    jockeySlug: jockey_slug\\n    trainerName: trainer_name\\n    trainerSlug: trainer_slug\\n    odd\\n    sp\\n    wgt\\n    wgtLbs: wgt_lbs\\n    age\\n    rating\\n    position\\n    distance\\n    gender\\n    __typename\\n  }\\n  __typename\\n}\\nfragment MarketsFragment on Match {\\n  markets {\\n    bookmaker {\\n      ...BookmakerCacheFragment\\n      slug\\n      name\\n      logo\\n      favicon\\n      legal\\n      color\\n      url\\n      __typename\\n    }\\n    name\\n    value\\n    __typename\\n  }\\n  bkmUrls: bkm_urls {\\n    bookmaker\\n    url\\n    __typename\\n  }\\n  __typename\\n}\\nfragment BookmakerCacheFragment on Bookmaker {\\n  slug\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment MatchCacheFragment on Match {\\n  slug\\n  matchDate: match_date\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment LeagueCacheFragment on League {\\n  slug\\n  langSlug: lang_slug\\n  sportSlug: sport_slug\\n  __typename\\n}\\nfragment TeamCacheFragment on Team {\\n  slug\\n  langSlug: lang_slug\\n  name\\n  temporarilyQualified: temporarily_qualified\\n  __typename\\n}\\nfragment MatchStatistic on Match {\\n  statistic {\\n    filteredPeriods: filtered_periods(\\n      period_types: [\\n\\\"total\\\"]\\n      stat_types: [\\n\\\"corner_kicks\\\", \\n\\\"cards_given\\\", \\n\\\"fouls\\\", \\n\\\"yellow_cards\\\", \\n\\\"xg\\\"]\\n    ) {\\n      type\\n      items {\\n        type\\n        team1Value: team1_value\\n        team2Value: team2_value\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\",\"variables\":{\"excludeLive\":true,\"isHorseRacing\":false,\"langSlug\":\"en\",\"limit\":30,\"matchSlug\":\"" + game["slug"] + "\",\"meetingType\":\"join\",\"skip\":0,\"sportSlug\":\"table-tennis\",\"withFriendly\":false,\"withMarkets\":false,\"withStatistics\":false}}"
            home_payload = "{\"operationName\":\"MatchH2HGamesMatches\",\"query\":\"query MatchH2HGamesMatches($matchSlug: String!, $sportSlug: String!, $langSlug: LangEnum!, $leagueSlug: String, $limit: Int, $skip: Int, $meetingType: MeetingTypeEnum!, $teamType: TeamTypeEnum, $excludeLive: Boolean!, $withFriendly: Boolean, $isHorseRacing: Boolean!, $withMarkets: Boolean!, $withStatistics: Boolean!) {\\n  TeamMatches(\\n    exclude_live: $excludeLive\\n    lang: $langSlug\\n    sport_slug: $sportSlug\\n    match_slug: $matchSlug\\n    league_slug: $leagueSlug\\n    team_type: $teamType\\n    limit: $limit\\n    skip: $skip\\n    meeting_type: $meetingType\\n    match_status: past\\n    with_friendly: $withFriendly\\n  ) {\\n    ...NewCalendarMatch\\n    ...MatchStatistic @include(if: $withStatistics)\\n    __typename\\n  }\\n}\\nfragment NewCalendarMatch on Match {\\n  ...MatchCacheFragment\\n  ...HorseMatch @include(if: $isHorseRacing)\\n  ...MarketsFragment @include(if: $withMarkets)\\n  gameState: game_state {\\n    home: home_score\\n    away: away_score\\n    __typename\\n  }\\n  type\\n  broadcasts {\\n    livestream\\n    __typename\\n  }\\n  addMinute: add_minute\\n  serving\\n  sportSlug: sport_slug\\n  gameScore: game_score\\n  resultScore: result_score\\n  hasOdds: has_odds\\n  hasH2h: has_h2h\\n  hasSquads: has_squads\\n  hasStandings: has_standings\\n  hasPrediction: has_prediction\\n  resultScores: result_scores {\\n    awayTiebreakScore: away_tiebreak_score\\n    homeTiebreakScore: home_tiebreak_score\\n    type\\n    value\\n    __typename\\n  }\\n  server\\n  leagueSlug: league_slug\\n  cards {\\n    color\\n    team\\n    __typename\\n  }\\n  country {\\n    ...CountryFragment\\n    __typename\\n  }\\n  tournamentName: tournament_name\\n  uniqueTournament: unique_tournament {\\n    ...LeagueCacheFragment\\n    slug\\n    shortName: short_name\\n    __typename\\n  }\\n  uniqueTournamentName: unique_tournament_name\\n  teams {\\n    ...TeamCacheFragment\\n    id\\n    name\\n    logo\\n    country {\\n      iso\\n      __typename\\n    }\\n    __typename\\n  }\\n  status {\\n    code\\n    __typename\\n  }\\n  isLive: is_live\\n  isFinished: is_finished\\n  minute\\n  tiebreak\\n  winner\\n  __typename\\n}\\nfragment HorseMatch on Match {\\n  surface\\n  name\\n  distance\\n  purse\\n  uniqueTournament: unique_tournament {\\n    going\\n    __typename\\n  }\\n  teams {\\n    name\\n    slug\\n    jockeyName: jockey_name\\n    jockeySlug: jockey_slug\\n    trainerName: trainer_name\\n    trainerSlug: trainer_slug\\n    odd\\n    sp\\n    wgt\\n    wgtLbs: wgt_lbs\\n    age\\n    rating\\n    position\\n    distance\\n    gender\\n    __typename\\n  }\\n  __typename\\n}\\nfragment MarketsFragment on Match {\\n  markets {\\n    bookmaker {\\n      ...BookmakerCacheFragment\\n      slug\\n      name\\n      logo\\n      favicon\\n      legal\\n      color\\n      url\\n      __typename\\n    }\\n    name\\n    value\\n    __typename\\n  }\\n  bkmUrls: bkm_urls {\\n    bookmaker\\n    url\\n    __typename\\n  }\\n  __typename\\n}\\nfragment BookmakerCacheFragment on Bookmaker {\\n  slug\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment MatchCacheFragment on Match {\\n  slug\\n  matchDate: match_date\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment CountryFragment on Country {\\n  name\\n  slug\\n  iso\\n  __typename\\n}\\nfragment LeagueCacheFragment on League {\\n  slug\\n  langSlug: lang_slug\\n  sportSlug: sport_slug\\n  __typename\\n}\\nfragment TeamCacheFragment on Team {\\n  slug\\n  langSlug: lang_slug\\n  name\\n  temporarilyQualified: temporarily_qualified\\n  __typename\\n}\\nfragment MatchStatistic on Match {\\n  statistic {\\n    filteredPeriods: filtered_periods(\\n      period_types: [\\n\\\"total\\\"]\\n      stat_types: [\\n\\\"corner_kicks\\\", \\n\\\"cards_given\\\", \\n\\\"fouls\\\", \\n\\\"yellow_cards\\\", \\n\\\"xg\\\"]\\n    ) {\\n      type\\n      items {\\n        type\\n        team1Value: team1_value\\n        team2Value: team2_value\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\",\"variables\":{\"excludeLive\":true,\"isHorseRacing\":false,\"langSlug\":\"en\",\"limit\":30,\"matchSlug\":\"" + game["slug"] + "\",\"meetingType\":\"join\",\"skip\":0,\"sportSlug\":\"table-tennis\",\"teamType\":\"home\",\"withFriendly\":true,\"withMarkets\":false,\"withStatistics\":false}}"
            away_payload = "{\"operationName\":\"MatchH2HGamesMatches\",\"query\":\"query MatchH2HGamesMatches($matchSlug: String!, $sportSlug: String!, $langSlug: LangEnum!, $leagueSlug: String, $limit: Int, $skip: Int, $meetingType: MeetingTypeEnum!, $teamType: TeamTypeEnum, $excludeLive: Boolean!, $withFriendly: Boolean, $isHorseRacing: Boolean!, $withMarkets: Boolean!, $withStatistics: Boolean!) {\\n  TeamMatches(\\n    exclude_live: $excludeLive\\n    lang: $langSlug\\n    sport_slug: $sportSlug\\n    match_slug: $matchSlug\\n    league_slug: $leagueSlug\\n    team_type: $teamType\\n    limit: $limit\\n    skip: $skip\\n    meeting_type: $meetingType\\n    match_status: past\\n    with_friendly: $withFriendly\\n  ) {\\n    ...NewCalendarMatch\\n    ...MatchStatistic @include(if: $withStatistics)\\n    __typename\\n  }\\n}\\nfragment NewCalendarMatch on Match {\\n  ...MatchCacheFragment\\n  ...HorseMatch @include(if: $isHorseRacing)\\n  ...MarketsFragment @include(if: $withMarkets)\\n  gameState: game_state {\\n    home: home_score\\n    away: away_score\\n    __typename\\n  }\\n  type\\n  broadcasts {\\n    livestream\\n    __typename\\n  }\\n  addMinute: add_minute\\n  serving\\n  sportSlug: sport_slug\\n  gameScore: game_score\\n  resultScore: result_score\\n  hasOdds: has_odds\\n  hasH2h: has_h2h\\n  hasSquads: has_squads\\n  hasStandings: has_standings\\n  hasPrediction: has_prediction\\n  resultScores: result_scores {\\n    awayTiebreakScore: away_tiebreak_score\\n    homeTiebreakScore: home_tiebreak_score\\n    type\\n    value\\n    __typename\\n  }\\n  server\\n  leagueSlug: league_slug\\n  cards {\\n    color\\n    team\\n    __typename\\n  }\\n  country {\\n    ...CountryFragment\\n    __typename\\n  }\\n  tournamentName: tournament_name\\n  uniqueTournament: unique_tournament {\\n    ...LeagueCacheFragment\\n    slug\\n    shortName: short_name\\n    __typename\\n  }\\n  uniqueTournamentName: unique_tournament_name\\n  teams {\\n    ...TeamCacheFragment\\n    id\\n    name\\n    logo\\n    country {\\n      iso\\n      __typename\\n    }\\n    __typename\\n  }\\n  status {\\n    code\\n    __typename\\n  }\\n  isLive: is_live\\n  isFinished: is_finished\\n  minute\\n  tiebreak\\n  winner\\n  __typename\\n}\\nfragment HorseMatch on Match {\\n  surface\\n  name\\n  distance\\n  purse\\n  uniqueTournament: unique_tournament {\\n    going\\n    __typename\\n  }\\n  teams {\\n    name\\n    slug\\n    jockeyName: jockey_name\\n    jockeySlug: jockey_slug\\n    trainerName: trainer_name\\n    trainerSlug: trainer_slug\\n    odd\\n    sp\\n    wgt\\n    wgtLbs: wgt_lbs\\n    age\\n    rating\\n    position\\n    distance\\n    gender\\n    __typename\\n  }\\n  __typename\\n}\\nfragment MarketsFragment on Match {\\n  markets {\\n    bookmaker {\\n      ...BookmakerCacheFragment\\n      slug\\n      name\\n      logo\\n      favicon\\n      legal\\n      color\\n      url\\n      __typename\\n    }\\n    name\\n    value\\n    __typename\\n  }\\n  bkmUrls: bkm_urls {\\n    bookmaker\\n    url\\n    __typename\\n  }\\n  __typename\\n}\\nfragment BookmakerCacheFragment on Bookmaker {\\n  slug\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment MatchCacheFragment on Match {\\n  slug\\n  matchDate: match_date\\n  langSlug: lang_slug\\n  __typename\\n}\\nfragment CountryFragment on Country {\\n  name\\n  slug\\n  iso\\n  __typename\\n}\\nfragment LeagueCacheFragment on League {\\n  slug\\n  langSlug: lang_slug\\n  sportSlug: sport_slug\\n  __typename\\n}\\nfragment TeamCacheFragment on Team {\\n  slug\\n  langSlug: lang_slug\\n  name\\n  temporarilyQualified: temporarily_qualified\\n  __typename\\n}\\nfragment MatchStatistic on Match {\\n  statistic {\\n    filteredPeriods: filtered_periods(\\n      period_types: [\\n\\\"total\\\"]\\n      stat_types: [\\n\\\"corner_kicks\\\", \\n\\\"cards_given\\\", \\n\\\"fouls\\\", \\n\\\"yellow_cards\\\", \\n\\\"xg\\\"]\\n    ) {\\n      type\\n      items {\\n        type\\n        team1Value: team1_value\\n        team2Value: team2_value\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\",\"variables\":{\"excludeLive\":true,\"isHorseRacing\":false,\"langSlug\":\"en\",\"limit\":30,\"matchSlug\":\"" + game["slug"] + "\",\"meetingType\":\"join\",\"skip\":0,\"sportSlug\":\"table-tennis\",\"teamType\":\"away\",\"withFriendly\":true,\"withMarkets\":false,\"withStatistics\":false}}"

            conn.request("POST", "/graphql", loop_h2h_payload, headers)

            h2h_res = conn.getresponse()
            h2h_data = h2h_res.read()
            h2h_json_res = json.loads(h2h_data.decode("utf-8"))

            conn.request("POST", "/graphql", home_payload, headers)

            home_res = conn.getresponse()
            home_data = home_res.read()
            home_json_res = json.loads(home_data.decode("utf-8"))

            conn.request("POST", "/graphql", away_payload, headers)

            away_res = conn.getresponse()
            away_data = away_res.read()
            away_json_res = json.loads(away_data.decode("utf-8"))

            scores_array = []
            home_scores_array = []
            away_scores_array = []
            home_total_scores = []
            away_total_scores = []
            home_game_totals = []
            away_game_totals = []
            h_home_1st_scores = []
            h_away_1st_scores = []
            h_home_total_scores = []
            h_away_total_scores = []
            h_home_game_totals = []
            h_away_game_totals = []
            h_1_and_2_sets = []
            h_2_and_3_sets = []
            h_dates_array = []
            h_labels = []
            a_home_1st_scores = []
            a_away_1st_scores = []
            a_home_total_scores = []
            a_away_total_scores = []
            a_home_game_totals = []
            a_away_game_totals = []
            a_1_and_2_sets = []
            a_2_and_3_sets = []
            a_dates_array = []
            a_labels = []
            h2h_home_1st_scores = []
            h2h_away_1st_scores = []
            h2h_dates_array = []
            h2h_1_and_2_sets = []
            h2h_2_and_3_sets = []
            h2h_score_history = {"home": [], "away": []}
            home_score_history = {"home": [], "away": []}
            away_score_history = {"home": [], "away": []}
            mean = 0
            confidence_interval = 0

            print(f"Pulling Match {index} - {game['teams'][0]['name']} vs {game['teams'][1]['name']}")
            if(len(h2h_json_res["data"]["TeamMatches"]) > 0):
                for index, elem in enumerate(h2h_json_res["data"]["TeamMatches"]):
                    home_total = 0
                    away_total = 0
                    temp_total_score = 0
                    temp_first_round = 0 
                    temp_second_round = 0
                    temp_third_round = 0
                    temp_home_score_history = []
                    temp_away_score_history = []

                    if(game["teams"][0]["name"] == elem["teams"][0]["name"]):
                        home_team_index = 0
                        away_team_index = 1
                    else: 
                        home_team_index = 1
                        away_team_index = 0
                    if(elem["resultScores"]):
                        for match in elem["resultScores"]:
                            if (match["type"] != "FT"):
                                split_list = match["value"].split(":")

                                if(match["type"] == "1"):
                                    if(int(split_list[home_team_index]) > int(split_list[away_team_index])):
                                        temp_first_round = 1
                                    h2h_home_1st_scores.append(int(split_list[home_team_index]))
                                    h2h_away_1st_scores.append(int(split_list[away_team_index]))
                                if(match["type"] == "2"):
                                    if(int(split_list[home_team_index]) > int(split_list[away_team_index])):
                                        temp_second_round = 1
                                if(match["type"] == "3"):
                                    if(int(split_list[home_team_index]) > int(split_list[away_team_index])):
                                        temp_third_round = 1

                                temp_total_score += sum([int(i) for i in split_list if type(i) == int or i.isdigit()])
                                home_total += int(split_list[home_team_index])
                                away_total += int(split_list[away_team_index])
                                temp_home_score_history.append(int(split_list[home_team_index]))
                                temp_away_score_history.append(int(split_list[away_team_index]))
                            else:
                                split_game_total = match["value"].split(":")
                                home_game_totals.append(int(split_game_total[home_team_index]))
                                away_game_totals.append(int(split_game_total[away_team_index]))
                    
                    if (temp_first_round == 1 and temp_second_round == 1):
                        h2h_1_and_2_sets.append("H")
                    elif (temp_first_round == 0 and temp_second_round == 0):
                        h2h_1_and_2_sets.append("A")
                    else:
                        h2h_1_and_2_sets.append("S")

                    if (temp_second_round == 1 and temp_third_round == 1):
                        h2h_2_and_3_sets.append("H")
                    elif (temp_second_round == 0 and temp_third_round == 0):
                        h2h_2_and_3_sets.append("A")
                    else:
                        h2h_2_and_3_sets.append("S")

                    home_total_scores.append(home_total)
                    away_total_scores.append(away_total)
                    scores_array.append(temp_total_score)
                    h2h_score_history["home"].append(temp_home_score_history)
                    h2h_score_history["away"].append(temp_away_score_history)
                    h2h_dates_array.append((datetime.strptime(elem["matchDate"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'))

            for index, elem in enumerate(home_json_res["data"]["TeamMatches"]):
                home_total = 0
                away_total = 0
                temp_first_round = 0
                temp_second_round = 0
                temp_third_round = 0
                temp_home_score_history = []
                temp_opp_score_history = []
                
                if(game["teams"][0]["name"] == elem["teams"][0]["name"]):
                    home_team_index = 0
                    away_team_index = 1
                else: 
                    home_team_index = 1
                    away_team_index = 0
                
                for match in elem["resultScores"]:
                    if (match["type"] != "FT"):
                        split_list = match["value"].split(":")
                        if(match["type"] == "1"):
                            if(int(split_list[home_team_index]) > int(split_list[away_team_index])):
                                temp_first_round = 1
                            h_home_1st_scores.append(int(split_list[home_team_index]))
                            h_away_1st_scores.append(int(split_list[away_team_index]))
                        if(match["type"] == "2"):
                            if(int(split_list[home_team_index]) > int(split_list[away_team_index])):
                                temp_second_round = 1
                        if(match["type"] == "3"):
                            if(int(split_list[home_team_index]) > int(split_list[away_team_index])):
                                temp_third_round = 1
                        # Add option for set 1 & 2 and 2 & 3
                        # temp_total_score += sum([int(i) for i in split_list if type(i) == int or i.isdigit()])
                        home_total += int(split_list[home_team_index])
                        away_total += int(split_list[away_team_index])
                        temp_home_score_history.append(int(split_list[home_team_index]))
                        temp_opp_score_history.append(int(split_list[away_team_index]))
                    else:
                        split_game_total = match["value"].split(":")
                        h_home_game_totals.append(int(split_game_total[home_team_index]))
                        h_away_game_totals.append(int(split_game_total[away_team_index]))

                if (temp_first_round == 1 and temp_second_round == 1):
                    h_1_and_2_sets.append("H")
                elif (temp_first_round == 0 and temp_second_round == 0):
                    h_1_and_2_sets.append("A")
                else:
                    h_1_and_2_sets.append("S")

                if (temp_second_round == 1 and temp_third_round == 1):
                    h_2_and_3_sets.append("H")
                elif (temp_second_round == 0 and temp_third_round == 0):
                    h_2_and_3_sets.append("A")
                else:
                    h_2_and_3_sets.append("S") 

                h_home_total_scores.append(home_total)
                h_away_total_scores.append(away_total)
                h_labels.append(elem["teams"][away_team_index]["name"])
                home_score_history["home"].append(temp_home_score_history)
                home_score_history["away"].append(temp_opp_score_history)
                h_dates_array.append((datetime.strptime(elem["matchDate"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'))

            for index, elem in enumerate(away_json_res["data"]["TeamMatches"]):
                home_total = 0
                away_total = 0
                temp_first_round = 0
                temp_second_round = 0
                temp_third_round = 0
                temp_home_score_history = []
                temp_opp_score_history = []

                if(game["teams"][1]["name"] == elem["teams"][0]["name"]):
                    home_team_index = 1
                    away_team_index = 0
                else: 
                    home_team_index = 0
                    away_team_index = 1

                for match in elem["resultScores"]:
                    if (match["type"] != "FT"):
                        split_list = match["value"].split(":")
                        if(match["type"] == "1"):
                            if(int(split_list[home_team_index]) > int(split_list[away_team_index])):
                                temp_first_round = 1
                            a_home_1st_scores.append(int(split_list[home_team_index]))
                            a_away_1st_scores.append(int(split_list[away_team_index]))
                        if(match["type"] == "2"):
                            if(int(split_list[home_team_index]) > int(split_list[away_team_index])):
                                temp_second_round = 1
                        if(match["type"] == "3"):
                            if(int(split_list[home_team_index]) > int(split_list[away_team_index])):
                                temp_third_round = 1# Add option for set 1 & 2 and 2 & 3
                        # temp_total_score += sum([int(i) for i in split_list if type(i) == int or i.isdigit()])
                        home_total += int(split_list[home_team_index])
                        away_total += int(split_list[away_team_index])
                        temp_home_score_history.append(int(split_list[home_team_index]))
                        temp_opp_score_history.append(int(split_list[away_team_index]))
                    else:
                        split_game_total = match["value"].split(":")
                        a_home_game_totals.append(int(split_game_total[home_team_index]))
                        a_away_game_totals.append(int(split_game_total[away_team_index]))
                
                if (temp_first_round == 1 and temp_second_round == 1):
                    a_1_and_2_sets.append("H")
                elif (temp_first_round == 0 and temp_second_round == 0):
                    a_1_and_2_sets.append("A")
                else:
                    a_1_and_2_sets.append("S")

                if (temp_second_round == 1 and temp_third_round == 1):
                    a_2_and_3_sets.append("H")
                elif (temp_second_round == 0 and temp_third_round == 0):
                    a_2_and_3_sets.append("A")
                else:
                    a_2_and_3_sets.append("S") 

                a_home_total_scores.append(home_total)
                a_away_total_scores.append(away_total)
                a_labels.append(elem["teams"][home_team_index]["name"])
                away_score_history["home"].append(temp_home_score_history)
                away_score_history["away"].append(temp_opp_score_history)
                a_dates_array.append((datetime.strptime(elem["matchDate"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'))

            if(len(scores_array) > 1):
                std_dev = statistics.stdev(scores_array)
                mean = statistics.mean(scores_array)
                # Confidence Ratings
                # 95% - 1.960
                # 98% - 2.326
                # 99% - 2.576
                confidence_interval = (1.960 * (std_dev / math.sqrt(len(scores_array))))

            h2h_game_object = {
                "date": (datetime.strptime(game["matchDate"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'),
                "home_player": game["teams"][0]["name"],
                "away_player": game["teams"][1]["name"],
                "mean": mean,
                "confidence_interval": confidence_interval,
                "h2h_datasets": {
                    "scores_dataset" : [
                        {
                            "label": game["teams"][0]["name"],
                            "data": home_total_scores,
                        },
                        {
                            "label": game["teams"][1]["name"],
                            "data": away_total_scores,
                        }
                    ],
                    "games_dataset": [
                        {
                            "label": game["teams"][0]["name"],
                            "data": home_game_totals,
                        },
                        {
                            "label": game["teams"][1]["name"],
                            "data": away_game_totals,
                        }
                    ],
                    "1st_dataset": [
                        {
                            "label": game["teams"][0]["name"],
                            "data": h2h_home_1st_scores,
                        },
                        {
                            "label": game["teams"][1]["name"],
                            "data": h2h_away_1st_scores,
                        }
                    ],
                    "1st_and_2nd_sets": h2h_1_and_2_sets,
                    "2nd_and_3rd_sets": h2h_2_and_3_sets,
                    "score_history": h2h_score_history,
                    "dates": h2h_dates_array,
                },
            }

            h_game_object = {
                "date": (datetime.strptime(game["matchDate"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'),
                "home_player": game["teams"][0]["name"],
                "away_player": game["teams"][1]["name"],
                "mean": mean,
                "confidence_interval": confidence_interval,
                "home_datasets": {
                    "scores_dataset" : [
                        {
                            "label": game["teams"][0]["name"],
                            "data": h_home_total_scores,
                        },
                        {
                            "label": h_labels,
                            "data": h_away_total_scores,
                        }
                    ],
                    "games_dataset": [
                        {
                            "label": game["teams"][0]["name"],
                            "data": h_home_game_totals,
                        },
                        {
                            "label": h_labels,
                            "data": h_away_game_totals,
                        }
                    ],
                    "1st_dataset": [
                        {
                            "label": game["teams"][0]["name"],
                            "data": h_home_1st_scores,
                        },
                        {
                            "label": h_labels,
                            "data": h_away_1st_scores,
                        }
                    ],
                    "1st_and_2nd_sets": h_1_and_2_sets,
                    "2nd_and_3rd_sets": h_2_and_3_sets,
                    "score_history": home_score_history,
                    "dates": h_dates_array,
                },
            }

            a_game_object = {
                "date": (datetime.strptime(game["matchDate"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=0)).strftime('%Y-%m-%d %I:%M%p'),
                "home_player": game["teams"][0]["name"],
                "away_player": game["teams"][1]["name"],
                "mean": mean,
                "confidence_interval": confidence_interval,
                "away_datasets": {
                    "scores_dataset" : [
                        {
                            "label": a_labels,
                            "data": a_home_total_scores,
                        },
                        {
                            "label": game["teams"][1]["name"],
                            "data": a_away_total_scores,
                        }
                    ],
                    "games_dataset": [
                        {
                            "label": a_labels,
                            "data": a_home_game_totals,
                        },
                        {
                            "label": game["teams"][1]["name"],
                            "data": a_away_game_totals,
                        }
                    ],
                    "1st_dataset": [
                        {
                            "label": a_labels,
                            "data": a_home_1st_scores,
                        },
                        {
                            "label": game["teams"][1]["name"],
                            "data": a_away_1st_scores,
                        }
                    ],
                    "1st_and_2nd_sets": a_1_and_2_sets,
                    "2nd_and_3rd_sets": a_2_and_3_sets,
                    "score_history": away_score_history,
                    "dates": a_dates_array,
                }
            }

            h2h_plays_array.append(h2h_game_object)
            h_plays_array.append(h_game_object)
            a_plays_array.append(a_game_object)

            print(f"Match has been added to the array")

        write_json = json.dumps(h2h_plays_array, indent=4)
        with open("data/all_h2h_plays.json", "w") as outfile:
            outfile.write(write_json)
        print("Data has been written to all_h2h_plays.json")

        write_json = json.dumps(h_plays_array, indent=4)
        with open("data/all_home_plays.json", "w") as outfile:
            outfile.write(write_json)
        print("Data has been written to all_home_plays.json")
            
        write_json = json.dumps(a_plays_array, indent=4)
        with open("data/all_away_plays.json", "w") as outfile:
            outfile.write(write_json)
        print("Data has been written to all_away_plays.json")

    except NameError as e:
        print("Visualization Data Script Error: ", e)
        


if __name__ == "__main__":
    # Get the function argument from the command line
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else "World"

        if function_name == "run_script":
            run_script()
        else:
            print(f"Function '{function_name}' not found.")
    else:
        print("No function name provided.")

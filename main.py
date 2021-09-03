import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def auth(username, password):
    url = "https://cognito-idp.us-east-1.amazonaws.com/"
    payload = {
        "AuthFlow": "USER_PASSWORD_AUTH",
        "ClientId": "435acrsnab24sb7si8fe0ccnb4",
        "ClientMetadata": {},
        "AuthParameters": {
            "USERNAME": f"{username}",
            "PASSWORD": f"{password}",
        },
    }

    headers = {
        "origin": "https://app.movespring.com",
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/92.0.4515.159 Safari/537.36",
        "x-amz-target": "AWSCognitoIdentityProviderService.InitiateAuth",
        "x-amz-user-agent": "aws-amplify/0.1.x js",
        "content-type": "application/x-amz-json-1.1",
    }
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    r_json = r.json()
    try:
        auth_token = r_json["AuthenticationResult"]["AccessToken"]
        return auth_token
    except Exception as e:
        print(
            f"""req error: {r_json}
            excetpion: {e}"""
        )


def get_stats(token):
    headers = {
        "accept": "*/*",
        "apollographql-client-name": "web:app",
        "apollographql-client-version": "360",
        "app-state": "foreground",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": "https://app.movespring.com",
        "platform": "web",
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "version": "360",
    }
    payload = [
        {
            "operationName": None,
            "variables": {
                "groupModuleId": 72754,
                "startIndex": 0,
                "stopIndex": 99,
                "sort": {"field": "stepsTotal", "order": "desc"},
            },
            "query": "query ($groupModuleId: Int!, $sort: Sorter, $startIndex: Int, $stopIndex: Int, \
                $cacheTimestamp: String) {\n  boom(id: $groupModuleId, cacheTimestamp: $cacheTimestamp) \
                {\n    id\n    metric\n    leaderboard {\n      currentUserSummary: summary \
                {\n        ...LeaderboardFullSummaryFields\n        __typename\n      }\n      \
                pagedSummaries(sort: $sort, startIndex: $startIndex, stopIndex: $stopIndex) \
                {\n        pageInfo {\n          lastIndex\n          rowCount\n          __typename\n        }\n        \
                summaries {\n          ...LeaderboardFullSummaryFields\n          __typename\n        }\n        \
                __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\n\
                fragment LeaderboardFullSummaryFields on LeaderboardSummary {\n  id\n  distanceAverage\n  \
                distanceTotal\n  minutesAverage\n  minutesTotal\n  rank\n  stepsAverage\n  stepsTotal\n  \
                member {\n    id\n    avatar\n    unitType\n    username\n    __typename\n  }\n  __typename\n}\n",
        }
    ]

    r = requests.post(
        "https://app.movespring.com/graphql", headers=headers, data=json.dumps(payload)
    )

    return r.json()


def stats_parser(data):
    for i in data[0]["data"]["boom"]["leaderboard"]["pagedSummaries"]["summaries"]:
        member_id = i["member"]["id"]
        username = i["member"]["username"]
        avatar = i["member"]["avatar"]
        unit_type = i["member"]["unitType"]
        leaderboard_id = i["id"]
        distance_average = i["distanceAverage"]
        distance_total = i["distanceTotal"]
        minutes_average = i["minutesAverage"]
        minutes_otal = i["minutesTotal"]
        rank = i["rank"]
        steps_average = i["stepsAverage"]
        steps_total = i["stepsTotal"]

        print(
            f"""
            {member_id}
            {username}
            {unit_type}
            {avatar}
            {leaderboard_id}
            {distance_average}
            {distance_total}
            {minutes_average}
            {minutes_otal}
            {rank}
            {steps_average}
            {steps_total}
            """
        )


auth_token = auth(os.getenv("m_username"), os.getenv("m_password"))
stats = get_stats(auth_token)
stats_parser(stats)

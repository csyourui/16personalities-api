import json
import requests
from data import PAY_LOAD_EN, PAY_LOAD_CN, TEST_PAYLOAD

URL = "https://www.16personalities.com/test-results"
SESSION_URL = "https://www.16personalities.com/api/session"
ANSWERS = [-3, -2, -1, 0, 1, 2, 3]

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "origin": "https://www.16personalities.com",
    "referer": "https://www.16personalities.com/free-personality-test",
    "sec-ch-ua": "'Google Chrome';v='125', 'Chromium';v='125', 'Not.A/Brand';v='24'",
    "sec-ch-ua-platform": "macOS",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}


def build_payload(answers):
    assert len(answers) == len(PAY_LOAD_EN["questions"])
    payload = PAY_LOAD_CN
    for index, A in enumerate(answers):
        payload["questions"][index]["answer"] = ANSWERS[A]


def get_result(payload, local_session="session.json"):
    session = requests.session()
    session.post(URL, data=json.dumps(payload), headers=HEADERS)
    sess_r = session.get(SESSION_URL)
    res_json = sess_r.json()
    if local_session:
        json.dump(res_json, open(local_session, "w"), indent=4)
    analysis_result(res_json=res_json)


def analysis_result(res_json):
    print("Scores:")
    print(res_json["user"]["scores"])
    print("------" * 3)
    print("Traits:")
    identity = res_json["user"]["traits"]["identity"]
    for key in res_json["user"]["traits"]:
        value = res_json["user"]["traits"][key]
        print(f"{key.upper()}: {value}")
    print("------" * 3)
    personality = res_json["user"]["personality"]
    print(f"Personality: {personality}-{identity[0]}")


if __name__ == "__main__":
    get_result(TEST_PAYLOAD)

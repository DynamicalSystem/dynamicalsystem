from dynamicalsystem.halogen.config import config_instance
from dynamicalsystem.halogen.utils import url_join
from dynamicalsystem.halogen import logger
from requests import get, post


class Notion:
    def __init__(self, chart, placing):
        self.config = config_instance(__name__)
        self.logger = logger
        self.chart = chart
        self.placing = placing
        self.headers = {
            "Authorization": f"Bearer {self.config.token}",
            "Content-Type": "application/json",
            "Notion-Version": self.config.version,
        }

        url = url_join(
            self.config.url, ["v1/databases", self.config.placings_id, "query"]
        )
        filter = {
            "filter": {
                "and": [
                    {"property": "Place", "title": {"equals": str(self.placing)}},
                    {
                        "property": "Charts",
                        "relation": {"contains": self._notion_chart_id()},
                    },
                ]
            }
        }

        response = post(url, headers=self.headers, json=filter)

        try:
            review_id = response.json()["results"][0]["properties"]["Reviews"][
                "relation"
            ][0]["id"]
        except IndexError as e:
            message = f"No review found for placing {placing} in chart {chart}."
            raise ValueError(message) from e

        url = url_join(self.config.url, ["v1/pages", review_id])
        response = get(url, headers=self.headers)
        self.content = response.json()

    _judgement = {
        "https://www.notion.so/icons/volume-off_lightgray.svg": "Ignore.",
        "https://www.notion.so/icons/repeat_lightgray.svg": "Buy.",
        "https://www.notion.so/icons/skateboard_lightgray.svg": "Explore.",
    }

    def _notion_chart_id(self):
        url = url_join(
            self.config.url, ["v1/databases", self.config.charts_id, "query"]
        )
        filter = {
            "filter": {"property": "Short Name", "title": {"contains": self.chart}}
        }
        response = post(url, headers=self.headers, json=filter)

        return response.json()["results"][0]["id"]

    def validate_content(self):
        try:
            d = {}
            d["artist"] = self.content["properties"]["Artist"]["rich_text"][0]["text"][
                "content"
            ]
            d["work"] = self.content["properties"]["Work"]["rich_text"][0]["text"][
                "content"
            ]
            d["review"] = self.content["properties"]["Review"]["rich_text"][0]["text"][
                "content"
            ]
            d["verdict"] = self._judgement[self.content["icon"]["external"]["url"]]

            return d
        except (KeyError, IndexError, TypeError) as e:
            self.logger.warning(str(e) + f" for placing {str(self.placing)} in chart {self.chart}")
            return False

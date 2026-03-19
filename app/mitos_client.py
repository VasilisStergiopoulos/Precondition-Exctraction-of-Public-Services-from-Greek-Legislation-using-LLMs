import requests
import pandas as pd
from pathlib import Path
from typing import List
from .config import MITOS_API_BASE, REQUEST_TIMEOUT
from .models import ProcessRule, ProcessCondition, ServiceData


class MitosClient:
    def __init__(self, timeout: int = REQUEST_TIMEOUT):
        self.timeout = timeout
        self.session = requests.Session()

    def get_process_ids(self, csv_path: Path) -> List[str]:
        df = pd.read_csv(csv_path)
        return df["process_id"].dropna().astype(str).unique().tolist()

    def fetch_service(self, process_id: str) -> ServiceData:
        url = f"{MITOS_API_BASE}/{process_id}"
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()

        payload = response.json()
        metadata = payload.get("data", {}).get("metadata", {})

        rules = []
        for item in metadata.get("process_rules", []):
            rule_url = item.get("rule_url")
            if not rule_url:
                continue
            if rule_url.startswith("https://https://eur-lex.europa"):
                continue
            rules.append(ProcessRule(rule_url=rule_url))

        conditions = []
        for item in metadata.get("process_conditions", []):
            name = item.get("conditions_name")
            if name:
                conditions.append(ProcessCondition(condition_name=name))

        return ServiceData(
            process_id=process_id,
            rules=rules,
            conditions=conditions,
        )

    def download_file(self, url: str, destination: Path) -> bool:
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(response.content)
            return True
        except requests.RequestException as e:
            print(f"Download failed for {url}: {e}")
            return False
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import argparse
import time
import pandas as pd
from subprocess import run
import subprocess


def load_telemetry_peers():
    peers = {}
    with webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=webdriver.ChromeOptions()) as driver:
        # Set window to something big, so at least 1000 nodes loads
        driver.set_window_size(400, 100000)

        print("Loading telemetry page")
        driver.get(
            "https://telemetry.polkadot.io/#list/0x05d5279c52c484cc80396535a316add7d47b1c5b9e0398dd1f584149341460c5")
        # Wait for page to load
        time.sleep(1)

        print("Updating settings to show peer id")
        # Open settings
        driver.find_element(By.CSS_SELECTOR, 'div[title="Settings"]').click()

        # Turn on `Network ID` and `Finalized Block` settings
        settings = driver.find_elements(
            By.CSS_SELECTOR, 'div[class="Setting"]')
        for setting in settings:
            if setting.text == "Network ID":
                setting.find_element(
                    By.CSS_SELECTOR, 'span[class="Setting-switch"]').click()
            if setting.text == "Finalized Block":
                setting.find_element(
                    By.CSS_SELECTOR, 'span[class="Setting-switch"]').click()
        # Wait for page to load
        time.sleep(1)

        # Go back to node list
        driver.find_element(By.CSS_SELECTOR, 'div[title="List"]').click()

        print("Downloading list of peers")
        table = pd.read_html(driver.page_source)[0]
        print(f"Found {table.shape[0]-1} peers")
        for index, row in table.iterrows():
            if index > 0:
                peers[row["Network ID"][:52]] = row["Finalized Block"]
    return peers


def verify_signature(verifier_path, row, peers):
    peer_id = row.peer_id
    public_key = row.public_key
    signature = row.signed_message

    res = run([
        f"{verifier_path}",
        "verify-signature",
        "--peer-id",
        f"{peer_id}",
        "--message",
        f"{peer_id}",
        "--public-key",
        f"{public_key}",
        "--signature",
        f"{signature}"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if res.returncode != 0:
        return 1
    if peer_id in peers:
        return 0
    else:
        return 2


def result_name(res):
    if res == 0:
        return "ok"
    elif res == 1:
        return "wrong signature"
    elif res == 2:
        return "not in telemetry"
    else:
        return "unknown"


parser = argparse.ArgumentParser()
parser.add_argument("--verifier", type=Path)
parser.add_argument("--validators-in", type=Path)
parser.add_argument("--validators-out", type=Path)


p = parser.parse_args()
peers = load_telemetry_peers()

validators = pd.read_csv(p.validators_in)
validators = validators.assign(
    result=[verify_signature(p.verifier, row, peers) for _, row in validators.iterrows()])
validators = validators.assign(
    result_name=[result_name(row.result) for _, row in validators.iterrows()])
print(f"Writing results to {p.validators_out}")
validators.to_csv(p.validators_out, index=False)

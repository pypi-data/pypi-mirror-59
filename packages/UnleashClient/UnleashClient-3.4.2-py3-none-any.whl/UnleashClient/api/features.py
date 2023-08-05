import requests
from UnleashClient.constants import REQUEST_TIMEOUT, FEATURES_URL
from UnleashClient.utils import LOGGER


# pylint: disable=broad-except
def get_feature_toggles(url: str,
                        app_name: str,
                        instance_id: str,
                        custom_headers: dict,
                        custom_options: dict) -> dict:
    """
    Retrieves feature flags from unleash central server.

    Notes:
    * If unsuccessful (i.e. not HTTP status code 200), exception will be caught and logged.
      This is to allow "safe" error handling if unleash server goes down.

    :param url:
    :param app_name:
    :param instance_id:
    :param custom_headers:
    :param custom_options:
    :return: Feature flags if successful, empty dict if not.
    """
    try:
        LOGGER.info("Getting feature flag.")

        headers = {
            "UNLEASH-APPNAME": app_name,
            "UNLEASH-INSTANCEID": instance_id
        }

        resp = requests.get(url + FEATURES_URL,
                            headers={**custom_headers, **headers},
                            timeout=REQUEST_TIMEOUT, **custom_options)

        if resp.status_code != 200:
            LOGGER.warning("unleash feature fetch failed!")
            raise Exception("unleash feature fetch failed!")

        return resp.json()
    except Exception:
        LOGGER.exception("Unleash feature fetch failed!")

    return {}

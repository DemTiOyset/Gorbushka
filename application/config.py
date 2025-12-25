import os

from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("API_KEY")
        self.campaignId = int(os.getenv("CAMPAIGN_ID"))
        self.businessId = int(os.getenv("BUSINESS_ID"))
#
# class ApiClient:
#     headers = {
#         "Api-Key": "заглушка",
#         "Content-Type": "application/json"
#     }
#
#     ORDER_URL = "https://api.partner.market.yandex.ru/v1/businesses/{businessId}/orders"

settings = Settings()
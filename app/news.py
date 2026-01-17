from datetime import date

MOCK_NEWS = [
    {
        "category": "macro",
        "headline": "Investors weigh inflation data and interest-rate expectations ahead of central bank commentary.",
        "source": "MockWire",
    },
    {
        "category": "rates",
        "headline": "Bond yields move as traders reassess the pace of potential rate cuts this year.",
        "source": "MockWire",
    },
    {
        "category": "earnings",
        "headline": "Several large companies report quarterly results; guidance updates drive sector rotation.",
        "source": "MockWire",
    },
    {
        "category": "global",
        "headline": "Global markets react to currency moves and fresh geopolitical headlines overnight.",
        "source": "MockWire",
    },
]

def get_todays_items():
    # In a real integration, this would call GDELT/AlphaVantage/NewsAPI.
    return {
        "as_of": str(date.today()),
        "items": MOCK_NEWS,
    }

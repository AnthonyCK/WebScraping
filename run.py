import pandas as pd

import fetch
import parse
import constants

# Run the fetch and parse scripts
if __name__ == '__main__':
    log = []
    fetch.fetch_data("computers", "laptops", log)
    fetch.fetch_data("computers", "tablets", log)
    fetch.fetch_data("phones", "touch", log)
    pd.DataFrame(log).to_csv(constants.LOG_CSV, index=False)
    parse.parse_data()
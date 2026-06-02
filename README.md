# detide

de-tiding best practice of water level time series.

--- 

Created as part of the [surgeMIP](https://www.sciencedirect.com/science/article/pii/S2212094724000501) (_Storm surges and extreme sea levels: Review, establishment of model intercomparison and coordination of surge climate projection efforts_)

## Quick start

```python
import pandas as pd
from scripts.harmonic import pytides_surge
from scripts.constituents import FULL

df = pd.read_parquet("tests/data/cuxh.parquet")
surge = pytides_surge(df["elev"], constituents=FULL)
```

## Docs

Methodology, API reference, and open questions: 
**[tomsail.github.io/detide](https://tomsail.github.io/detide/)**

## Contributing

Issues and PRs welcome - especially discussion on constituent sets, metadata fields, and validation approaches.
# detide

Best practice for de-tiding water level time series.

--- 

Created as part of the [SurgeMIP](https://www.sciencedirect.com/science/article/pii/S2212094724000501) (_Storm surges and extreme sea levels: Review, establishment of model intercomparison and coordination of surge climate projection efforts_)

## Quick start

```python
import pandas as pd
from detide.harmonic import pytides_surge
from detide.constituents import FULL

df = pd.read_parquet("tests/data/cuxh.parquet")
surge = pytides_surge(df["elev"], constituents=FULL)
```

## Docs

Methodology, API reference, and open questions: 
**[oceanmodeling.github.io/detide](https://oceanmodeling.github.io/detide/)**

## Contributing

Issues and PRs welcome - especially discussion on constituent sets, metadata fields, and validation approaches.

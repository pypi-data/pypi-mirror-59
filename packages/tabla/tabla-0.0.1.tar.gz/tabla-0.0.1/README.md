# tabla

Generate LaTeX tables in Python from your data in a `pandas.DataFrame`.

## Example

All you need is a dataframe you'd like to create a table for, and a list of
`TableColumn`s for each column in the dataframe you would like to include in
your table.

```python
import pandas as pd
from tabla import TableColumn, Table

columns = [
    TableColumn("date", "", "%Y-%m-%d", "Date"),
    TableColumn("temp", "(degrees)", "{:0.2}", "Temperature"),
    TableColumn("rate", r"(m day\textsuperscript{-1})", "{:04.3}", "Rate"),
]


dates = pd.date_range("2020-01-01", "2020-01-02", freq="6H")
data = list()
for date in dates:
    d = {"date":date}
    d.update({c: pd.np.random.random() for c in ["temp", "rate"]})
    data.append(d)

df = pd.DataFrame(data)

table = Table("test_name", columns, dataframe, header_units=True)

# Generate as a string
latex_str = table.dumps()
```

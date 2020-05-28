import pandas as pd
import numpy as np
df = pd.DataFrame({"A": ["foo", "foo", "foo", "foo", "foo",
                         "bar", "bar", "bar", "bar"],
                   "B": ["one", "one", "one", "two", "two",
                         "one", "one", "two", "two"],
                   "C": ["small", "large", "large", "small",
                         "small", "large", "small", "small",
                         "large"],
                   "D": [1, 2, 2, 3, 3, 4, 5, 6, 7],
                   "E": [2, 4, 5, 5, 6, 6, 8, 9, 9]})
print(df)


table = pd.pivot_table(df, values='D', index=['A'],
                    columns=['C'], aggfunc=lambda x: x.sum(min_count=1), margins_name='Tổng',margins = True
                    )
print(table)
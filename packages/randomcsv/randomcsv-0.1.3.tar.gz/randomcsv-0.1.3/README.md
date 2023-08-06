# RandomCSV

This library let's you generate CSV files with a specific structure, but 
random data. These CSVs can be used as test data when developing data pipelines.

## Usage
```python
from randomcsv import *


generator = CsvGenerator()

# adds a column filled with integers, starting at 100, incrementing
generator.add_column(IntColumn("Integers", start=100))  

# adds a column filled with strings, currently first names from the firstNames.txt dictionary
generator.add_column(StringColumn("Names"))

# add a column filled with random float values between 10 and 20 rounded to 2 digits.
generator.add_column(RandomNumberColumn("Random", low=10, high=20, digits=2))

# adds a column, values are randomly picked from the provided list
generator.add_column(CategoryColumn("Categories", [1, 2, 3, 4]))

# adds a column with name "Calculated", based on Columns Integers and Class
# the arguments of the given function must match order and type of the values of the columns
generator.calculate_column("Calculated", ["Integers", "Categories"],
                           lambda number, category: f'{number} {category}')

# creates pandas DataFrame with 5 rows
data_frame = generator.generate_data_frame(5) 
# creates CSV file in directory "output"
generator.create_csv(5, "test.csv")
```

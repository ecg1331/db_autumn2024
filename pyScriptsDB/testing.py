import pandas as pd

books = pd.read_csv('tables/books.csv')

most_recent = books['publication_date'].max()
oldest = books['publication_date'].min()
print(most_recent)
print(oldest)

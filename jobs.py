import pandas as pd

df = pd.read_csv("ai4i2020.csv")

print("First 5 Rows")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

df = df.drop_duplicates()

df.columns = df.columns.str.strip()

print("\nData Types")
print(df.dtypes)

df["Type"] = df["Type"].map({
    "L": 0,
    "M": 1,
    "H": 2
})

print("\nAfter Transformation")
print(df.head())

print("\nUpdated Data Types")
print(df.dtypes)

df.to_csv("cleaned_ai4i2020.csv", index=False)

print("\nCleaned Dataset Saved Successfully")
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Read the Excel file
df = pd.read_excel('MucNuoc-2021.xlsx', sheet_name='Sheet1', nrows=8760)

# Extract the relevant columns
x = df[['st_quy_chau']]  # Independent variable (feature)
y = df['rain_quy_chau']     # Dependent variable (target)

# Create and fit the linear regression model
model = LinearRegression()
model.fit(x, y)

# Make predictions
y_pred = model.predict(x)

# Calculate R-squared
r2 = r2_score(y, y_pred)

# Get the coefficients
intercept = model.intercept_
coef = model.coef_[0]

# Print the results
print(f"Linear Regression Formula: rain = {coef:.6f} * level + {intercept:.6f}")
print(f"R-squared (Accuracy): {r2:.6f}")

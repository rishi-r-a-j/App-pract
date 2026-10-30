import pandas as pd
import matplotlib.pyplot as plt

# Read employee data from CSV file
df = pd.read_csv("employee.csv")

# Display employee names, departments, and salaries
print("Employee Details:")
print(df[["Name", "Department", "Salary"]])

# Calculate average salary for each department
avg = df.groupby("Department")["Salary"].mean()
print("\nAverage Salary by Department:")
print(avg)

# Identify the employee receiving the highest salary
highest = df.loc[df["Salary"].idxmax()]
print("\nEmployee Receiving the Highest Salary:")
print(highest)

# Bar chart comparing average salaries across departments
avg.plot(kind="bar")
plt.title("Average Salary by Department")
plt.xlabel("Department")
plt.ylabel("Average Salary")
plt.tight_layout()
plt.show()

# Histogram showing the distribution of employee salaries
plt.hist(df["Salary"], bins=5, edgecolor="black")
plt.title("Employee Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Al.csv')
plt.errorbar(data['Active Layer Cost Fraction (%)'],data['Average Thickness (m)'],yerr=data['Standard Error'],fmt='o')
plt.ylabel('Average Al Thickness (m)')
plt.xlabel('Active Layer Cost Fraction (%)')
plt.show()
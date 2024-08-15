import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("medical_examination.csv")

bmi = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = bmi > 25
df['overweight'] = df['overweight'].astype(int)

df['gluc'] = (df['gluc'] != 1).astype('uint8')
df['cholesterol'] = (df['cholesterol'] != 1).astype('uint8')

df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
df_cat = df_cat.reset_index().groupby(['variable', 'cardio', 'value']).count().rename(columns={'index': 'total'}).reset_index()
fig = sns.catplot(df_cat, x='variable', y='total', kind='bar', hue='value', col='cardio')
fig.savefig('catplot.png')

condition3 = df['height'] >= df['height'].quantile(0.025)
condition4 = df['height'] <= df['height'].quantile(0.975)
condition5 = df['weight'] >= df['weight'].quantile(0.025)
condition6 = df['weight'] <= df['weight'].quantile(0.975)
condition7 = df['ap_lo'] <= df['ap_hi']

heat_df = df.loc[condition3 & condition4 & condition5 & condition6 & condition7]
corr = heat_df.corr()
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True

fig = plt.figure(figsize=(12, 6))
sns.heatmap(corr, annot=True, fmt='.1f', center=0, vmin=-0.5, vmax=0.5)
fig.savefig('heatmap.png')

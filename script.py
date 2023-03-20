from orkg import ORKG
from math import ceil
from statannot import add_stat_annotation
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('data.csv')

fig, ax = plt.subplots(figsize=(6, 5))
ax, res = add_stat_annotation(sns.boxplot(data=df, x='Season', y='Event Duration [min]'), 
                              data=df, x='Season', y='Event Duration [min]',
                              box_pairs=[('Summer', 'Winter')],
                              test='t-test_ind', text_format='simple', loc='inside', verbose=2)
pvalue = res[0].pval

orkg = ORKG(host='https://sandbox.orkg.org')
orkg.templates.materialize_template('R12002')
tp = orkg.templates

tp.students_ttest('Statistical hypothesis test', 
  has_dependent_variable=tp.study_design_dependent_variable('Event duration',
    # atmospheric aerosolised particle formation event
    has_object_of_interest='http://purl.obolibrary.org/obo/ENVO_01001359',
    # duration
    has_property='http://purl.obolibrary.org/obo/PATO_0001309', 
  ), 
  has_specified_input=(df, 'Monthly mean event duration'),
  has_specified_output=tp.pvalue('Output p-value (p < {})'.format(ceil(pvalue*1000)/1000.0), 
    tp.scalar_value_specification('{}'.format(pvalue), pvalue)
  ),
).serialize_to_file('article.contribution.1.json', format='json-ld')

fig.savefig('figure.png')

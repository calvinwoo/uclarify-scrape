import pandas as pd
import numpy as np
from statsmodels.formula.api import ols

movies = pd.read_csv('http://www.rossmanchance.com/iscam2/data/movies03RT.txt', sep='\t', names=['X', 'score', 'rating', 'genre', 'box_office', 'running_time'], skiprows=1)

#r = pd.Categorical.from_array(movies['rating'])

lm1 = ols('box_office ~ genre + rating', movies).fit()
test = [1, 1]

print lm1.summary();
#print lm1.bse['genre[T.action/adventure]']


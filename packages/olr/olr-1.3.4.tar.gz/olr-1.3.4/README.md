The olr function runs all the possible combinations of linear regressions with all of the
dependent variables against the independent variable and returns the statistical summary
of either the greatest adjusted R-squared or R-squared term. R-squared increases 
with the addition of an explanatory variable whether it is 'significant' or not, thus this was developed to eliminate that conundrum. 
Adjusted R-squared is preferred to overcome this phenomenon, but each combination will still produce different results and this will
return the best one.


dataset = pd.read_csv('C:\Rstuff\olr\inst\extdata\oildata.csv') <br />
responseName = dataset[['OilPrices']] <br />
predictorNames = dataset[['SP500', 'RigCount', 'API', 'Field_Production', 'RefinerNetInput', 'OperableCapacity', 'Imports', 'StocksExcludingSPR']] <br />

The TRUE or FALSE in the olr function, specifies either the adjusted R-squared or the R-squared regression summary, respectfully.

When responseName and predictorNames are None (NULL), then the first column in the dataset is set as the responseName and the remaining columns are the predictorNames.

Adjusted R-squared <br />
olr(datasetname, resvarname = None, expvarnames = None, adjr2 = "True")

R-squared <br />
olr(datasetname, resvarname = None, expvarnames = None, adjr2 = "False")

list of summaries <br />
olrmodels(datasetname, resvarname = None, expvarnames = None)

list of formulas <br />
olrformulas(datasetname, resvarname = None, expvarnames = None)

list of forumlas with the dependant variables in ascending order <br />
olrformulasorder(datasetname, resvarname = None, expvarnames = None)

the list of adjusted R-squared terms <br />
adjr2list(datasetname, resvarname = None, expvarnames = None)

the list of R-squared terms <br />
r2list(datasetname, resvarname = None, expvarnames = None)

An R version of this package olr is available on CRAN.
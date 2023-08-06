This readme file is going to define some dependencies of this library before using it
First this library implements the topsis approach and have some constraints for using it which are defined below:
The data need to be provided in the numerical format no linguistic expression should be used in the data
The main topsis function should be provided with the 3 parameters which are described as below
Weights :- The integer valued one dimenshion numpy array which tells the weightage of each feature
Numerical_data :- 2D float numpy array having none of the feature values as linguistic values
impact :- 1D string numpy array consisting of 2 values as "+" and "-" where "+" shows that, that particular feature value should be maximum and "-" corresponds to minimizing it's values.
Result :- Now this function is going to return the index(starting from 1) of the model selected by the topsis approach in the numerical_data numpy array provided.
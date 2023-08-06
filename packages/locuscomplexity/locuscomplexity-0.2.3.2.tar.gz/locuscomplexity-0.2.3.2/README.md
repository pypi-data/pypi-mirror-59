# Economic Complexity

This package is the implementation of the Economic Complexity and Fitness

See https://locusanalytics.github.io/EconCmplx/ for full documentation.

## Getting Started

### Installation

The package can be downloaded and installed using pip.

```
pip install locuscomplexity
```
You will then be able to import the package in your Python scripts.

```
import locuscomplexity as lc
```
You can also import specific parts of the package.
```
import locuscomplexity.complexity as lcmplx
import locuscomplexity.fitness as lfit
```


### Prerequisites

This package is coded in Python 3.
Using pip install, all Python libraries required to use it should be automatically installed on your machine.

## How to use the Locus Economic Complexity package

### Input data

The input data needs to follow a specific format. the module requires a Dataframe that contains two dimensions. For example, the first dimension can be the area codes, such as County Fips codes, the second can be 4x6 Locus Functions or Functional markers for which we know the employment level for a year.
The following table could be an input if we want to compute the complexity of counties based on the distribution of employment by 4x6 Locus Functions.

| Fips codes |  1 A |  2 A | 3 A | ... |  4 E | 4 F |
|:----------:|:----:|:----:|:---:|:---:|:----:|:---:|
|    1001    | 1207 |  542 | 788 |     |  456 | 741 |
|    1003    |  456 | 7412 | 845 |     |  369 | 236 |
|            |      |      |     |     |      |     |
|    51857   |  159 | 4563 | 458 |     | 4563 | 257 |

### Using the original OEC algorithm

If we note df our input Dataframe, we can compute the complexity scores of both the counties and the Locus functions directly using the complexity_indices function. The first argument is the input Dataframe, the second is the name of the column that contains the first dimension.

```
area_complexity, functions_complexity = locuscomplexity.complexity.complexity_indices(
            df, 'Fips codes')
```

### Using the Fitness algorithm

Using the fitness algorithm the matrix m needs to be computed separately. We can then compute area fitness scores and functional complexity using the fitness and complexity functions. The arguments are the same as in the previous method.

```
m = locuscomplexity.complexity.build_m(df_data, 'Fips codes')
area_fitness = locuscomplexity.fitness.fitness(m, 'Fips codes')
functions_complexity = locuscomplexity.fitness.complexity(m)
```

### Output

Both methods return the complexity scores for the first and second dimension. We standardized the output for both methods.

The complexity (or fitness) scores for the first dimension are returned in a two column Dataframe.

|   f  | Fips codes |
|:----:|:----------:|
|  2.1 |    1001    |
|  1.5 |    1003    |
|      |            |
| 0.45 |    51857   |

The output for complexity scores on the second dimension has a similar structure.

| index |  q  |
|:-----:|:---:|
|  1 A  | 1.6 |
|  1 B  | 3.4 |
|       |     |
|  4 F  | 0.7 |


## Documentation

* Please read the [Technical Brief](https://docs.google.com/document/d/1gwdKcbqvOK-uHqWyH0UBY89wR6rAX9-UICtLvss6Sno/edit?usp=sharing) for details on the project.

## Authors

* **[Vinharng Chew](mailto:vchew@locus.co)**
* **[Olivia Dalglish](mailto:odalglish@locus.co)**
* **[Emeline Floc'h](mailto:efloch@locus.co)**
* **[Aaron Lee](mailto:alee@locus.co)**

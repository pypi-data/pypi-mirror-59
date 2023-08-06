# TOPSIS implementation in python 

>Project1 for DATA ANALYSIS AND VISUALISATION(UCS633) 
>Nishchay Mahajan COE18
>Roll number: 101703377

Output is a dataframe with 3 columns
 - **Alternatives** serial number
 - Corresponding performance **Score** or closeness to ideal solution
 - **Rank**

## Installation
`pip install topsis-pypck`

## Upgrade
`pip install topsis-pypck --upgrade`

## To use via command line
`python3 topsis.py file.csv "0.25,0.25,0.25,0.25" "-,+,+,+"`


## To use in python IDLE
```
>>>from topsis_pypck.topsis import topsis
>>> f= "file.csv"
>>> w = [1,1,1,1]
>>> im = ["+" , "+" , "-" , "+" ]
>>>topsis(f,w,im)
```

## Output

```
  Model     Score    Rank
-------  --------  ------
      1  0.534277       3
      2  0.308368       5
      3  0.691632       1
      4  0.534737       2
      5  0.401046       4

```




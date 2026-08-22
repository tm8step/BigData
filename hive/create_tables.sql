-- This is the SQL command used to create the table 'WiscCancerData'.  It lists all data with their data types,

CREATE TABLE WiscCancerData(
`ID Number` INT,
`Diagnosis` STRING,
`Radius Mean` FLOAT,
`Texture Mean` FLOAT,
`Perimeter Mean` FLOAT,
`Area Mean` FLOAT,
`Smoothness Mean` FLOAT,
`Compactness Mean` FLOAT,
`Concavity Mean` FLOAT,
`Concave Points Mean` FLOAT,
`Symmetry Mean` FLOAT,
`Fractal Dimension Mean` FLOAT,
`Radius SE` FLOAT,
`Texture SE` FLOAT,
`Perimeter SE` FLOAT,
`Area SE` FLOAT,
`Smoothness SE` FLOAT,
`Compactness SE` FLOAT,
`Concavity SE` FLOAT,
`Concave Points SE` FLOAT,
`Symmetry SE` FLOAT,
`Fractal Dimension SE` FLOAT,
`Radius Worst` FLOAT,
`Texture Worst` FLOAT,
`Perimeter Worst` FLOAT,
`Area Worst` FLOAT,
`Smoothness Worst` FLOAT,
`Compactness Worst` FLOAT,
`Concavity Worst` FLOAT,
`Concave Points Worst` FLOAT,
`Symmetry Worst` FLOAT,
`Fractal Dimension Worst` FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/data'
tblproperties("skip.header.line.count"="1");

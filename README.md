
# coaches-changes-brazilian-league

Code used to scrape web data on coaches changed on the brazilian football league from wikipedia. See it at [Kaggle](https://www.kaggle.com/datasets/pendulun/coaches-changes-brazilian-football-first-division).

  

## Configs

There is a `src/config.py` file where you can define target paths and target years. The scripts were made to work with years in the range [2008, 2023]. The data comes from the Wikipedia (in portuguese) on the Brazilian Serie A (First Division) League from those years.

  

The final aggregated csv file will be at the path indicated by the following configs in the config file:

- COACHES_FIRED_CSV_TREATED_TABLE_DIR_PATH

- COACHES_FIRED_CSV_TREATED_TABLE_PATH

  

## Steps

The total procedure takes 4 distinct steps to complete:

1. Download the HTMLs from the target wikipedia links with respect to the years indicated (`src/download_coaches_fired_wikis.py`)

2. Extract the HTML tables from the HTML files downloaded in step 1 (`src/extract_coaches_fired_tables.py`)

3. Parse the raw HTML tables from step 2 into CSV files (`src/process_coaches_fired_tables.py`)

4. Treat and aggregate the CSV files from step 3 into one unique CSV file (`src/treat_coaches_fired_tables.py`)

  

## Running

First of all, it's recommended that you create a unique python virtual environment inside the project's root folder. This can be done with:

  

`python -m venv <environment name here>`

  

You can name the virtual environment as `venv` for example. Then, you need to activate the environment:

  

On windows: `call venv/Scripts/activate.bat`

On linux: `source venv/bin/activate`

  

Now, with the environment activated, you have to install the dependencies informed at `requirements.txt`. You can do this via `python pip install -r requirements.txt`. Now you can run the scripts.

  

There are two ways of generating the data:

1. If you have the ability to run a makefile, go to the `src/` directory and run `make all_coaches`. This will run all 4 steps mentioned above

2. You can run each step, in order, manually with python3:

	1.  `python download_coaches_fired_wikis.py`

	2.  `python extract_coaches_fired_tables.py`

	3.  `python process_coaches_fired_tables.py`

	4.  `python treat_coaches_fired_tables.py`

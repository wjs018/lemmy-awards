This repo acts as a place to store the submitted ballots for the year-end awards being run by the [ani.social](https://ani.social/) lemmy instance. There are three different communities hosting award events:

1. [anime@ani.social](https://ani.social/c/anime)
2. [manga@ani.social](https://ani.social/c/manga)
3. [lightnovels@ani.social](https://ani.social/c/lightnovels)

## Requirements

- Python - run on 3.13.0
- `pandas`
- `starvote`

## Structure

I have organized files into folder by year. In each year's folder there are the three `.csv` files with all the survey responses for the three different communities listed above. These files are just slightly modified after being exported from the LimeSurvey instance the surveys were conducted on. The modifications are simply to delete some extraneous/irrelevant columns.

- `anime_responses.csv`
- `manga_responses.csv`
- `ln_responses.csv`

To conduct the elections, simply clone this repo and navigate to the `2024` folder. Then run the `process_votes.py` file. It will conduct all the elections for each category within all three mediums.

There will be a large number of output files. Summarizing them:

- `anime_results.csv`, `manga_results.csv`, `ln_results.csv` - These are simply listing the winners in each category for the three mediums.
- `{medium}_results {award category}.txt` - One of these files is generated for each medium/category and it is a recording of the verbose output of the `starvote` election results. This can be read if you want to see the runner-up for instance.
- `{medium}_results {award category} ballots.csv` - This is a simplified `.csv` file that contains all of the submitted ballots for the medium/category. Each row is a vote and each column signifies a nominee for the category (listed in the header row). The cell contents is the score that the voter gave to that nominee in the category.

I have included all the output files for you in the subfolders of 2024 for your convenience. Please reach out to me if you have any questions.

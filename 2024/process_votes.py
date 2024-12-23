"""Processes the votes using STAR voting."""

import csv
import starvote
import pandas as pd

from collections import defaultdict
from contextlib import redirect_stdout


def parse_header_text(text):
    if "[" in text:
        # This is the category
        category = text.split(" [")[0]

        # Pluck out the nominee from between brackets
        nominee = text.split(" [")[1].split("]")[0]

        # Clean up the text a little bit
        if nominee.startswith(" - "):
            nominee = nominee[3:]
        if nominee.startswith(" &amp; "):
            nominee = nominee[7:]
        nominee = nominee.replace("&amp;", "&")

        return [category, nominee]

    return None


def process_file(infile, outfile):
    """Parses input csv file and saves results to a new csv file."""

    # Initialize some variables to store stuff
    categories = set()
    category_noms = defaultdict(list)
    all_ballots = defaultdict(list)
    winners_dict = {}

    # Open the votes file as was exported from LimeSurvey
    with open(infile, mode="r") as file:
        csv_file = csv.reader(file)

        # Just look at header row first
        header_row = next(csv_file)

        for idx, heading in enumerate(header_row):
            # Build lists of categories and nominees from parsed headers
            if parse_header_text(heading):
                category, nominee = parse_header_text(heading)
                q_idx = idx
                category_noms[category].append([nominee, q_idx])
                categories.add(category)

        # Iterate through the rest of the rows and parse each ballot
        for vote in csv_file:
            # Parse votes on this ballot for a category
            for award in categories:
                # Create list of nominees for this category
                nominees = []
                for nom in category_noms[award]:
                    nominees.append(nom[0])

                # Create empty dict to store ballot scores to for each nominee
                scores = dict.fromkeys(nominees)

                # Parse the score given to each nominee and save it to the dict
                for nom, idx in category_noms[award]:
                    try:
                        scores[nom] = int(vote[idx])
                    except:  # noqa: E722
                        # Blank responses get assigned 0
                        scores[nom] = 0

                # Separate lists of ballots for each category, stored in a dict
                all_ballots[award].append(scores)

    # Need to run a separate election for each category.
    for key in all_ballots:
        # Make filename to save election output to
        logfile = outfile[:-4] + " " + key + ".txt"

        # Some stuff to deal with "/" character in category name
        logfile = rf"{logfile}"
        logfile = logfile.replace(r"/", r"_")

        # Election outputs to stdout, so redirect to a file
        with open(logfile, "w+") as f:
            with redirect_stdout(f):
                ballots = all_ballots[key]
                winners = starvote.election(starvote.star, ballots, verbosity=1)
                winners_dict[key] = winners[0]

    # Make a dataframe to store winners for easy reference
    results_df = pd.DataFrame(columns=["Category", "Winner"])

    # Populate dataframe with winners in each category
    for key in winners_dict:
        temp_df = pd.DataFrame([[key, winners_dict[key]]], columns=results_df.columns)
        results_df = pd.concat([results_df, temp_df])

        # Save the ballots for the category in a csv file for sharing
        ballotfile = outfile[:-4] + " " + key + " ballots.csv"

        # Some stuff to deal with "/" character in category name
        ballotfile = rf"{ballotfile}"
        ballotfile = ballotfile.replace(r"/", r"_")

        # Write the ballots to a csv file
        with open(ballotfile, "w+") as f:
            columns = all_ballots[key][0].keys()
            writer = csv.DictWriter(f, fieldnames=columns)

            writer.writeheader()
            for row in all_ballots[key]:
                writer.writerow(row)

    # Save short list of winners to file
    results_df.to_csv(outfile, index=False)


if __name__ == "__main__":
    anime_files = ["anime_responses.csv", "anime_results.csv"]
    manga_files = ["manga_responses.csv", "manga_results.csv"]
    ln_files = ["ln_responses.csv", "ln_results.csv"]

    # Just run anime elections
    all_files = [anime_files]

    # Just run manga elections
    # all_files = [manga_files]

    # Just run LN elections
    # all_files = [ln_files]

    # Do all three mediums at one time
    # all_files = [anime_files, manga_files, ln_files]

    for medium in all_files:
        process_file(medium[0], medium[1])

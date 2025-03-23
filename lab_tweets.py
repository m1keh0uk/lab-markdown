#!/usr/bin/python3

'''
# Lab: Analyzing Trump Tweets

In this lab, you will analyze all tweets sent by president Trump from 2009-2018.
You will get practice
1. loading datasets stored in JSON files, and
2. creating plots in python.
This lab will also get you started on your Project 2.

The data we will analyze is used to create the following two websites:
1. [An analysis of which types of tweets Trump is likely to send himself, versus which his staffers send.](http://varianceexplained.org/r/trump-tweets/)
2. [A search engine for all of Trump's tweets.](https://www.thetrumparchive.com/)

> **Note:**
> I am using Markdown formatting within this python docstring.
> This is a *very* common practice.
> Markdown (unlike HTML) is designed to be human readable in it's "uncompiled" form.

## Part 0: Setup Project

You will have to upload files to github to submit this lab.
Complete the following steps to setup your project.

1. Create a new github repo through the github interface called `lab-markdown`.

2. Use github desktop to clone that project onto your computer.

3. Copy this `lab_tweets.py` file into your project folder.

## Part 1: Download the Data

The github repo <https://github.com/bpb27/trump_tweet_data_archive> contains an archive of tweets sent by Donald Trump.

1. Download the files `master_*.json.zip`, where * is a year.
    There should be 10 total files (2009-2018).

    > **Note:**
    > This particular archive stops in 2018 because the maintainer moved their codebase to <https://github.com/bpb27/tta-elastic>.
    > The newer archive has data that goes through the current year (and includes messages sent on Truth Social),
    > but it's a bit more complicated to access the data,
    > so we will use this older archive for this assignment.

2. Unzip these files into the project folder you created in Part 0 above.
    You should get a bunch of files that look like `master_*.json`.

## Part 2: Data Analysis

1. Modify this python file so that it:

    1. Opens each json file and loads the file using the json library.
       Each file contains a list of tweets, and if you concatenate each file's tweets
       together you will get a list of all tweets ever sent by Donald Trump.

    2. Prints the total number of tweets.

    3. Counts the number of tweets that contain the following keywords:
       `Obama`, `Trump`, `Mexico`, `Russia`, and `Fake News`.
       It's important to remember that each of these words can appear with many different capitalizations, 
       and your program should count the word no matter how it is capitalized.  
       For example, `OBAMA`, `obama`, and `ObAmA` all need to count as an occurrence of the word `Obama`.

    4. Prints out a count of each of these words.

        > **Hint:**
        > My program gives the following output:
        > ```
        > len(tweets)= 36307
        > counts= {'trump': 13924, 'russia': 412, 'obama': 2712, 'fake news': 333, 'mexico': 199}
        > ```
        > You'll know your program is correct if you get the same numbers.

2. Select at least 3 more interesting words/phrases to count in trump's tweets,
    and modify your program to display those words.

3. Calculate the percentage of tweets that contain each word.  (Both your new words and Trump's original tweets.)

4. Display the results nicely in a markdown table.

    The display must have all words right justified and the percents printed with two 
    significant figures (on both sides of the decimal) as shown in the example output below.

    ```
    | phrase            | percent of tweets |
    | ----------------- | ----------------- |
    |              daca | 00.17             |
    |         fake news | 00.92             |
    |  mainstream media | 00.06             |
    |            mexico | 00.55             |
    |             obama | 07.47             |
    |            russia | 01.13             |
    |             trump | 38.35             |
    |              wall | 00.91             |
    ```

    > HINT:
    > There are many ways to achieve this effect in python,
    > but I recommend using python's f-string syntax.

5. Plot the results in a bar graph.

## Submission

Create a properly formatted markdown file `README.md` that contains:
1. the markdown table created by your program
2. the image created by your program
3. a short description (1 sentence is fine) for your table/image above

Ensure that you have uploaded to your github repo:
1. your modified python file
2. your python image

Upload your github url to sakai.

## Extra Credit

There are two extra credit opportunities for this lab, worth one point each.

1. If you use the latest version of the data (instead of the files in the github repo) you will get +1 point.
    You can find instructions for accessing the data at <https://www.thetrumparchive.com/faq> under the question "Can I have the data?"

2. If you make a plot of other interesting information in this dataset (that doesn't use the 'text' key).
    For example, you could plot: what time of day does Trump tweet most often? or what state does Trump tweet from most often?
'''
import json
import pprint
import matplotlib.pyplot as plt

files = [
    'data/condensed_2009.json',
    'data/condensed_2010.json',
    'data/condensed_2011.json',
    'data/condensed_2012.json',
    'data/condensed_2013.json',
    'data/condensed_2014.json',
    'data/condensed_2015.json',
    'data/condensed_2016.json',
    'data/condensed_2017.json',
    'data/condensed_2018.json'
]

data = []
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        tweets = json.load(f)
        print(f"{file}: {len(tweets)} tweets")
        data += tweets


print(len(data))


# 1. Print total number of tweets
print(f"Total number of tweets: {len(data)}")

word_counts = {
    'Obama':0,
    'Trump':0, 
    'Mexico':0,
    'Russia': 0,
    'Fake News': 0,
    'Love': 0,
    'Thank You': 0,
    'Happy': 0,
}

favorite_counts = []
most_likes = 0
for i, tweet in enumerate(data):
    for word in word_counts:
        try:
            if word.lower() in tweet['text'].lower():
                word_counts[word] += 1
        except KeyError:
            if word.lower() in tweet['full_text'].lower():
                word_counts[word] += 1
    favorite_counts.append(tweet['favorite_count'])
    if tweet['favorite_count'] > most_likes:
        most_likes = tweet['favorite_count']
        fav_tweet = tweet['text']

pprint.pprint(word_counts)


table_lines = []
table_lines.append("| phrase            | percent of tweets |")
table_lines.append("| ----------------- | ----------------- |")

labels = []
percents = []
for word in word_counts:
    labels.append(word)
    count = word_counts[word]
    percent = (count / len(data)) * 100
    percents.append(percent)
    table_lines.append(f"| {word.rjust(17).lower()} | {percent:05.2f}             |")

# Plot bar chart


plt.figure(figsize=(10, 6))
plt.bar(labels, percents)
plt.ylabel("Percent of Tweets (%)")
plt.title("Keyword Frequency in Trump Tweets (2009–2018)")
plt.savefig("plot.png")
plt.close()

plt.figure(figsize=(10, 6))
plt.hist(favorite_counts, bins=50, edgecolor='black')
plt.xlabel("Favorite Count")
plt.ylabel("Number of Tweets")
plt.title("Distribution of Favorite Counts in Trump Tweets (2009–2018)")
plt.xlim(0, 200000)
plt.savefig("favorite_hist.png")
plt.close()



# Write to README.md
with open("README.md", "w") as readme:
    readme.write("## Keyword Frequency in Trump Tweets (2009–2018)\n\n")
    readme.write("The table below shows how frequently each keyword appeared in Trump's tweets from 2009 to 2018.\n\n")
    readme.write("\n".join(table_lines))
    readme.write("\n\n")
    readme.write("![Keyword Bar Graph](plot.png)\n")
    readme.write("\nThe histogram below shows the distribution of how many favorites Trump's tweets received.\n\n")
    readme.write("![Favorite Count Histogram](favorite_hist.png)\n")
    readme.write("\nTrumps most liked tweet:\n")
    readme.write(fav_tweet)

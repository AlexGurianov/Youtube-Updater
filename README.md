# Youtube Updater
Want to keep up with updates on the channels you are not subscribed to? Youtube updater generates for you a web page with all videos from the channels in your list uploaded since the last program run.

### Preparation

To use the program you must first create a txt file in the "channel lists" folder containing a list channel IDs and names under which you want to display them, one channel per line. It should look like this:

UC16niRr50-MSBwiO3YDb3RA BBC News

If channel ID is not visible in the address bar when you got to the channel page, look for it in the page source.

You should name your file this way "\<ListName\>_list.txt". After initial creation you may update the channels in the file as you wish.

You must also create a txt file in the "last retrieved" folder containing the starting date after which you wish to get videos published until the current moment. The format for the date looks looks like this:

2018-05-16T08:39:44Z

You should name your file this way "\<ListName\>_last_retrieved.txt". After the initial creation of this file the date in it will be set automatically with each run of the program to the date of the run, so that each time you will get a list of the videos posted since the last run. You can also set it manually if you wish.

For clarification, an example for "news" list is provided in the folders.

In this way you can create as many channel lists under different names as you like.

### Output

The result of a program run is an HTML document containing links to the new videos as well as a thumbnail, description and other properties. Videos are sorted by duration in a descending order. An item in the output looks like this:

<table border = "1" cellpadding = "5" cellspacing = "5">
<tr><td>
    <p>Channel: <a href="https://www.youtube.com/channel/UC16niRr50-MSBwiO3YDb3RA/videos">BBC News</a></p>
    <p>Title: <strong>Real Madrid fans celebrate Champions League victory - BBC News</strong></p>
    <p>Duration: <strong>01:00</strong>&nbsp;&nbsp;&nbsp;Published on: 2018-05-27</p>
    <img src = https://i.ytimg.com/vi/Q10jqfmR2nU/default.jpg alt = "Thumbnail Image" align="left"/>Thousands of euphoric Real Madrid supporters took to the streets of the Spanish capital to celebrate victory in the Champions League final against Liverpool.
    <p>URL: <a href="https://www.youtube.com/watch?v=Q10jqfmR2nU">https://www.youtube.com/watch?v=Q10jqfmR2nU</a></p>
</td></tr></table>

The document is created in the "generated lists" folder, its name reflects channels list name and date of creation.

### Requirements
This code uses Python 3 and the following libraries:
- requests
- json
- datetime
- sys
- os

### Usage

To run generate the list of new videos in the command line run:

```
python youtube_updater.py <ListName>
```

and after it's done look for the file in "generated lists" folder. The default value for <ListName> is "music", so if you name a list like this, you may omit the argument.

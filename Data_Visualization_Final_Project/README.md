# P6: Data Visualization using Titanic data

## Summary
Create a visualization that shows the demographics or passenger information between those passengers who survived and those who died

The RMS Titanic was a British passenger ship that collided with an iceberg during her maiden voyage from Southampton in England to New York in the United States of America and sank in the Atlantic Ocean on 15 April 1912. There were approximately 2,224 passengers and crew aboard, and of these, more than 1,500 died. This made the Titanic’s sinking one of the deadliest disasters in modern history.

In this visualization, I have focused on the survival rates of the passengers for whom demographic and other info is available, as seen across various factors such as gender and passenger class etc. I have drawn upon insights from one of my earlier Data Analyst nanodegree projects, project P2, which also analyzed survival rates for various categories of passengers of the Titanic. This analysis (linked in the resources section) had already calculated proportions for the various survival categories and I am using them to visualize the data in a more interactive manner.

The final charts are in the index_v2.html file.
## Design

From the available dataset of survivors for whom demographic and other information was available, there were 891 passengers aboard. Of these, only 342 survived.

### Types of Charts & Layout:
I chose to have my charts laid out one below the other and not side-by-side, to prevent horizontal movement of the eye from left to right. I also chose to use primarily bar charts,  stacked/grouped bar charts and scatter charts as the data being represented is mostly categorical (except for the survival rate counts).

### Key Takeaways to be highlighted:

My key takeaways from an analysis of who survived versus who didn’t were:
* Women were more likely than men to survive, and of women, those in the upper classes (1 & 2) were also more likely to survive
* Younger people (children) were the age group with the highest rate of survival
* Passengers who embarked at Cherbourg had a much higher survival rate

I wanted my audience to be able to notice these 3 trends right away.

### Initial Design:

The design and layout that I chose initially was: Charts on survival rates based on
* Port of embarkation: bar chart
* Gender + passenger class: stacked bar chart
* Age groups: scatter/line plot

### Final Design:

Once I got user feedback, I changed my design layout to:
* Gender + passenger class: vertical grouped bar chart
** I used a grouped bar chart to show the delineation between men and women across passenger classes, without the %s going over 100%.
* Age groups: scatter/line plot
** I wanted the higher/lower survival rates to pop out and thought a scatter/trend line combination would show this best.
* Port of embarkation: bar chart
** A simple bar chart would suffice to show how the port of embarkation really made a difference to a passenger’s survival chances.

#### Changes made in final design:
* I replaced proportions with percentages to make the charts more readable.
* I changed the chart type for the gender-class survival breakdown to make it a horizontal grouped bar chart instead of a stacked bar chart.
* I added another chart as the first chart to show passenger counts across passenger class and port of embarkation.
* From the takeaways section of the feedback, the fact that women had higher survival rates was what stood out immediately. I decided to move this chart up.
* I added x and y axis titles, with some resizing needed to display them.
* I added ordering for the x-axis for each chart.
* I added a legend as and when needed (for 2 out of 4 charts)
* I added a summary description and a title for each chart
* I also added in comments for the HTML code


## Feedback

I asked 3 reviewers for feedback on look and feel of the chart, if they had any suggestions to share and their key takeaway from the charts.

### Feedback #1
Looks good. Colors are very muted. A title would have been nice. Also, some axis labels seem to be missing. And over a 100% of people in first class survived? That seems strange. 

Its interesting to see that young women and folks embarking at Cherbourg (France?) had better survival rates. How many passengers were there in total at each port?

### Feedback #2

Some constructive feedback that these charts could use:
* The x axis is not ordered correctly for chart 2.
* Add a legend for each chart - it is good practice..
* The last chart shows that all females in class 1 survived. That does not seem correct - please check.
* Chart 3 is not the right type of chart to show the breakdown - the proportion goes over 1 (100%). Use a different chart.
* Percentages would be better than proportions. Also, adding totals is good to get an idea of passenger count.
* On a similar note, the y-axis should show %s instead of proportions as it is easier to read.
* My takeaway: From chart 3, it looks like women had much better survival rates compared to men (and among women, the richer folks in class 1 had the highest survival rates.) 

### Feedback #3

I really liked the bounce effect and the pleasant color scheme, but I would like some additional context for each chart. Maybe you want to add a blurb of some sort? It looks like children had a good survival rate and so did women. Most men didn’t seem to have stood much of a chance of surviving.

## Resources

* Dimple.js documentation: https://github.com/PMSI-AlignAlytics/dimple/wiki
* Titanic data set from Kaggle: https://www.kaggle.com/c/titanic
* My Udacity project P2 on Titanic data analysis: https://review.udacity.com/#!/reviews/240876. 
The html version is linked in my submission.
* https://github.com/michaelstrobl/Udacity-Project-5

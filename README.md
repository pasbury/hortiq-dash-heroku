

![hortiq-logo-black](assets\hortiq-logo-black.png)



## What is Hortiq?

Hortiq is a new service for growers and retailers in horticultural industry. We aim to provide provide information to help with decisions about assortment, pricing and online marketing.

Please visit our [website](http://www.hortiq.co.uk/) to see what's on offer.  The site is a 'proof of concept': we would really appreciate feedback and suggestions.   So please take a look and share your thoughts via contact.us@hortiq.co.uk.



## How does Hortiq work?

In the current version, Hortiq gathers publicly available horticultural  information from the internet, processes that information in order to make it more useful and provides a 'dashboard' for users to conduct their own analysis.

### Data Sources

##### [Royal Horticultural Society (RHS)](https://www.rhs.org.uk/)

There are two main items of data from the RHS:

1. List of popular plant genera and a classification of those genera into "types", where example types are: bulbs, houseplants and shrubs.  As used by the RHS [here](https://www.rhs.org.uk/plants/popular).
2. List of plants within these popular genera, with associated details such as common name, growth habit, flower colour as displayed by the RHS Plant Finder.  An [example](https://www.rhs.org.uk/Plants/201715/Cornus-kousa-var-chinensis-Wisley-Queen/Details) for a very nice ornamental tree.  For now, only plants with a RHS 'Award of Garden Merit' have been included in Hortiq.

##### [Google Trends](https://trends.google.com/trends/?geo=GB)

Online search interest for the popular plant genera was sourced from Google Trends.   The Google Knowledge Graph contains relevant entries for many of the genera being searched, however a mapping is sometimes required:

| #    | Genus       | Google Knowledge Graph Name | Freebase ID |
| ---- | ----------- | --------------------------- | ----------- |
| 1    | Anemone     | Anemone                     | /m/0k9xk    |
| 2    | Brugmansia  | Angel's trumpets            | /m/041cw6   |
| 3    | Festuca     | Fescues                     | /m/069879   |
| 4    | Waterlilies | Water lilies                | /m/0hqvc    |

##### [Google Shopping](https://www.google.co.uk/shopping)

For each plant included in Hortiq, Google Shopping is searched to find online buying options.  Information such as product description and price are captured.



### Data Processing

##### Online search interest

The Google Trends interface allows up to five search terms to be compared, the results are scaled such that the maximum search interest is 100.  However, we need commensurate search interest for over one hundred popular plant genera.  Therefore the search is automated, and the results collated, so as to ensure that the search interest for all genera can be compared.



##### Online buying options

The online buying options gathered from Google Shopping are joined with the plant reference data from the RHS.  Additional processing of textual product descriptions is used to create product attributes such as product type (e.g. seeds, bulb, potted plant) and pot size (e.g. 9cm, 2L, 3L) and to extract prices.



##### Data cleansing

There is a need to cleanse the data from all the sources.  The majority of the cleaning is to remove 'false positive' matches from the Google Shopping results.  This is still a work in progress.



### User Interface

The Hortiq user interface is a [Dash](https://dash.plotly.com/) app, running on [Heroku](https://www.heroku.com/).


# RapidResearch
#### Video Demo: https://youtu.be/STKHe2lRiOY
#### Description:

RapidResearch is a web-app designed to make life easier for investors without access to large amounts of institutional data.
Even when this data can be obtained it is like opening the floodgates, with an endless torrent of information coming our way.
By making use of a variety of finance API's and an array of endpoints; RapidResearch gathers the most commonly used metrics used
in evaluating companies for a specific ticker and presents it in a concise report.

All the user has to do is punch in the ticker and the program outputs a report on the company. To make things easier for users,
the calculations for the more complicated figures are included in popovers, simply click on any of them to find out more about the
calculations used and market averages/target ranges. I acknowledge there may be certain biases evident as despite most conventionally
used metrics being included, there are certain figures that I am accustomed to which led to their inclusion.

The following files are included as part of the project:

1. Static Folder containing CSS styles used across the project, apart from common fonts and background image styling, there are also
styles used to section off different parts of the HTML documents for better information presentation.

2. Templates folder containing the templates for the 4 pages in the site as well as a layout template.
    - index.html - the landing page HTML this contains the latest information on markets including most actives, biggest gainers, biggest losers and sector changes.
    - info.html - this provides an overview of the project and the features that I would have liked to include but am unable to for the time being due to resource and time constraints.
    - reports.html - this is a simple page where users simply type in a ticker they would like a report generated for and click submit to post
    - reports2.html - When the user posts a ticker, a report is generated on this page containing key metrics about the company, from ROE and ROA to Gross Profit Margin.
                      There is also a graph charting the stock price movement over the last 600 trading days as well as latest news on the company. The metrics used
                      may be unfamiliar to some, so when clicked on, a popover appears explaining the metric as well as detailing market averages or benchmarks.

3. apiinfo.py
    - This python file contains several functions that calls the API to retrieve various pieces of data in JSON format from different endpoints.

4. application.py
    - This python file calls the functions in apiinfo.py as the user interacts with the website in order to clean the data, isolate relevant figures, perform
      calculations and plotting before rendering subsequent HTML pages containing this information.

5. requirements.txt
    - Lists the relevant dependencies used in the program.

Where the overall design is concerned, I certainly relied on my personal equity research experience as well as knowledge accrued from my undergraduate degree
- which was in Accounting and Finance. I wanted to include a broader range of functionality, but was unable to due to time or resource constraints as I
- allocated myself 3 days to get the project done in order to take up a subsequent course.

I  plan to incorporate the following features if I continue to develop the project:

1. Access to different Financial Products and Markets - not committed enough to the project for a premium API

2. Additional Data - Formularisation of certain metrics involving a large amount of calculation

3. Additional graphs - Interactive Graphs with different time-frame and technical-indicator overlay options

4. Option to customise report output, by including or not including certain metrics/graphs or customisation in aesthetic choices (colour, font etc.)# rapidresearch

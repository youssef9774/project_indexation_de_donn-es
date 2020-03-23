#question 1
from fileFunction import scrapWebSite
url = "https://www.allrecipes.com/recipes/96/salad/"
print(scrapWebSite(url).text)
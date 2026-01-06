If I get the RSS of a site, I don't need the playwright level extraction at all.
If I can store RSS links of a site , then i would know how to access RSS of a news from the specific site.
but I would need the links of articles/news. I would category based RSS feed.
From that RSS feed I can extract RSS of article.
## Jan 4
- I need to be able to get articles from specific publishes - need a list of publishers
# Tasks
- [ ] Way to get RSS feed based on category.
- [ ]  Extract URL of articles - 10 per sources


# Problems
- Using google news as URL extractor doesn't work, because even though Google News has RSS Feed and links to articles can be pulled from there, the redirection to original publisher makes a hit to link to article use less, unless you know the subsequent URL which is comming up. 

# learnings
There is a difference between module and scripts in python, which is obvious.
Modules are meant to imported. Scripts are meant to be ran. Obvious.
-m flags to run as a module. what?
means run the module as a script. Find the module's __main__ or the package ie main.py and run that first, followed by module.py. Wrong.
means runs the module as a script. Meaning runs as __main__ == __name__. or else __name__ would be file name.
-m doesn't take file paths. so no ./ or .py.

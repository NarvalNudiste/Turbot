import urllib.request
import urllib.parse
import re
#simple request to avoid youtube api data usage
def ytSearch(searchString):
    #returns the video id of a youtube search
    query_string = urllib.parse.urlencode({"search_query" : searchString})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return search_results[0]

import sys, urllib, urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcplugin


def main():
    WEB_PAGE_BASE = 'http://www.tvkstella.pl/archiwum'
    url = WEB_PAGE_BASE
    
    startstring = '<img src="img/video2.gif" border="0" height="16" width="16" alt=""/>&nbsp;&nbsp;&nbsp;<a href="/archiwum" onClick="archiwum(\'video.php?id='
    endstring = ';return false">'
    
    print startstring

    print endstring

    
    
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        videos = extractAll(content, startstring, endstring)
 
 
def extractAll(text, startText, endText):
    """
    Extract all occurences of string within text that start with startText and end with endText
    
    Parameters:
    text: the text to be parsed
    startText: the starting tokem
    endText: the ending token
    
    Returns an array containing all occurences found, with tabs and newlines removed and leading whitespace removed
    """
    result = []
    start = 0
    pos = text.find(startText, start)
    while pos != -1:
        start = pos + startText.__len__()
        end = text.find(endText, start)
        #result.append(text[start:end].replace('\n', '').replace('\t', '').lstrip())
        result.append(text[start:end].replace('\')', '').lstrip())
        pos = text.find(startText, end)
    
    print result
    return result


if __name__ == '__main__':
  main()
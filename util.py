import sys, urllib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

def playMedia(title, thumbnail, link, mediaType='Video') :
    """Plays a video

    Arguments:
    title: the title to be displayed
    thumbnail: the thumnail to be used as an icon and thumbnail
    link: the link to the media to be played
    mediaType: the type of media to play, defaults to Video. Known values are Video, Pictures, Music and Programs
    """
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=link)
    li.setInfo(type=mediaType, infoLabels={ "Title": title })
    xbmc.Player().play(item=link, listitem=li)


def parseParameters(inputString=sys.argv[2]):
    """Parses a parameter string starting at the first ? found in inputString
    
    Argument:
    inputString: the string to be parsed, sys.argv[2] by default
    
    Returns a dictionary with parameter names as keys and parameter values as values
    """
    parameters = {}
    p1 = inputString.find('?')
    if p1 >= 0:
        splitParameters = inputString[p1 + 1:].split('&')
        for nameValuePair in splitParameters:
            if (len(nameValuePair) > 0):
                pair = nameValuePair.split('=')
                key = pair[0]
                value = urllib.unquote(urllib.unquote_plus(pair[1])).decode('utf-8')
                parameters[key] = value
    return parameters

def notify(addonId, message, timeShown=5000):
    """Displays a notification to the user
    
    Parameters:
    addonId: the current addon id
    message: the message to be shown
    timeShown: the length of time for which the notification will be shown, in milliseconds, 5 seconds by default
    """
    addon = xbmcaddon.Addon(addonId)
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'), message, timeShown, addon.getAddonInfo('icon')))


def showError(addonId, errorMessage):
    """
    Shows an error to the user and logs it
    
    Parameters:
    addonId: the current addon id
    message: the message to be shown
    """
    notify(addonId, errorMessage)
    xbmc.log(errorMessage, xbmc.LOGERROR)

def extractInfo(text, startText, endText):
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
        result.append(text[start:end].replace('\')', '').lstrip())
        pos = text.find(startText, end)

    return result

    
def makeLink(params, baseUrl=sys.argv[0]):
    """
    Build a link with the specified base URL and parameters
    
    Parameters:
    params: the params to be added to the URL
    BaseURL: the base URL, sys.argv[0] by default
    """
    return baseUrl + '?' +urllib.urlencode(dict([k.encode('utf-8'),unicode(v).encode('utf-8')] for k,v in params.items()))


def makeTitle(argTitle):
    """
    Build a title depending on the content
    
    Parameters:
    params: the params 
    """
    if 'si' in argTitle:
        return 'Serwis Informacyjny z dnia: %s.%s.20%s' % (argTitle[-6:-4], argTitle[-4:-2], argTitle[-2:])
        #print 'tre' title = 'Serwis Informacyjny z dnia: %s.%s.20%s' % (argTitle[-1:2], (argTitle[-3:2], argTitle[-5:2])
    if 'ik' in argTitle:
        return 'Informacje Kulturalne z dnia: %s.%s.20%s' % (argTitle[-6:-4], argTitle[-4:-2], argTitle[-2:])
    if 'is' in argTitle:
        return 'Informacje Sportowe z dnia: %s.%s.20%s' % (argTitle[-6:-4], argTitle[-4:-2], argTitle[-2:])
    return


def addMenuItem(caption, link, icon=None, thumbnail=None, folder=False):
    #util.addMenuItem(params['title'], link, 'DefaultVideo.png', params['image'], False)
    """
    Add a menu item to the xbmc GUI
    
    Parameters:
    caption: the caption for the menu item
    icon: the icon for the menu item, displayed if the thumbnail is not accessible
    thumbail: the thumbnail for the menu item
    link: the link for the menu item
    folder: True if the menu item is a folder, false if it is a terminal menu item
    
    Returns True if the item is successfully added, False otherwise
    """
    listItem = xbmcgui.ListItem(unicode(caption), iconImage=icon, thumbnailImage=thumbnail)
    listItem.setInfo(type="Video", infoLabels={ "Title": caption })
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=link, listitem=listItem, isFolder=folder)
  

def endListing():
    """
    Signals the end of the menu listing
    """
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
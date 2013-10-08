import util, urllib2

def playVideo(params):
    #response = urllib2.urlopen(params['video'])
    #if response and response.getcode() == 200:
        #content = response.read()
        #print params['video']
        util.playMedia(params['title'], params['image'], params['video'], 'Video')
   # else:
        #util.showError(ADDON_ID, 'Could not open URL %s to get video information' % (params['video']))
    
def buildMenu():
    url = WEB_PAGE_BASE
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        params = {}
        videos = util.extractInfo(content, STARTSTRING, ENDSTRING)
        for video in videos:
            linkTitle = util.makeTitle(video)
            params = {'play':1}
            params['video'] = 'http://www.tvkstella.pl/play.php?id=%s' % video
            params['image'] = 'http://www.tvkstella.pl/img/nowe/%s.jpg' % video
            params['title'] = linkTitle
            link = util.makeLink(params)
            util.addMenuItem(linkTitle, link, 'DefaultVideo.png', params['image'], False)
        util.endListing()
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))

WEB_PAGE_BASE = 'http://www.tvkstella.pl/archiwum'
ADDON_ID = 'plugin.video.TVKStella'
STARTSTRING = '<img src="img/video2.gif" border="0" height="16" width="16" alt=""/>&nbsp;&nbsp;&nbsp;<a href="/archiwum" onClick="archiwum(\'video.php?id='
ENDSTRING = ';return false">'

def main():
    buildMenu()


parameters = util.parseParameters()
if 'play' in parameters:
    playVideo(parameters)
else:
    buildMenu()

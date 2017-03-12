'''
Name: Jason Le
Email: le.kent.jason@gmail.com
Github: jQwotos
'''

import os
import logging
import re

import requests

import constants

# Returns a list of results
def search(keyword, numResults = 99):
    '''

    Scrapes the search query page of 9anime in order to find shows
    Returns a list of shows in the following format
    [{'link': 'A URL to the show', 'title': 'The name of the show'}]

    '''
    payload = {'keyword': keyword}
    headers = {'Referer': 'https://google.com'}
    page = requests.get(constants.SEARCH_URL, params=payload, headers=headers).content
    soupedPage = BeautifulSoup(page, "html.parser")

    shows = []
    numFound = 0

    listFilm = soupedPage.findAll(attrs={'class': 'list-film'})

    if len(listFilm) > 0:
        listFilm = listFilm[0]
        listFilm = listFilm.findAll(attrs={'class': 'row'})

        if len(listFilm) > 0:
            showsSouped = listFilm[0].findAll(attrs={'class': 'item'})

            if len(showsSouped) > 0:
                for show in showsSouped:
                    numFound += 1
                    if numFound > numResults: break
                    shows.append({
                        'link': show.findAll(attrs={'class': 'name'})[0]['href'],
                        'title': show.findAll(attrs={'class': 'name'})[0].text,
                    })
            else
                logging.info("Could not find any Shows when searching for %s" % (keyword))
        else
            logging.info("Unable to find any rows pertaining to search query %s" % (keyword))
    logging.info("Found a total of %i shows when searching for %s at a limit of %i shows." % (len(shows), keyword, numResults))
    return shows

def get_mp4(id):
    '''

    Returns a list of MP4 links by taking in an episode ID
    [{'type': 'file format', 'file': 'link to video file', 'label': 'resolution / quality of file'}]

    '''
    payload = {
        'id': id
    }

    details = requests.get(constants.INFO_API, params=payload).json()
    payload['token'] = details['params']['token']
    logging.info("Acquired token %s when requested from id %s" % (payload['token'], payload['id']))

    data = requests.get(constants.GRABBER_API, params=payload).json()['data']
    logging.info("Recieved %i different links for id %s" % (len(data), payload['id']))
    return data
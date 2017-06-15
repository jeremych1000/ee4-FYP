from __future__ import unicode_literals
from django.conf import settings
import twitter, json, googlemaps


def post_to_twitter(location1, location2, speed, pic_url, pic_url2):
    api = twitter.Api(
        consumer_key='aUe3p3vkiih5tVoOr9NwQfklw',
        consumer_secret='hlsGz9o8ZlUtUrRM5PVUlgWXCur1Fr54KUkJ4qRoZAEqIC4kYt',
        access_token_key='398428540-pU1SxHhVZlU09WSt5Jo7AofhNBkXZWI47YyMSHpu',
        access_token_secret='J3RqksPucuON7uQDafXScxUinxknHwTGPDsUH8JLVBuH2'
    )

    # gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)#'AIzaSyAa6ZK81sMBK2dVrGcOVaWhKUVyfvyUft8')
    # lo1 = gmaps.reverse_geocode(latlng=(51.499691, -0.179612))[0]["formatted_address"]
    # lo2 = gmaps.reverse_geocode(latlng=(51.399691, -0.179612))[0]["formatted_address"]

    status = "Speeding car detected using EE4-DRTSM between " \
             + str(location1[0]) + "," + str(location1[1]) \
             + " and " + str(location2[0]) + "," + str(location2[1]) \
             + ", doing " + str(speed) + " mph, evidence attached."

    # print(status, type(status))
    # print(pic_url, type(pic_url))
    # print(pic_url2, type(pic_url2))

    # status= 'Speeding car detected using EE4-DRTSM between 51.499691,-0.179612 and 51.520700,-0.196500, doing 9173.25 mph, evidence attached.'
    # pic_url = 'http://86.177.166.34:34571/alpr/home/pi/test_videos/walking/VID_20170528_200924/20170528_200924_600000.png'
    # pic_url2 = 'http://86.177.166.34:34572/alpr/home/pi/test_videos/walking/VID_20170528_200925/20170528_200925_600000.png'

    ret = api.PostMultipleMedia(status=status, media=[pic_url, pic_url2])

    #print(json.dumps(ret.AsDict(), indent=2), type(ret))

    post_url = ret.AsDict()["urls"][0]["url"]

    return post_url


    # a=post_to_twitter((0,0),(0,0),0,0,0)
    # print(a)

import twitter, json

def setup_twitter():
    api = twitter.Api(
        consumer_key='aUe3p3vkiih5tVoOr9NwQfklw',
        consumer_secret='hlsGz9o8ZlUtUrRM5PVUlgWXCur1Fr54KUkJ4qRoZAEqIC4kYt',
        access_token_key='398428540-pU1SxHhVZlU09WSt5Jo7AofhNBkXZWI47YyMSHpu',
        access_token_secret='J3RqksPucuON7uQDafXScxUinxknHwTGPDsUH8JLVBuH2'
    )
    print(api.VerifyCredentials())
    return api

def post_to_twitter(api, status, pic_url):

    status = 'speeding car detected, evidence attached'
    pic_url = 'http://jeremych.zapto.org:34571/alpr/home/pi/test_videos/walking/VID_20170528_200924/20170528_200924_600000.png'
    ret = api.PostMedia(status=status, media=pic_url)
    print(ret)
    return ret

api = setup_twitter()
post_to_twitter(api, 0, 0)
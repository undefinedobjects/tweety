import tweepy
import re
import time

def main():
    consumer_key = "" 
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    commentTagUser = ["@x", "@y", "@z", "@q", "@w"]

    urls = []
    with open("cekilis.txt", 'r+') as file:
            urls = file.read().splitlines()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    searchDraw = tweepy.Cursor(api.search, q="#çekiliş").items(50)
    for tweet in searchDraw:
        url = f"https://twitter.com/user/status/{tweet.id}"
        
        if url not in urls:
            print("Eklendi:", url)
            urls.append(url)

            info = []

            if re.search(r"(rt|retweet)", tweet.text, re.IGNORECASE):
                try:
                    tweet.retweet()
                    info.append("Retweetlendi")
                except:
                    pass

            if re.search(r"(beğen|favori|\sfav)", tweet.text, re.IGNORECASE):
                try:
                    tweet.favorite()
                    info.append("Favorilendi")
                except:
                    pass
            
            if re.search(r"takip", tweet.text, re.IGNORECASE):
                try:
                    api.create_friendship(tweet.user.id)
                    info.append("Takip Edildi")
                except:
                    pass
            
            if re.search(r"([0-9])\s+(kişi|arkadaş)", tweet.text, re.IGNORECASE):
                userNumber = re.search(r"([0-9]) (kişi|arkadaş)", tweet.text, re.IGNORECASE).groups(0)[0]

                try:
                    api.update_status(" ".join(commentTagUser[:int(userNumber)]), in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                    info.append(userNumber + " Kişi Etiketlendi")
                except tweepy.TweepError as e:
                    pass

            elif re.search(r"(bir|iki|üç|dört|beş|altı)\s+(kişi|arkadaş)", tweet.text, re.IGNORECASE):
                userNumber = re.search(r"(bir|iki|üç|dört|beş|altı)\s+(kişi|arkadaş)", tweet.text, re.IGNORECASE).groups(0)[0]

                try:
                    api.update_status(" ".join(commentTagUser[:int(getDigit(userNumber))]), in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                    info.append(userNumber + " Kişi Etiketlendi")
                except tweepy.TweepError as e:
                    pass

            if info:        
                print(*info, sep=", ", end=".\n")

            with open("cekilis.txt", "a") as file:
                file.write(url + "\n")
            
            time.sleep(15)

def getDigit(string):
    string = string.lower()
    if string == "bir":
        return 1
    elif string == "iki":
        return 2
    elif string == "üç":
        return 3
    elif string == "dört":
        return 4
    elif string == "beş":
        return 5
    elif string == "altı":
        return 6

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60 * 5)
import tweepy


consumer_key = "hr8ClRl4AniT2jdRHSTfkKuWu"
consumer_secret = "MHQpKBQCPFoRztKi4Z4MIKkCccgDtwTFQrXb4bLO2Xev5Mr5Yv"
access_token = "1235232986909601793-YORkwEC1S6879MssIlsWnpYsgxtYgR"
access_token_secret = "BboF9MdYCZ8kgFDAQkSTXkSK5nOpVh23juDhqHba6vQGv"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

blockTwitterForTesting = True

if True:
    print("------------BOT CONTROL------------")
    print("Si desea activar el bot entonces:")
    if input("Esta seguro? [y / n]: ") == "y":
        if input("Escriba 'ENABLE_TWEET': \n") == "ENABLE_TWEET":
            print("BLOQUEO de twitteo DESACTIVADO. (" + str(blockTwitterForTesting) + ")")
            blockTwitterForTesting = False
        else:
            print("Cancelado")
            print("El bloqueo NO se ha DESACTIVADO, Modo Seguro " + str(blockTwitterForTesting))
    else:
        print("El bloqueo NO se ha DESACTIVADO, Modo Seguro " + str(blockTwitterForTesting))
    print("-----------------------------------")


def twittea(frase):
    global blockTwitterForTesting
    if blockTwitterForTesting:
        print("No se puden escribir tweets ya que se ha bloqueado. Para hacerlo cambia el valor de la variable"
              " 'blockTwitterForTesting'")
        print("Esto es lo que se iba a Twittear: '" + str(frase) + "'")
    else:
        api.update_status(frase)


def prevTweets(cuant):
    aar = []
    for status in tweepy.Cursor(api.user_timeline).items(cuant):
        # print(status._api)
        # print(status._json['text'])
        aar.append(status._json['text'])

    return aar

import tweepy
import config

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Valores predeterminados: Son estos para evita el envio de tweets desaforunado
blockTwitterForTesting = True
notifyWhenTweetToUser = False

if True:
    print("------------BOT CONTROL------------")
    print("Si desea activar las funciones del bot entonces:")
    if input("Esta seguro? [y / n]: ") == "y":
        print("Para desactival el bloqueo de twitteo")
        if input("Escriba 'ENABLE_TWEET': \n") == "ENABLE_TWEET":
            blockTwitterForTesting = False
            print("BLOQUEO de twitteo DESACTIVADO. (" + str(blockTwitterForTesting) + ")")
        else:
            print("Cancelado")
            print("El bloqueo NO se ha DESACTIVADO, Modo Seguro " + str(blockTwitterForTesting))

        print("Para activar las notificaciones privadas a md")
        if input("Escriba 'ENABLE_NOTIFTOUSER': \n") == "ENABLE_NOTIFTOUSER":
            notifyWhenTweetToUser = True
            print("NOTIFICACIONES de twitteo por md ACTIVADAS. (" + str(notifyWhenTweetToUser) + ")")

        else:
            print("Cancelado")
            print("NOTIFICACIONES de twitteo por md DESACTIVADAS, Modo Silencio " + str(notifyWhenTweetToUser))
    else:
        print("El bloqueo NO se ha DESACTIVADO, Modo Seguro " + str(notifyWhenTweetToUser))
        print("NOTIFICACIONES de twitteo por md DESACTIVADAS, Modo Silencio " + str(notifyWhenTweetToUser))
    print("-----------------------------------")


def twittea(frase):
    global blockTwitterForTesting
    if blockTwitterForTesting:
        print("No se puden escribir tweets ya que se ha bloqueado. Para hacerlo cambia el valor de la variable"
              " 'blockTwitterForTesting'")
        print("Esto es lo que se iba a Twittear: '" + str(frase) + "'")

    else:
        api.update_status(frase)

    sendMdToUsers(frase, True)


def prevTweets(cuant):
    aar = []
    for status in tweepy.Cursor(api.user_timeline).items(cuant):
        # print(status._api)
        # print(status._json['text'])
        aar.append(status._json['text'])

    return aar

def sendMdToUsers(text, confirm = False):
    if notifyWhenTweetToUser and confirm:
        for userId in config.listOfidsOfTwitterUser:
            api.send_direct_message(userId, text)

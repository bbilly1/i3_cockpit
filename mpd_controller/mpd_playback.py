from time import sleep

def fade(way, current_vol, client):
    """ gracefull fading """
    if way == 'out':
        steps = int(current_vol / 2)
        amount = -2
    elif way == 'in':
        steps = 50
        amount = +2
    for i in range(steps):
        client.volume(amount)
        sleep(0.03)


def toggle(client):
    """ toggles play status """
    # setup
    client_status = client.status()
    # switch
    current_vol = int(client_status['volume'])
    if client_status['state'] == 'play':
        fade('out', current_vol, client)
        client.pause()
    elif client_status['state'] == 'pause':
        client.setvol(0)
        client.play()
        fade('in', current_vol, client)
    

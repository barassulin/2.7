

def send_protocol(message):

    """

    length = str(len(message))
    zfill_length = length.zfill(2)
    message = zfill_length + message
    """

    return message

def recive_protocol(message):
    got=message
    """
    got = True
    length = int(message[0:2],16)
    length2 =len(message[2:])
    if length==length2:
        got = False
    
    """
    return got







"""if works without add this:"""
def recv_parameters(message):
    client_socket.send(send_protocol(message).encode())
    parameter = client_socket.recv(MAX_PACKET).decode()
    recv_protocol(parameter)
    return parameter


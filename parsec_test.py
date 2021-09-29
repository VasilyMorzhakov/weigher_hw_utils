import parsec
import time

if __name__=='__main__':
    server_IP=input('Enter server IP:')
    parsec_IP=input('Enter parsec IP:')

    try:
        p = parsec.Parsec(server_IP, parsec_IP)

        p.connect()
        
        version=p.get_version()
        print('Version received, connected')
        print(version)
        
        p.clear_transaction()

        while True:
            res = p.ask_transaction()
            if res is not None:
                print(time.time())
                print(res)

    except Exception as e:
        print(e)
        time.sleep(10.0)

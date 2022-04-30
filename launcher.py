from subprocess import Popen, CREATE_NEW_CONSOLE


process = []

while True:
    action = input('Выберите действие: q - выход , s - запустить сервер и клиенты, x - закрыть все окна:')

    if action == 'q':
        break
    elif action == 's':
        process.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))
        process.append(Popen('python client.py -n test1', creationflags=CREATE_NEW_CONSOLE))
        process.append(Popen('python client.py -n test2', creationflags=CREATE_NEW_CONSOLE))
        process.append(Popen('python client.py -n test3', creationflags=CREATE_NEW_CONSOLE))
    elif action == 'x':
        while process:
            victim = process.pop()
            victim.kill()

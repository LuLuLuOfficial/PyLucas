import msvcrt

print("按任意键退出...")
while True:
    if msvcrt.kbhit():
        key = msvcrt.getch()
        print(f'{key}')
        break
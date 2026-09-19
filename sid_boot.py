import os
import time
import psutil
import requests
import threading
import msvcrt
from datetime import datetime
from colorama import Fore, init
import random

init(autoreset=True)

CITY = "???"
API_KEY = "???"

skip = False

def listen_for_skip():
    global skip
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().lower()
            if key == b's':
                skip = True
                break

threading.Thread(target=listen_for_skip, daemon=True).start()

def clear():
    os.system("cls")

def type_text(text, delay=0.02):
    for c in text:
        if skip:
            print(text)
            return
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

Openings = [r"""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░▄▄▀▀▀▀▀▀▀▀▀▀▄▄█▄░░░░▄░░░░█░░░░░░░
░░░░░░█▀░░░░░░░░░░░░░▀▀█▄░░░▀░░░░░░░░░▄░
░░░░▄▀░░░░░░░░░░░░░░░░░▀██░░░▄▀▀▀▄▄░░▀░░
░░▄█▀▄█▀▀▀▀▄░░░░░░▄▀▀█▄░▀█▄░░█▄░░░▀█░░░░
░▄█░▄▀░░▄▄▄░█░░░▄▀▄█▄░▀█░░█▄░░▀█░░░░█░░░
▄█░░█░░░▀▀▀░█░░▄█░▀▀▀░░█░░░█▄░░█░░░░█░░░
██░░░▀▄░░░▄█▀░░░▀▄▄▄▄▄█▀░░░▀█░░█▄░░░█░░░
██░░░░░▀▀▀░░░░░░░░░░░░░░░░░░█░▄█░░░░█░░░
██░░░░░░░░░░░░░░░░░░░░░█░░░░██▀░░░░█▄░░░
██░░░░░░░░░░░░░░░░░░░░░█░░░░█░░░░░░░▀▀█▄
██░░░░░░░░░░░░░░░░░░░░█░░░░░█░░░░░░░▄▄██
░██░░░░░░░░░░░░░░░░░░▄▀░░░░░█░░░░░░░▀▀█▄
░▀█░░░░░░█░░░░░░░░░▄█▀░░░░░░█░░░░░░░▄▄██
░▄██▄░░░░░▀▀▀▄▄▄▄▀▀░░░░░░░░░█░░░░░░░▀▀█▄
░░▀▀▀▀░░░░░░░░░░░░░░░░░░░░░░█▄▄▄▄▄▄▄▄▄██
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
""",
r"""
              _-o#&&*''''?d:>b\_
          _o/"`''  '',, dMF9MMMMMHo_
       .o&#'        `"MbHMMMMMMMMMMMHo.
     .o"" '         vodM*$&&HMMMMMMMMMM?.
    ,'              $M&ood,~'`(&##MMMMMMH\
   /               ,MMMMMMM#b?#bobMMMMHMMML
  &              ?MMMMMMMMMMMMMMMMM7MMM$R*Hk
 ?$.            :MMMMMMMMMMMMMMMMMMM/HMMM|`*L
|               |MMMMMMMMMMMMMMMMMMMMbMH'   T,
$H#:            `*MMMMMMMMMMMMMMMMMMMMb#}'  `?
]MMH#             ""******#MMMMMMMMMMMMM'    -
MMMMMb_                   |MMMMMMMMMMMP'     :
HMMMMMMMHo                 `MMMMMMMMMT       .
?MMMMMMMMP                  9MMMMMMMM}       -
-?MMMMMMM                  |MMMMMMMMM?,d-    '
 :|MMMMMM-                 `MMMMMMMT .M|.   :
  .9MMM[                    &MMMMM*' `'    .
   :9MMk                    `MMM#"        -
     &M}                     `          .-
      `&.                             .
        `~,   .                     ./
            . _                  .-
              '`--._,dd###pp=""'
""",
r"""
⠄⠄⠄⠄⣠⣴⣿⣿⣿⣷⣦⡠⣴⣶⣶⣶⣦⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⣴⣿⣿⣫⣭⣭⣭⣭⣥⢹⣟⣛⣛⣛⣃⣀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
⠄⣠⢸⣿⣿⣿⣿⢯⡓⢻⠿⠿⠷⡜⣯⠭⢽⠿⠯⠽⣀⠄⠄⠄⠄⠄⠄⠄⠄⠄
⣼⣿⣾⣿⣿⣿⣥⣝⠂⠐⠈⢸⠿⢆⠱⠯⠄⠈⠸⣛⡒⠄⠄⠄⠄⠄⠄⠄⠄⠄
⣿⣿⣿⣿⣿⣿⣿⣶⣶⣭⡭⢟⣲⣶⡿⠿⠿⠿⠿⠋⠄⠄⣴⠶⠶⠶⠶⠶⢶⡀
⣿⣿⣿⣿⣿⢟⣛⠿⢿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣷⡄⠄⢰⠇⠄⠄⠄⠄⠄⠈⣧
⣿⣿⣿⣿⣷⡹⣭⣛⠳⠶⠬⠭⢭⣝⣛⣛⣛⣫⣭⡥⠄⠸⡄⣶⣶⣾⣿⣿⢇⡟
⠿⣿⣿⣿⣿⣿⣦⣭⣛⣛⡛⠳⠶⠶⠶⣶⣶⣶⠶⠄⠄⠄⠙⠮⣽⣛⣫⡵⠊⠁
⣍⡲⠮⣍⣙⣛⣛⡻⠿⠿⠿⠿⠿⠿⠿⠖⠂⠄⠄⠄⠄⠄⠄⠄⠄⣸⠄⠄⠄⠄
⣿⣿⣿⣶⣦⣬⣭⣭⣭⣝⣭⣭⣭⣴⣷⣦⡀⠄⠄⠄⠄⠄⠄⠠⠤⠿⠦⠤⠄⠄
""",
r"""
                                                                    ..;===+.
                                                                .:=iiiiii=+=
                                                             .=i))=;::+)i=+,
                                                          ,=i);)I)))I):=i=;
                                                       .=i==))))ii)))I:i++
                                                     +)+))iiiiiiii))I=i+:'
                                .,:;;++++++;:,.       )iii+:::;iii))+i='
                             .:;++=iiiiiiiiii=++;.    =::,,,:::=i));=+'
                           ,;+==ii)))))))))))ii==+;,      ,,,:=i))+=:
                         ,;+=ii))))))IIIIII))))ii===;.    ,,:=i)=i+
                        ;+=ii)))IIIIITIIIIII))))iiii=+,   ,:=));=,
                      ,+=i))IIIIIITTTTTITIIIIII)))I)i=+,,:+i)=i+
                     ,+i))IIIIIITTTTTTTTTTTTI))IIII))i=::i))i='
                    ,=i))IIIIITLLTTTTTTTTTTIITTTTIII)+;+i)+i`
                    =i))IIITTLTLTTTTTTTTTIITTLLTTTII+:i)ii:'
                   +i))IITTTLLLTTTTTTTTTTTTLLLTTTT+:i)))=,
                   =))ITTTTTTTTTTTLTTTTTTLLLLLLTi:=)IIiii;
                  .i)IIITTTTTTTTLTTTITLLLLLLLT);=)I)))))i;
                  :))IIITTTTTLTTTTTTLLHLLLLL);=)II)IIIIi=:
                  :i)IIITTTTTTTTTLLLHLLHLL)+=)II)ITTTI)i=
                  .i)IIITTTTITTLLLHHLLLL);=)II)ITTTTII)i+
                  =i)IIIIIITTLLLLLLHLL=:i)II)TTTTTTIII)i'
                +i)i)))IITTLLLLLLLLT=:i)II)TTTTLTTIII)i;
              +ii)i:)IITTLLTLLLLT=;+i)I)ITTTTLTTTII))i;
             =;)i=:,=)ITTTTLTTI=:i))I)TTTLLLTTTTTII)i;
           +i)ii::,  +)IIITI+:+i)I))TTTTLLTTTTTII))=,
         :=;)i=:,,    ,i++::i))I)ITTTTTTTTTTIIII)=+'
       .+ii)i=::,,   ,,::=i)))iIITTTTTTTTIIIII)=+
      ,==)ii=;:,,,,:::=ii)i)iIIIITIIITIIII))i+:'
     +=:))i==;:::;=iii)+)=  `:i)))IIIII)ii+'
   .+=:))iiiiiiii)))+ii;
  .+=;))iiiiii)));ii+
 .+=i:)))))))=+ii+
.;==i+::::=)i=;
,+==iiiiii+,
`+=+++;`
""",
r"""
             ______
          ,'"       "-._
        ,'              "-._ _._
        ;              __,-'/   |
       ;|           ,-' _,'"'._,.
       |:            _,'      |\ `.
       : \       _,-'         | \  `.
        \ \   ,-'             |  \   \
         \ '.         .-.     |       \
          \  \         "      |        :
           `. `.              |        |
             `. "-._          |        ;
             / |`._ `-._      L       /
            /  | \ `._   "-.___    _,'
           /   |  \_.-"-.___   ""*"
           \   :            /"*"
            `._\_       __.'_
       __,--''_ ' "--'''' \_  `-._
 __,--'     .' /_  |   __. `-._   `-._
<            `.  `-.-''  __,-'     _,-'
 `.            `.   _,-'"      _,-'
   `.            ''"       _,-'
     `.                _,-'
       `.          _,-'
         `.   __,'"
           `'"
""",
r"""
 /\/\/\                            /  \
| \  / |                         /      \
|  \/  |                       /          \
|  /\  |----------------------|     /\     |
| /  \ |                      |    /  \    |
|/    \|                      |   /    \   |
|\    /|                      |  | (  ) |  |
| \  / |                      |  | (  ) |  |
|  \/  |                 /\   |  |      |  |   /\
|  /\  |                /  \  |  |      |  |  /  \
| /  \ |               |----| |  |      |  | |----|
|/    \|---------------|    | | /|   .  |\ | |    |
|\    /|               |    | /  |   .  |  \ |    |
| \  / |               |    /    |   .  |    \    |
|  \/  |               |  /      |   .  |      \  |
|  /\  |---------------|/        |   .  |        \|
| /  \ |              /   NASA   |   .  |  NASA    \
|/    \|              (          |      |           )
|/\/\/\|               |    | |--|      |--| |    |
------------------------/  \-----/  \/  \-----/  \--------
                        \\//     \\//\\//     \\//
                         \/       \/  \/       \/
""",
r"""
                     _  _     ____________.--.
                  |\|_|//_.-"" .'    \   /|  |
                  |.--""-.|   /       \_/ |  |
                  \  ||  /| __\_____________ |
                  _\_||_/_| .-""            ""-.  __
                .' '.    \//                    ".\/
                ||   '. >()_                     |()
                ||__.-' |/\ \                    |/\
                   |   / "|  \__________________/.""
                  /   //  | / \ "-.__________/  /\
               ___|__/_|__|/___\___".______//__/__\
              /|\     [____________] \__/         |\
             //\ \     |  |=====| |   /\\         |\\
            // |\ \    |  |=====| |   | \\        | \\        ____...____....----
          .//__| \ \   |  |=====| |   | |\\       |--\\---"--""     .            ..
_____....-//___|  \_\  |  |=====| |   |_|_\\      |___\\    .                 ...'
 .      .//-.__|_______|__|_____|_|_____[__\\_____|__.-\\      .     .    ...::
        //        //        /          \ `-_\\/         \\          .....:::
  -... //     .  / /       /____________\    \\       .  \ \     .            .
      //   .. .-/_/-.                 .       \\        .-\_\-.                 .
     / /      '-----'           .             \ \      '._____.'         .
  .-/_/-.         .                          .-\_\-.                          ...
 '._____.'                            .     '._____.'                       .....
        .                                                             ...... ..
    .            .                  .                        .
   ...                    .                      .                       .      .
        ....     .                       .                    ....
 JRO      ......           . ..                       ......'
             .......             '...              ....
                                   ''''''      .              .

""",
r"""
.     .       .  .   . .   .   . .    +  .
  .     .  :     .    .. :. .___---------___.
       .  .   .    .  :.:. _".^ .^ ^.  '.. :"-_. .
    .  :       .  .  .:../:            . .^  :.:\.
        .   . :: +. :.:/: .   .    .        . . .:\
 .  :    .     . _ :::/:               .  ^ .  . .:\
  .. . .   . - : :.:./.                        .  .:\
  .      .     . :..|:                    .  .  ^. .:|
    .       . : : ..||        .                . . !:|
  .     . . . ::. ::\(                           . :)/
 .   .     : . : .:.|. ######              .#######::|
  :.. .  :-  : .:  ::|.#######           ..########:|
 .  .  .  ..  .  .. :\ ########          :######## :/
  .        .+ :: : -.:\ ########       . ########.:/
    .  .+   . . . . :.:\. #######       #######..:/
      :: . . . . ::.:..:.\           .   .   ..:/
   .   .   .  .. :  -::::.\.       | |     . .:/
      .  :  .  .  .-:.":.::.\             ..:/
 .      -.   . . . .: .:::.:.\.           .:/
.   .   .  :      : ....::_:..:\   ___.  :/
   .   .  .   .:. .. .  .: :.:.:\       :/
     +   .   .   : . ::. :.:. .:.|\  .:/|
     .         +   .  .  ...:: ..|  --.:|
.      . . .   .  .  . ... :..:.."(  ..)"
 .   .       .      :  .   .: ::/  .  .::\
""",
r"""
                    ___                                          ___
 __________________/  /                       __________________/  /
| _    _______    /  /                       | _    _______    /  /
|(_) .d########b. //)| _____________________ |(_) .d########b. //)|
|  .d############//  ||        _____        ||  .d############//  |
| .d######""####//b. ||() ||  [MUSIC]  || ()|| .d######""####//b. |
| 9######(  )#_//##P ||()|__|  | = |  |__|()|| 9######(  )#_//##P |
| 'b######++#/_/##d' ||() ||   | = |   || ()|| 'b######++#/_/##d' |
|  "9############P"  ||   ||   |___|   ||   ||  "9############P"  |
|  _"9a#######aP"    ||  _   _____..__   _  ||  _"9a#######aP"    |
| |_|  `""""''       || (_) |_____||__| (_) || |_|  `""""''       |
|  ___..___________  ||_____________________||  ___..___________  |
| |___||___________| |                       | |___||___________| |
|____________________|♬ ♩ ♩ ♯ ♪ ♮ ♫ ♭ ♩ ♩ ♪ ♩ |____________________|
""",
r"""
        ___
    .-"`   `"-.
  .'           '.
 /               \
/  #              \
| #               |
|                 |
;     .-~~~-.     ;
 ;     )   (     ;
  \   (     )   /
   \   \   /   /
    \   ) (   /
     |  | |  |
     |__|_|__|
     {=======}
     }======={
     {=======}
     }======={
     {=======}
      `""u""`

"""]

def open_frame():
    print("\r" + Fore.RED + random.choice(Openings))

def get_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').free // (1024**3)
    return cpu, ram, disk

def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=imperial"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return "Weather error (bad API key?)"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"{temp}°F | {desc}"

    except Exception as e:
        return "Weather unavailable"

def get_quote():
    try:
        res = requests.get("https://zenquotes.io/api/random").json()
        return res[0]["q"]
    except:
        return "U GOT THIS!"

def main():

    open_frame()

    print(Fore.RED + r"""
   _____  _  _____ 
  / ____|| ||  __ \
 | (___  | || |  | |
  \___ \ | || |  | |
  ____) || || |__| |
 |_____/ |_||_____/
    """)

    type_text("Welcome back, Sid.\n")

    cpu, ram, disk = get_stats()
    weather = get_weather()
    quote = get_quote()
    now = datetime.now().strftime("%H:%M:%S")

    print(Fore.RED + "~~~ OMEN STATUS ~~~")
    print(f"CPU: {cpu}%")
    print(f"RAM: {ram}%")
    print(f"Disk Free: {disk} GB")
    print(f"Time: {now}")
    print(f"Weather: {weather}")

    print("\nQuote of the Day:")
    type_text(f"\"{quote}\"")

    print("\nOMEN Ready.\n")

if __name__ == "__main__":
    main()

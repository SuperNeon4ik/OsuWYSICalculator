import colorama

def get_map_data(filePath: str):
    data = { 
        "title": "NOT_FOUND",
        "artist": "NOT_FOUND",
        "difficultyTitle": "NOT_FOUND",
        "object_count": 727
    }

    if filePath.startswith('"') and filePath.endswith('"'):
        filePath = filePath[1:len(filePath) - 1]

    file = open(filePath, 'r', encoding="UTF-8")
    countAsObjects = False
    objectCount = 0
    for l in file.readlines():
        if countAsObjects:
            if l.strip() == "":
                countAsObjects = False
            else:
                objectCount += 1
        else:
            if l.__contains__(":"):
                tokens = l.strip().split(":")
                if (tokens[0] == "Title"):
                    data["title"] = tokens[1]
                elif (tokens[0] == "Artist"):
                    data["artist"] = tokens[1]
                elif (tokens[0] == "Version"):
                    data["difficultyTitle"] = tokens[1]
            else:
                if l.strip() == "[HitObjects]":
                    countAsObjects = True
    data["object_count"] = objectCount
    return data

def calculate_acc(greatHits: int, goodHits: int, mehHits: int, totalObjects: int) -> float:
    return round(((300 * greatHits + 100 * goodHits + 50 * mehHits) / (300 * totalObjects)) * 10000) / 100

if __name__ == '__main__':
    colorama.init()

    print("The WYSI Calculator for osu! by SuperNeon4ik")
    print(f"{colorama.Fore.YELLOW}WARNING:{colorama.Fore.RESET} Doesn't work with Score V2!")
    print()

    try:
        diffPath = input("Enter the path to the difficulty file (*.osu): ")

        mapdata = get_map_data(diffPath)

        print(f"Map Data: {colorama.Fore.YELLOW}{str(mapdata)}{colorama.Fore.RESET}")

        hitobjects_count = mapdata["object_count"]

        LB = colorama.Fore.LIGHTBLUE_EX
        GR = colorama.Fore.GREEN
        BL = colorama.Fore.MAGENTA
        RT = colorama.Fore.RESET

        for i in range(hitobjects_count):
            for good in range(0, 15):
                for meh in range(0, 15):
                    acc = calculate_acc(i + 1 - good - meh, good, meh, hitobjects_count)
                    if (str(acc).endswith("7.27")): # the most reliable method of checking for the thing, ik
                        print(f"WYSI! 300x{LB}{i + 1 - good - meh}{RT} 100x{GR}{good}{RT} 50x{BL}{meh}{RT} / {hitobjects_count} : {str(acc)}%")

        print()
        print(f"Showing results for {colorama.Fore.YELLOW}{mapdata['artist']} - {mapdata['title']} [{mapdata['difficultyTitle']}]{colorama.Fore.RESET}")
        if mapdata["artist"] != "xi":
            print(f"{colorama.Fore.YELLOW}WARNING:{colorama.Fore.RESET} The artist is not 'xi', which means you will not get the medal, since it's one of the requirements.")
    except:
        print(f"{colorama.Fore.RED}ERROR:{colorama.Fore.RESET} Bad map difficulty file.")

    input('Press ENTER to exit.')

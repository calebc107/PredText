import time
import requests

headers = {"Authorization": "bearer " + "",
           "User-Agent": "Ubuntu:predText:v1"}


def uniqueID(commentsdb, id):
    for comment in commentsdb:
        if comment['data']['id'] == id:
            return False
    return True


def DownloadThings(url, count):
    if not url.startswith("http"):
        url = "http://" + url
    if "?" in url:
        seperator = "&"
    else:
        seperator = "?"
    after = ""
    result = []
    c = 0
    while c < count:
        time.sleep(0.5)
        page = requests.get(
            url + seperator + "raw_json=1&limit=100&after=" + after, headers=headers)
        pagedata = page.json()
        after = pagedata['data']['after']
        posts = pagedata['data']['children']
        l = len(posts)
        if not l > 0 or after is None:
            after = ""
        for post in posts:
            if uniqueID(result, post['data']['id']):
                result.append(post)
                c = c + 1
        print("Downloaded " + str(c) + " out of " + str(count))
    result.sort(key=lambda x: x['data']['id'])
    return result


def sanitize(string):
    result = ""
    string = string.replace("\r", " ")
    string = string.replace("\n", " ")
    string = string.replace("\t", " ")
    string = string.replace("...", " ")
    string = string.replace("]", " ")
    while string.find("  ") > -1:
        string = string.replace("  ", " ")
    words = string.split(' ')
    for word in words:
        word = word.lstrip().rstrip()
        word = word.lower()
        for char in word:
            if char.isalpha() or char == ' ':
                result += char
        result += ' '
    result = result[0:-1]
    while result.find("  ") > -1:
        result = result.replace("  ", " ")
    return result


def hasslur(string):
    for slur in slurs2:
        if slur in sanitize(string):
            return True
    return False


# This is a vulgar variable. It's defined so that these words can be filtered out of content

slurs2 = ["abbie", "abie", "abid", "abeed", "abbo", "afro", "alibaba", "gatorbait", "annamite", "aseng", "arabush", "auntjemima",
          "ayrab", "bamboula", "beaner", "beaney", "bluegum", "boche", "bosch", "bogtrotter", "bohunk", "boong", "bung", "bong", "boong", "bunga", "boonie", "bootlip", "boungoule", "bountybar", "bozgor", "brownie", "buddahead", "bule", "cameljockey", "chankoro", "cheesehead", "cheeseeatingsurrendermonkey", "chefur", "chernozhopy", "chilote", "chinaman", "chink", "churka", "chonky", "christkiller", "chocice", "cina", "cokin", "coolie", "coonass", "cracker", "currymuncher", "cushi", "kushi", "dago", "dego", "dalkhor", "darky", "darkey", "darkie",
          "dink", "dogan", "dogun", "dothead", "dunecoon", "eyetie", "farang", "fenian", "feuj", "fritz", "frogeater", "fuzzywuzzy", "gabacho", "gaijin", "gammon",
          "ginjockey", "golliwog", "gook", "gora", "goy", "greaser", "greaseball", "gringo", "groid", "gub", "guiri", "guizi", "guido", "ginzo", "gweilo", "gwailo", "gyopo", "kyopo", "gypsy", "gyppo", "gippo gypo", "gyppie", "gyppy", "gipp", "hairyback", "hajji", "hadji", "halfbreed", "haole",
          "heeb", "hibe", "hillbilly", "honky", "honkey", "honkie", "hunky", "hymie", "ikey", "iky", "ikeymo", "indon", "indonesia", "injun",
          "jakun", "japie", "yarpie", "jerry", "jewboy", "jigaboo", "jiggaboo", "jigarooni", "jijiboo", "zigaboo", "jigg", "jigga", "jigger", "jocky", "jockie", "jungle bunny", "kaffir", "kaffer", "kaffir", "kafir", "kaffre", "kuffar", "kalar", "kalia", "kalu", "kallu", "kanaka", "kanke", "kano", "katsap", "kacap", "kacapas", "kaouiche", "kawish", "kebab", "keling", "kharkhuwa", "khokhol", "kike", "kyke", "kimichi", "knacker", "kolorad", "kraut", "labas", "laowai", "lebo", "limey", "lubra", "lugan", "mabuno", "mahbuno", "macaca", "majus", "malakhkhor", "malaun", "malon", "malingsia", "malingsial", "malingsialan", "maumau", "mick", "mooncricket", "moskal", "mulignan", "mulignon", "moolinyan", "munt", "mzungu", "nawar", "niakou", "niglet", "nignog", "nigger", "nigor", "nigra", "nigre", "nigar", "niggur", "nigga", "niggah", "niggar", "nigguh", "nigress", "nigette", "nitchie", "neche", "neechee", "neejee", "nicji", "nichiwa", "nidge", "nitchee", "nitchy", "nonpri", "monkey", "nusayri", "olah", "overner", "paddy", "paki", "palagi", "paleface", "peckerwood", "piefke", "pickaninny", "pikey", "piky", "piker", "pocho", "pocha", "polak", "polack", "polock", "polaco", "polentone", "pohm", "pommy",
          "pommie", "portagee", "pshek", "quashie", "raghead", "rastus", "razakara", "redlegs", "redneck", "redskin", "rosuke", "roske", "rooinek", "roundeye", "rusnya", "sambo", "sandnigger", "sassenach", "sawney", "scandihoovian", "seppo", "schvartse", "schwartze", "sheeny", "shegetz", "shelta", "shiksa",
          "shiptar", "shkije", "shkutzim", "shylock", "skopianoi", "slanteye", "slopehead", "slopy", "slopey", "sloper", "soosmarkhor", "sooty", "sourpeil", "spearchunker", "squarehead", "squaw", "tacohead", "tiag", "tarbaby", "terrone", "teuchter", "thicklip", "tingtong", "towelhead", "uncle tom", "vatnik", "wetback", "wigger", "whigger", "whitey", "wog", "wop", "yam yam", "yank", "yellow bone", "zipperhead"]

wholewords = ["pom", "ike", "russi", "arab", "nig", "ann", "gin", "abo", "jap",
              "ching", "chong", "hun", "nip", "ape", "armo", "haji", "coon", "chee", "crow",
              "hori", "chug","nere","burr", "cholo","gans"]

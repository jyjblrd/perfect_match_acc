import xlrd
from xlwt import Workbook

# Defining variables
row = 1
col = 9
comment = []
comments = []
tmp_comment_list = []
prox_comments = {}

# Proximity to ski field
prox1 = {"ski slope", "ski field", "lifts", "gondola"}
prox2 = {"connect", "proximity", "minute", "walk", "locat", "bus", "close",
        "shuttle", "meter", "metre", "mins", "min", "driving", "drive",
        "access", "van", "nearby", "car", "distance", "easy to get to",
        "convenient", "isolated", "steps away", "right on"}
prox3 = {"ski in", "ski out"}
prox4 = {"ski into"}

# Close to Restaurant and Shops
clos1 = {"restaurant", "shops", "dining", "bars", "cafe", "village", "pub",
        "main road"}
clos2 = {"walk", "minute", "mins", "nearby", "distance", "locat",
        "easy to get to", "metre", "meter", "street", "access", "min", "close",
        "convenient", "isolated", "steps away", "central", "nearby",
        "in the area", "proximity"}

# Peaceful and Tranquil Location
peac1 = {"peaceful", "restful", "quiet", "serene", "tranquil"}
peac2 = {"remote"}
peac3 = {"location", "road"}
peac4 = {"loud", "nois"}
peac5 = {"sleep", "walls", "hallway", "next door", "woke", "wake", "groomers",
        "machinery", "plow", "issue", "road", "room", "night", "evening",
        "problem", "front"}

# View
view1 = {"view"} #And not "review"

# Onsen / Hot Spring Bath
onse1 = {"onsen", "spa", "hot spring"}

# Bar
bar1 = {"bar"}
bar2 = {"walking", "locat", "dessert", "expresso", "buffet", "bar fridge",
        "snack bar", "next door", "mini"}

# Wifi
wifi1 = {"wifi", "wi-fi"}

# Overall Guest Rating
rate1 = {"overall", "but overall", "summary", "in summary"} #At start of sentence

# Value for Money
valu1 = {"value"}
valu2 = {"restaurant", "bar", "massage", "food", "buffet", "value add", "meal",
        "valued", "the value"}

# Room and Bathroom Size
size1 = {"tiny", "small", "large", "gigantic", "huge", "big"}
size2 = {"room", "toilet", "shower", "bath"}

# Breakfast
brea1 = {"family friendly", "kids", "children", "families"}
brea2 = {"love", "like", "enjoy", "easy", "popular", "beautiful", "lovely",
        "suitable", "dangerous", "recommend", "fun", "delight",
        "entertainment", "fantastic", "great", "glad", "relax", "ideal",
        "perfect", "good", "nice", "comfortable", "sleep"}

# Staff / Service
staf1 = {"staff", "service"}
sraf2 = {"bus service", "shuttle service", "taxi service", "self service",
        "self-service", "a service", "this service", "room service",
        "exchange service", "up service", "rental service", "dinner service",
        "restaurant service", "service shop", "massage service", "off service",
        "laundry service", "free service", "translation service",
        "van service", "transport service", "services manager",
        "service manager"}

# Overall Comfort
comf1 = ["comfortable"]

# Excel spreadsheet setup
wb = Workbook()
workbook = xlrd.open_workbook(
    "/home/j_blrd/webscraping/spreadsheets/comments.xls")
data_sheet = wb.add_sheet("commentExtraction", cell_overwrite_ok=True)
sheet = workbook.sheet_by_index(0)  # Open first sheet

def clearVariables():
    global comment
    global comments
    global col
    global tmp_comment_list

    comment = []
    comments = []
    col = 9
    tmp_comment_list = []

while True:
    print("\n", row)

    hotel_name = sheet.cell_value(row, 0)
    print(hotel_name)

    if sheet.cell_type(row, col) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
        row += 1
        continue

    while True:
        if col == sheet.ncols or sheet.cell_type(row, col) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
            break

        comment = sheet.cell_value(row, col).split("||")[7].split(".") #Gets the actual comment from the spreadsheet and seperates the sentences
        comments.append(comment)
        col += 1

    comments = [element for sublist in comments for element in sublist] #Not really sure how this works but it makes a list of lists into a list
#    print(comments)

    for i in range(0, len(comments)): #Repeat for each comment in the list
        if any(word in comments[i] for word in prox1):
            if any(x in comments[i] for x in prox2):
                tmp_comment_list.append(comments[i])

    prox_comments[hotel_name] = tmp_comment_list

    row +=1
    clearVariables()
    print(prox_comments)

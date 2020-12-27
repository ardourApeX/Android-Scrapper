from urllib.request import urlopen
from bs4 import BeautifulSoup as Soup


android_url = "https://en.wikipedia.org/wiki/Android_version_history"
android_data = urlopen(android_url)
android_html = android_data.read()
android_data.close() #Closing request

# Parsing Data
android_soup = Soup(android_html, "html.parser")
#print(android_soup)

tables = android_soup.find_all("table", {"class" : "wikitable"}) # Find Tables
#print(len(tables))
android_table = tables[0] # Desired table is at position 0
#print(android_table)

head = android_table.findAll("th") # Find all the headers in selected table
#print(len(head))

column_title = [ct.text[:-1] for ct in head] # Extract all the columns name
#print(column_title)

rows_html = android_table.findAll("tr")[1:] # selecting rows only
#print(rows_html)

rows_data = []
for row in rows_html:
    current_row = []
    row_data = row.findAll("td")
    for idx,data in enumerate(row_data):
        #print(data.text[:-1])
        # Removing , from date
        if idx == 2:
            date = data.text[:-1]
            date = date.split(", ")
            date = " ".join(date)
            current_row.extend([date])
        else:
            current_row.extend([data.text[:-1]])
    rows_data.append(current_row)
#print(rows_data[1]) # Missing Android Name
rows_data[1].insert(0, rows_data[0][0])
#print(rows_data)

# Saving scrapped info into a csv file
with open("android history.csv", "w") as file:
    header_string = ",".join(column_title)
    header_string += "\n"
    file.write(header_string)
    for row in rows_data:
        data = ""
        data = ",".join(row)
        data += "\n"
        file.write(data)
    file.close()
    
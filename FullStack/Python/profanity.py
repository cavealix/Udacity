import urllib

def read_text():
         quotes = open("/Users/Alix/Desktop/profanity.txt")
         contents_of_file = quotes.read()
         print (contents_of_file)
         quotes.close()
         check_profanity(contents_of_file)

def check_profanity(text_to_check):
         connection = urllib.urlopen("http://www.wdyl.com/profanity?q="+text_to_check)
         #read response
         output = connection.read()
         print(output)
         connection.close()

read_text()
                  

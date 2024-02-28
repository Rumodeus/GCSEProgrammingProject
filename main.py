"""
Noel is creating a music quiz game.
The game stores a list of song names and their artist
(e.g. the band or solo artist name). The player needs to
try and guess the song name.
"""

#Obviously need random for this
import random

#ID List
AuthorisedID = ["1001", "7860", "8182", "0912"]

#Declaring variables for later
num = 0
SongArtist = "X"
WrongChoices = 0
LetterCount = 0
CensoredSongName = ""
Score = 0

def randompick():
  global SongArtist
  global num
  global LetterCount
  global CensoredSongName

  #Clearing the variables
  LetterCount = 0
  CensoredSongName = ""
  SongArtist = "X"
  num = 0
  
  #This is required so that a random song is picked. I don't include this in the file handling operation below this as it would not be truly random, with a bias to the first few songs.
  with open("SongList.csv", "r") as SongList:
    choice = random.randint(0, len(SongList.readlines()))
  
  #Using a context handler makes life easier, like I don't have to manually close the file
  #Open SongListExtend.csv for extra songs
  #Please note that the extend is rougher, and I havent checked if its even compatible
  with open("SongList.csv", "r") as SongList:
    #Skip the headerline in the CSV
    next(SongList)
    for line in SongList:
      num += 1
      SongArtist = line.split(",")
      #In essence picks a random song
      if num == choice:
        break

  #Dont like the red underline when it's unbound so
  if SongArtist != "X":
    #Removes the \n from the second value
    SongArtist[1] = SongArtist[1].strip()
  
  #Creating the censored song name to show the player
  for i in range(0, len(SongArtist[0])):
    #If its the first letter, or a new word, it adds the first letter of the word
    if LetterCount == 0 or CensoredSongName[i-1] == " ":
      CensoredSongName += (SongArtist[0])[i]
      LetterCount += 1
      continue
    #If its a special, keep it a special
    if (SongArtist[0][i].isalnum() is False):
      CensoredSongName += (SongArtist[0])[i]
      continue
    #If it isn't a space, add an underscore to indicate a word
    if (SongArtist[0])[i] != " ":
      CensoredSongName += "_"
      continue
    #If it is a space, just add a space
    if (SongArtist[0])[i] == " ":
      CensoredSongName += " "
    LetterCount += 1
    
  
#Simple Login
IDInput = input("Please enter your Player ID: ")
while IDInput not in AuthorisedID:
  print("Wrong ID, please try again.")
  IDInput = input("Please enter your Player ID: ")

print("Please remember that all answers must include the special characters shown in the censored song name!!")
print()

def game():
  #Calling the random song procedure we made earlier
  randompick()

  #Declaring a nested procedure as its the easiest way to repeat the same level
  def ingame():
    global WrongChoices
    global Score
    
    print(CensoredSongName, "by", SongArtist[1])
    guess = input("Enter your guess here: ")
    #Cases for correct answer
    if guess.lower() == SongArtist[0].lower():
      if WrongChoices == 0:
        Score += 3
      if WrongChoices == 1:
        Score += 1
      print(f"Correct! You have {Score} points!")
      print("Starting new game...")
      print()
      WrongChoices = 0
      game()

    #Cases for an incorrect answer
    if guess.lower() != SongArtist[0].lower():
      if WrongChoices == 1:
        print(f"Game over! You got {Score} points!")
        #Updating the leaderboard
        #This took a bit, but I needed to use both read and write.
        with open("Highscores.csv", "r") as HighScore:
          lines = HighScore.readlines()
        #Using w+ truncates the file content upon opening, so this is the only method I could deduce
        with open("Highscores.csv", "w") as HighScore:
          for line in lines:
            if IDInput == line.split(',')[0].strip():
              #If the score is higher only
              if Score > int(line.split(',')[1].strip()):
                HighScore.write(f"{IDInput},{Score}\n")
                continue 
              HighScore.write(line)
            HighScore.write(line)
        exit()
      WrongChoices += 1
      print("Wrong Choice, try again?")
      ingame()
  ingame()
game()

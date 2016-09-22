import media
import  fresh_tomatoes

"""Line wrapping now set at a max of 79 characters according to Python Style
Guidelines"""

#Movie instances 
toy_story = media.Movie(
  "Toy Story", 
  "A story of a boy and his toys that come to life",
  "http://www.gstatic.com/tv/thumb/movieposters/17420/p17420_p_v8_ab.jpg",
  "https://www.youtube.com/watch?v=KYz2wyBy3kc")

avatar=media.Movie(
  "Avatar", 
  "A marine on an alien planet",
  "http://moviecultists.com/wp-content/uploads/2009/11/avatar-poster.jpg",
  "https://www.youtube.com/watch?v=5PSNL1qE6VY")

batman = media.Movie(
  "Batman", 
  "Bruce Wayne becomes the greatest hero of all time",
  "http://www.gstatic.com/tv/thumb/movieposters/35903/p35903_p_v8_ae.jpg",
  "https://www.youtube.com/watch?v=vak9ZLfhGnQ")

prestige = media.Movie(
  "The Prestige",
  "An illusion gone horribly wrong pits two 19th-century magicians,\
    Alfred Borden (Christian Bale) and Rupert Angier (Hugh Jackman),\
    against each other in a bitter battle for supremacy.",
  "http://www.gstatic.com/tv/thumb/movieposters/161581/p161581_p_v8_aa.jpg",
  "https://www.youtube.com/watch?v=ijXruSzfGEc")

cloudy = media.Movie(
  "Cloudy with a Chance of Meatballs", 
  "When hard times hit Swallow Falls, its townspeople can only afford to eat\
    sardines.",
  "http://www.gstatic.com/tv/thumb/movieposters/197825/p197825_p_v8_ae.jpg",
  "https://www.youtube.com/watch?v=Ytw30l-T2WI")

mad_max = media.Movie(
  "Mad Max Fury Road", 
  "Years after the collapse of civilization, the tyrannical Immortan Joe\
    enslaves apocalypse survivors inside the desert fortress the Citadel.",            
  "http://posterposse.com/wp-content/uploads/2015/03/Mad-Max-Fury-Road1.jpg",            
  "https://www.youtube.com/watch?v=5wHRFvJNCW4")

#package movies in array to feed to fresh_tomatoes
movies = [toy_story, avatar, batman, prestige, cloudy, mad_max]

#generate movie page
fresh_tomatoes.open_movies_page(movies)


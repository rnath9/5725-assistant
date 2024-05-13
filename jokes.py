import random
jokes = ["Why did the rabbit go to the salon? It was having a bad hare day!",
         "What kind of felines can bowl? Alley cats!",
         "Where do penguins go to vote? The North Poll!",
         "Why aren't lobsters generous? Because they're shellfish!",
         "How do mice floss their teeth? With string cheese!",
         "What do you call a happy cowboy? A jolly rancher!",
         "What kind of bagel can travel? A plain bagel!",
         "I've never been a fan of facial hair. But now it's starting to grow on me.",
         "Did you hear about the guy who afraid of hurdles? He got over it.",
         "Why did the computer catch a cold? It left a window open!"]

def get_joke():
    index = random.randint(0,len(jokes)-1)
    return jokes[index]

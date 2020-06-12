# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Citlali Trigos
# Collaborators:
# Date: 6/10/20

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        if 'description' not in entry: description = ''
        else: description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #    pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''
        Initializes a NewsStory object
                
        guid: globally unique identifier (GUID)
        title: a string
        description: a string
        link: string link to more content 
        pubdate - a datetime of published time

        A NewsStory object has 5 attributes:
            self.message_text (string, determined by input text)
            self.guid (string, determined by input text)
            self.title (string, determined by input text)
            self.description (string, determined by input text)
            self.link (string, determined by input text)
            self.pubdate (dateTime, determined by input text)
        '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self): 
        return self.title
    def get_description(self):
        return self.description
    def get_link(self): 
        return self.link
    def get_pubdate(self): 
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, trigger_phrase):
        '''
        Initializes an Trigger object

        story (object): a news story object
        trigger_phrase (string): the phrase we want to find 

        An PhraseTrigger object inherits from Trigger and has one attributes:
            self.story (object, determined by input text)
            
        '''
        Trigger.__init__(self)
        self.trigger_phrase = trigger_phrase.lower()
    def get_trigger_phrase(self):
        return self.trigger_phrase
    def is_phrase_in(self, text):
        '''
        Returns True if the whole trigger is present in text, False otherwise

        For example, a phrase trigger with the phrase "purple cow" should fire on:
            'PURPLE COW'
            'The purple cow is soft and cuddly.'
            'The farmer owns a really PURPLE cow.'
            'Purple!!! Cow!!!'
            ' purple@#$%cow'
            'Did you see a purple cow?'

        But not on: 
            'Purple cows are cool!'
            'The purple blob over there is a cow.'
            'How now brown cow.'
            'Cow!!! Purple!!!'
            'purplecowpurplecowpurplecow'
        '''
        # cleans the input text and the trigger phrase
        clean_text = text.lower()
        trigger_phrase = self.get_trigger_phrase().split(' ')
        for punctuation in string.punctuation:
            clean_text = clean_text.replace(punctuation, ' ')
        phrase_list = clean_text.split(' ')
        new_list = []
        for i in range(len(phrase_list)):
            if phrase_list[i] != '': new_list.append(phrase_list[i].replace(' ', ''))
        clean_text = ' '.join(new_list)
        trigger_length = len(trigger_phrase)
        # checks and sees if there is overlap
        for i in range(len(new_list)):
            if i+ trigger_length-1 > len(new_list): 
                return False 
            if new_list[i] in trigger_phrase:
                if new_list[i:i+trigger_length] == trigger_phrase: return True
        return False




# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, trigger_phrase):
        '''
        Initializes an Trigger object

        story (object): a news story object
        trigger_phrase (string): the phrase we want to find 

        An PhraseTrigger object inherits from Trigger and has one attributes:
            self.story (object, determined by input text)
            
        '''
        PhraseTrigger.__init__(self, trigger_phrase)
    def get_story_title(self, story):
        return NewsStory(story.guid, story.title, story.description, story.link, story.pubdate).get_title()
    def evaluate(self, story):
        '''
        Returns true if the given trigger exists in the story's title else False
        '''
        title = self.get_story_title(story)
        return self.is_phrase_in(title)

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, trigger_phrase):
        '''
        Initializes an Trigger object

        story (object): a news story object
        trigger_phrase (string): the phrase we want to find 

        An PhraseTrigger object inherits from Trigger and has one attributes:
            self.story (object, determined by input text)
            
        '''
        PhraseTrigger.__init__(self, trigger_phrase)
    def get_story_description(self, story):
        return NewsStory(story.guid, story.title, story.description, story.link, story.pubdate).get_description()
    def evaluate(self, story):
        '''
        Returns true if the given trigger exists in the story's description else False
        '''
        description = self.get_story_description(story)
        return self.is_phrase_in(description)

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, date_time):
        '''
        Initializes an Trigger object

        date_time (string): the phrase we want to find 

        An TimeTrigger object inherits from Trigger and has one attributes:
            self.date_time (dateTime, determined by input text, saved as a string)
            
        '''
        Trigger.__init__(self)
        self.time_string = str(date_time)
    def get_time_string(self):
        return self.time_string
    def get_story_pubdate(self, story):
        pubdate =  NewsStory(story.guid, story.title, story.description, story.link, story.pubdate).get_pubdate()
        return pubdate if len(str(pubdate))!=25 else datetime.strptime(str(pubdate)[:-6], "%Y-%m-%d %H:%M:%S")
    def get_time_string_as_date(self):
        return  datetime.strptime(self.get_time_string(), "%d %b %Y %H:%M:%S")

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, date_time):
        '''
        Initializes an Trigger object

        date_time (string): the phrase we want to find 

        An TimeTrigger object inherits from Trigger and has one attributes:
            self.date_time (dateTime, determined by input text, saved as a string)
            
        '''
        TimeTrigger.__init__(self, date_time)
    def evaluate(self, story):
        '''
        Returns true if the story was created strictly before the given trigger time else False
        '''
        return self.get_story_pubdate(story) < self.get_time_string_as_date()

class AfterTrigger(TimeTrigger):
    def __init__(self, date_time):
        '''
        Initializes an Trigger object

        date_time (string): the phrase we want to find 

        An TimeTrigger object inherits from Trigger and has one attributes:
            self.date_time (dateTime, determined by input text, saved as a string)
            
        '''
        TimeTrigger.__init__(self, date_time)
    def evaluate(self, story):
        '''
        Returns true if the story was created strictly after the given trigger time else False
        '''
        return self.get_story_pubdate(story) > self.get_time_string_as_date()


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        '''
        Initializes an Trigger object

        trigger (trigger object): takes in a trigger object and returns the NOT of it 
        '''
        Trigger.__init__(self)
        self.trigger = trigger
    def get_trigger(self):
        return self.trigger
    def evaluate(self, story):
        '''
        Returns true if the given trigger evaluates False, else False
        '''
        newsStory = NewsStory(story.guid, story.title, story.description, story.link, story.pubdate)
        trigger = self.get_trigger()
        return not trigger.evaluate(newsStory)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        '''
        Initializes an Trigger object

        first_trigger (trigger object)
        second_trigger (trigger object)

        '''
        Trigger.__init__(self)
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger
    def get_first_trigger(self):
        return self.first_trigger
    def get_second_trigger(self):
        return self.second_trigger
    def evaluate(self, story):
        '''
        Returns true only if both triggers fire, else false
        '''
        newsStory = NewsStory(story.guid, story.title, story.description, story.link, story.pubdate)
        first_trigger = self.get_first_trigger()
        second_trigger =self.get_second_trigger()
        return first_trigger.evaluate(newsStory) and second_trigger.evaluate(newsStory)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        '''
        Initializes an Trigger object

        first_trigger (trigger object)
        second_trigger (trigger object)

        '''
        Trigger.__init__(self)
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger
    def get_first_trigger(self):
        return self.first_trigger
    def get_second_trigger(self):
        return self.second_trigger
    def evaluate(self, story):
        '''
        Returns true if one or both triggers fire, else false
        '''
        newsStory = NewsStory(story.guid, story.title, story.description, story.link, story.pubdate)
        first_trigger = self.get_first_trigger()
        second_trigger =self.get_second_trigger()
        return first_trigger.evaluate(newsStory) or second_trigger.evaluate(newsStory)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    firing_stories= []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story): 
                firing_stories.append(story)
                break
    return firing_stories


#======================
# User-Specified Triggers
#======================
# Problem 11

# TODO: Problem 11
# line is the list of lines that you need to parse and for which you need
# to build triggers
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    triggers = {}
    needed=[]
    for item in lines:
        split_list = item.split(',')
        name = split_list[1]
        if split_list[0] =='ADD': needed.extend(split_list[1:])
        elif name =='TITLE': triggers[split_list[0]] = TitleTrigger(split_list[2])
        elif name =='DESCRIPTION': triggers[split_list[0]] = DescriptionTrigger(split_list[2])
        elif name == 'AFTER': triggers[split_list[0]] = AfterTrigger(split_list[2])
        elif name == 'NOT': triggers[split_list[0]] = NotTrigger(split_list[2])
        elif name == 'AND': 
            trigger_one = triggers[split_list[2]]
            trigger_two = triggers[split_list[3]]
            triggers[split_list[0]] = AndTrigger(trigger_one, trigger_two)
        elif name == 'OR': 
            trigger_one = triggers[split_list[2]]
            trigger_two = triggers[split_list[3]]
            triggers[split_list[0]] = OrTrigger(trigger_one, trigger_two)

    output_list = [triggers[trigger] for trigger in needed]
    return output_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()


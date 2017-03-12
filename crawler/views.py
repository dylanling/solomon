from django.shortcuts import render
from django.http import HttpResponse

from fiction import StoryData, User

from .forms import AuthorForm
from .models import Story, Author

def index(request):
    return HttpResponse("empty page")

def crawl_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            crawl_via_author_id(form.cleaned_data['author_id'])
            return HttpResponse("thx :)") 
        else:
            return HttpResponse("NOT valid >:(") 
    else:
        form = AuthorForm()
        return render(request, 'crawl_author.html', {'form': form})

def crawl_via_author_id(author_id, depth=1):
    user = User(id=author_id)

    story_ids = user.get_story_ids()
    favorite_story_ids = user.get_favorite_story_ids()
    favorite_author_ids = user.get_favorite_author_ids()

    author = get_or_create_author_from_id(author_id, user=user)

    for story_id in story_ids:
        get_or_create_story_from_id(story_id, author=author)

    favorite_stories = map(lambda x: get_or_create_story_from_id(x), favorite_story_ids)

    for favorite_story in favorite_stories:
        author.favorite_stories.add(favorite_story)

    for favorite_author_id in favorite_author_ids:
        favorite_author = get_or_create_author_from_id(favorite_author_id, user=user)
        author.favorite_authors.add(favorite_author)

    author.save()

    if depth <= 0:
        return        

    for story in favorite_stories:
        print 'beginning recrawl on favorites'
        crawl_via_author_id(story.author_id, depth - 1)


def get_or_create_author_from_id(authorid, user=None):
    if Author.objects.filter(author_id=authorid).exists():
        author =  Author.objects.get(author_id=authorid)
        print author.name.encode('utf-8') + ' already exists, skipping network call.'
        return author
    if user is None:
        user = User(id=authorid)

    author = Author(author_id=user.userid, name=user.username)
    author.save()
    print author.name.encode('utf-8') + ' created.'
    return author

def get_or_create_story_from_id(storyid, author=None, storydata=None):
    if Story.objects.filter(story_id=storyid).exists():
        story = Story.objects.get(story_id=storyid)
        print story.title.encode('utf-8') + ' already exists, skipping network call.'
        return story

    if storydata is None:
        storydata = StoryData(id=storyid)

    if author is None and Author.objects.filter(author_id=storydata.author_id).exists():
        author = Author.objects.get(author_id=storydata.author_id)
    elif author is None:
        author = get_or_create_author_from_id(storydata.author_id)
    genres = tuple([storydata.genre[i] if len(storydata.genre) > i else None for i in range(0,2)])
    characters = tuple([storydata.characters[i] if len(storydata.characters) > i else None for i in range(0,4)])
    story = Story(story_id=storydata.id, 
                 author=author,
                 title=storydata.title,
                 published=storydata.date_published,
                 updated=storydata.date_updated,
                 chapters=storydata.chapter_count,
                 rated=storydata.rated,
                 language=storydata.language,
                 genre1=genres[0],
                 genre2=genres[1],
                 character1=characters[0],
                 character2=characters[1],
                 character3=characters[2],
                 character4=characters[3],
                 reviews=storydata.reviews
    )
    story.save()
    print story.title.encode('utf-8') + ' created.'
    return story
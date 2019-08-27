from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import Review
from ..login.models import User
from django.contrib import messages
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bsoup
import re

def index(request):
    
    this_user = User.objects.get(id=request.session['id'])
    site_links = []
    site_headlines = []

    tag_remove = re.compile(r'<[^>]+>')
    review_dict={}
    review_details_dict={}

    if request.session['error'] == "":
    
        link = request.session['url']
        # Need to make this dynamic
        site_link = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        # site_link = Request('https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183', headers={'User-Agent': 'Mozilla/5.0'})
        
        uClient = urlopen(site_link)
        #BeautifulSoup Magic
        soup = bsoup( uClient, 'html.parser' )
        r_content = ""
        r_content += "<hr style='background-color:white'>"
        review_total = soup.findAll('div',attrs={"class":"mainReviews"})
        
        for each_review in review_total:
            # print ('==============================')
            # r_content += "<hr style='background-color:white'>"            
            rating = each_review.find('div',attrs={"class":"numRec"}).text
            # print (rating)
            r_content += rating + "<br>"
            
            title = each_review.find('p',attrs={"class":"reviewTitle"}).text
            # print (title)
            r_content += title + "<br>"
            
            content = each_review.find('p',attrs={"class":"reviewText"}).text
            # print (content)
            r_content += content + "<br>"
            
            auther = each_review.find('p',attrs={"class":"consumerName"}).text
            # print (auther)
            r_content += auther + "<br>"
            
            review_date = each_review.find('p',attrs={"class":"consumerReviewDate"}).text
            # print (review_date)
            r_content += review_date + "<br>"
            
            likes = each_review.find('span',attrs={"class":"likes"}).number
            # print (likes)
            r_content += str(likes) + "<br>"
            
            dislikes = each_review.find('span',attrs={"class":"dislikes"}).number
            # print (dislikes)
            r_content += str(dislikes) + "<br>"
            
            r_content += "<hr style='background-color:white'>"

            # Add to DB
            if (len(r_content)) > 10:
                Review.objects.create(
                users=User.objects.get(id=int(request.session['id'])),
                site=link,
                rating=rating,
                title=title,
                content=content,
                auther=auther,
                review_date=review_date,
                likes=str(likes),
                dislikes=str(dislikes))

            # print ('#' , len(r_content), '#')
        context={'review_total': r_content}
    
        return render(request, 'tracker/dashboard.html', context)
    else:
        return render(request, 'tracker/dashboard.html')

def create_list(request):
    if request.POST :
        request.session['url'] = request.POST['url']
        request.session['error'] = ""

        real_url = request.session['url']
        try:
            with closing(get(real_url, stream=True)) as resp:
                if is_good_response(resp):
                    request.session['error'] = ""
                    return index(request)
                else:
                    request.session['error'] = "please enter a valid url"
                    return render(request, 'tracker/dashboard.html')

        except RequestException:
            request.session['error'] = "please enter a valid url"
            return index(request)
    else:
        return render(request, 'tracker/dashboard.html')

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


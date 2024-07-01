#importing important libraries
import csv
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import mysql.connector


# Function declarations

# Function to extract Social Media links present in the websites
def extractSocialMediaLinks(url):
    
    socialMediaDomains = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com', 'youtube.com', 'pinterest.com']
    socialLinks = []

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for aTag in soup.find_all('a', href=True):
            href = aTag['href']
            if any(domain in href for domain in socialMediaDomains):
                socialLinks.append(href)

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return socialLinks

# Extract the Tech Stack used in websites
def extractTechStack(url):
    techStack = {}

    # Create Dictionary for Technologies which are mostly used in websites
    techKeywords = {
        'WordPress': 'wp-content',
        'Magento': 'magento',
        'Shopify': 'shopify',
        'Drupal': 'drupal',
        'Joomla': 'joomla',
        'Wix': 'wix',
        'Django': 'django',
        'Ruby on Rails': 'rails',
        'ASP.NET': 'asp.net',
        'Laravel': 'laravel',
        'Spring': 'spring',
        'Express': 'express',
        'jQuery': 'jquery',
        'Bootstrap': 'bootstrap',
        'React': 'react',
        'Angular': 'angular',
        'Vue.js': 'vue',
        'Ember.js': 'ember',
        'Backbone.js': 'backbone',
    }

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check script tags 
        for script in soup.find_all('script', src=True):
            src = script.get('src', '')
            for tech, keyword in techKeywords.items():
                if keyword in src and tech not in techStack:
                    techStack[tech] = True

        # Check for the keywords in the HTML code
        htmlContent = response.text.lower()
        for tech, keyword in techKeywords.items():
            if keyword in htmlContent and tech not in techStack:
                techStack[tech] = True

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return techStack


# Extract the Meta Title from the webpage and returns the meta title string
def extractMetaTitle(url):    
    metaTitle = None

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        titleTag = soup.find('title')
        if titleTag:
            metaTitle = titleTag.text.strip()

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return metaTitle


# Extract the Meta Description of the webpage and returns the Meta Description String
def extractMetaDescription(url):    
    metaDescription = None

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        metaDescriptionTag = soup.find('meta', attrs={'name': 'description'})
        if metaDescriptionTag:
            metaDescription = metaDescriptionTag.get('content', '').strip()

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return metaDescription


# Extract the payment gateways (such as Paypal, Stripe, etc) that are used on the homepage of the website
def extractPaymentGateways(url):
    paymentGateways = []

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

       # Keywords for Payment Method
        paymentKeywords = {
            'PayPal': r'paypal',
            'Stripe': r'stripe',
            'Razorpay': r'razorpay',
            'Square': r'square',
            'Authorize.Net': r'authorize\.net',
            'Braintree': r'braintree',
            'Venmo': r'venmo',
            'Apple Pay': r'apple\s*pay',
            'Google Pay': r'google\s*pay',
            'Amazon Pay': r'amazon\s*pay',
            'Bitcoin': r'bitcoin',
            'Ethereum': r'ethereum',
           
        }

        
        textContent = soup.get_text().lower()

        for gateway, pattern in paymentKeywords.items():
            if re.search(pattern, textContent):
                paymentGateways.append(gateway)

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    # Returns a list of payment gateways found.
    return paymentGateways


# Detect the Website Language i.e. English, Hindi etc and returns LanguageCode 
def detectWebsiteLanguage(url):    
    languageCode = None

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        html_tag = soup.find('html')
        if html_tag and 'lang' in html_tag.attrs:
            languageCode = html_tag['lang'].strip().lower()

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return languageCode


# Detect the Category of website (Sports, News, Tech etc)
def detectWebsiteCategory(url):    
    category = 'Uncategorized'

    try:
        response = requests.get(url)
        htmlContent = response.text.lower()

        # Define categories and their associated keywords or entity types
        categories = {
            'News': ['news', 'breaking news', 'headlines', 'current affairs'],
            'Sports': ['sports', 'football', 'soccer', 'basketball', 'tennis', 'cricket'],
            'Technology': ['technology', 'tech', 'gadgets', 'innovation', 'software', 'hardware'],
            'Business': ['business', 'finance', 'economy', 'stocks', 'investing'],
            'Health': ['health', 'medical', 'wellness', 'fitness', 'nutrition'],
            'Education': ['education', 'learning', 'school', 'university', 'courses', 'study'],
            'Entertainment': ['entertainment', 'movies', 'music', 'celebrities', 'gaming'],
            'Shopping': ['shopping', 'store', 'online shop', 'ecommerce', 'buy', 'shop'],
            'Travel': ['travel', 'tourism', 'vacation', 'destinations', 'flights', 'hotels'],
            'Food': ['food', 'recipes', 'cooking', 'restaurants', 'cuisine'],
            'Art & Culture': ['art', 'culture', 'history', 'museum', 'literature'],
            'Home & Garden': ['home', 'garden', 'decor', 'interior', 'diy'],
            'Automotive': ['automotive', 'cars', 'vehicles', 'auto', 'motorcycles'],
            'Science': ['science', 'research', 'discoveries', 'technology', 'innovation'],
            'Social Media': ['social media', 'networking', 'platform', 'community', 'connect'],
            'Pets': ['pets', 'animals', 'dogs', 'cats', 'pet care']
            
        }

        # Check for categories based on keywords in document text
        for cat, keywords in categories.items():
            for keyword in keywords:
                if keyword in htmlContent:
                    category = cat
                    break
            if category != 'Uncategorized':
                break

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return category



# Insert the data into MySQL Database by using mysql connecter
def insertWebsiteData(url, social_media_links, tech_stack, meta_title, meta_description, payment_gateways, website_language, website_category):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="scrapper"
        )

        cursor = connection.cursor()

        sql = "INSERT INTO websites (url, social_media_links, tech_stack, meta_title, meta_description, payment_gateways, website_language, website_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (url, ', '.join(social_media_links), ', '.join(tech_stack.keys()), meta_title, meta_description, ', '.join(payment_gateways), website_language, website_category)

        cursor.execute(sql, val)

        connection.commit()

        print(f"Data inserted successfully for {url}")

    except mysql.connector.Error as error:
        print(f"Error inserting data for {url}: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
# List of websites to analyze
    websites = [
    
        'https://www.nytimes.com',
        'https://www.bbc.com',
        'https://www.forbes.com',
        'https://www.wsj.com',
        'https://www.bloomberg.com',
        'https://edition.cnn.com',
        'https://www.theguardian.com',
        'https://www.huffpost.com',
        'https://www.npr.org',
        'https://www.reuters.com',
    
    
        'https://www.hindustantimes.com',
    
        'https://www.usatoday.com',
        'https://www.cnn.com',
        'https://www.bbc.co.uk',
        'https://www.latimes.com',
        'https://www.chicagotribune.com',
        'https://www.thetimes.co.uk',
        'https://www.telegraph.co.uk',
        'https://www.dailymail.co.uk',
        'https://www.abc.net.au',
        'https://www.nzherald.co.nz',
    
    
        'https://www.elpais.com',
        'https://www.abc.es',
        'https://www.elmundo.es',
        'https://www.20minutos.es',
        'https://www.lavanguardia.com',
        'https://www.marca.com',
        'https://www.eldiario.es',
        'https://www.elconfidencial.com',
        'https://www.eldiario.es',
        'https://www.elmundo.es',
    
    
        'https://www.paypal.com',
        'https://www.stripe.com',
        'https://www.razorpay.com',
        'https://www.square.com',
        'https://www.authorize.net',
        'https://www.braintree.com',
        'https://www.venmo.com',
        'https://pay.amazon.com',
        'https://www.bitcoin.org',
        'https://www.ethereum.org',
        
        
        'https://www.webmd.com',
        'https://www.mayoclinic.org',
        'https://www.medicalnewstoday.com',
        'https://www.nih.gov',
        'https://www.nhs.uk',
        'https://www.cdc.gov',
        'https://www.bmj.com',
        'https://www.npr.org/sections/health-shots',
        
    
        'https://www.techcrunch.com',
        'https://www.theverge.com',
        'https://www.engadget.com',
        'https://www.mashable.com',
        'https://www.gizmodo.com',
        'https://www.wired.com',
        'https://www.lifehacker.com',
        'https://www.businessinsider.com',
        'https://www.economist.com',
        'https://www.ft.com',
        
        
        'https://www.espn.com',
        'https://www.cbssports.com',
        'https://www.sportingnews.com',
        'https://www.nbcsports.com',
        'https://www.skysports.com',
        'https://www.foxsports.com',
        'https://www.bleacherreport.com',
        'https://www.si.com',
        'https://www.goal.com',
        'https://www.sbnation.com',
        
        
        'https://www.lemonde.fr',
        'https://www.lefigaro.fr',
        'https://www.liberation.fr',
        'https://www.lequipe.fr',
        'https://www.20minutes.fr',
        'https://www.francetvinfo.fr',
        'https://www.rtl.fr',
        'https://www.ouest-france.fr',
        'https://www.lapresse.ca',
        'https://www.cnews.fr',
        
        
        
        'https://www.twitter.com',
        'https://www.linkedin.com',
        'https://www.instagram.com',
        'https://www.youtube.com',
        'https://www.pinterest.com',
        'https://www.snapchat.com',
        'https://www.tiktok.com',
        'https://www.reddit.com',
        
        
        
        'https://www.amazon.com',
        'https://www.ebay.com',
        'https://www.walmart.com',
        'https://www.target.com',
        'https://www.bestbuy.com',
        'https://www.alibaba.com',
        'https://www.flipkart.com',
        'https://www.shopify.com',
        'https://www.newegg.com',
        'https://www.overstock.com'
        'https://www.geeksforgeeks.org'
        'https://github.com'
        'https://www.triumphmotorcycles.in'
        'https://www.ufc.com'
        'https://www.onefc.com'
        'https://www.sportskeeda.com'
    ]   



    for url in tqdm(websites):
        print(f"Extracting information from: {url}")

        # Saving Social Media Links of Website
        social_media_links = extractSocialMediaLinks(url)
        print(f"Social Media Links: {social_media_links}")

        # Saving Tech Stack of Website
        tech_stack = extractTechStack(url)
        print(f"Tech Stack: {tech_stack}")

        # Meta Title of Website
        meta_title = extractMetaTitle(url)
        print(f"Meta Title: {meta_title}")

        # Meta Description of Website
        meta_description = extractMetaDescription(url)
        print(f"Meta Description: {meta_description}")

        # Payment Gateways used in Website
        payment_gateways = extractPaymentGateways(url)
        print(f"Payment Gateways: {payment_gateways}")

        # Website Language used in Webpage
        website_language = detectWebsiteLanguage(url)
        print(f"Website Language: {website_language}")

        # Website Category
        website_category = detectWebsiteCategory(url)
        print(f"Website Category: {website_category}")

        # Insert data into MySQL database 
        insertWebsiteData(url, social_media_links, tech_stack, meta_title, meta_description, payment_gateways, website_language, website_category)

        # Separator for readability of Extracted Data
        print("-" * 50)  #
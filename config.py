apikey = "84f75d747e4f43e48803000bc81dc930"
database = "./data/source.json"
datefile = "./utils/data.json"
tweet_datefile = "./analysis/tweet_date.json"
news_datefile = "./analysis/news_date.json"
newsquerydb = "./data/query_news.plk"
tweetquerydb = "./data/query_tweets.plk"
wordquerydb = "./data/worddb.json"
xml_data = "./analysis/data/raw.xml"
firebaseConfig = {
    "apiKey": "AIzaSyD0e6NAyxUI5Z8rs1j2ahwCwpG2HptFg-o",
    "authDomain": "coronow-d737d.firebaseapp.com",
    "databaseURL": "https://coronow-d737d.firebaseio.com",
    "projectId": "coronow-d737d",
    "storageBucket": "coronow-d737d.appspot.com",
    "messagingSenderId": "787414217798",
    "appId": "1:787414217798:web:5a013427d62e4425da4647",
    "measurementId": "G-X4NZ3H0HDS"
}
keywords = {"Coronavirus", "Koronavirus", "Corona", "CDC", "Wuhancoronavirus", "Wuhanlockdown", "Ncov",
            "Wuhan", "N95", "Kungflu", "Epidemic", "Outbreak", "Sinophobia", "China", "Covid-19 ",
            "Corona virus", "Covid", "Covid19", "Sars-cov-2", "COVID–19", "COVD", "Pandemic"}

mapping = {
    "Coronavirus": ["coronavirus", "coronvirus", "corona", "virus"],
    "Koronavirus": ["koronavirus", "koronvirus", "korona", "virus"],
    "Corona": ["corona"],
    "CDC": ["cdc"],
    "Wuhancoronavirus": ["wuhan", "wuhan virus", "wuhan coronavirus"],
    "Wuhanlockdown": ["wuhan", "lockdown"],
    "Ncov": ["ncov", "ncov19", "ncov-19"],
    "Wuhan": ["wuhan"],
    "N95": ["n95", "mask"],
    "Kungflu": ["kungflu", "kung", "flu"],
    "Epidemic": ["epidemic"],
    "Outbreak": ["outbreak"],
    "Sinophobia": ["sinophobia"],
    "China": ["china"],
    "Covid-19 ": ["covid-19", "covid19", "covid"],
    "Corona virus": ["corona virus", "corona", "virus"],
    "Covid": ["covid"],
    "Covid19": ["covid19"],
    "Sars-cov-2": ["sars", "cov-2", "cov"],
    "COVID-19": ["covid-19"],
    "COVD": ["covd"],
    "Pandemic": ["pandemic"]
}

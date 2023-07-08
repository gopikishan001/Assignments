import requests
from pytube import YouTube, Channel
from bs4 import BeautifulSoup
import csv

def get_youtube_data(query, num_results):
    base_url = f"https://www.google.com/search?q=site%3Ayoutube.com+{query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    page = 0
    results = []
    link_cnt = 0
    warning_cnt = 0

    print("\nExtracting links \n")

    while(link_cnt < num_results) :
        url = f"{base_url}&start={page}"
        response = requests.get(url , headers = headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results += soup.find_all('a')
        page += 1

        if len(results) - link_cnt == 3 :
            link = results[-2].get('href') 

            if "policies" in link :
                print("\nGoogle polices warning \nWarinig count = ", warning_cnt + 1)
                warning_cnt += 1
                results = results[:-3]

            if warning_cnt > 2 : break

        link_cnt = len(results)
        print("page = ", page , " total links found = " , len(results))

    channels = []
    warning_cnt = 0

    print("\n\nExtracting YouTube links\n")
    
    for i in range(len(results)):

        print("progress % = " , str(int((i+1)*100/len(results))) , end = "\r")

        try :
            href = str(results[i].get('href'))
            if href.startswith('https://www.youtube.com/'):
                if "/c/" in href or "/channel/" in href:
                    if "/community" in href :
                        href = href.split("/community")[0]
                    channel_name = Channel(href).channel_name
                    channels.append([channel_name , href, href])

                elif "watch" in href:
                    channel_link = "https://www.youtube.com/channel/" + YouTube(href).channel_id 
                    channel_name = Channel(channel_link).channel_name
                    channels.append([channel_name , channel_link, href])

                elif "post" in href:
                    response = requests.get(href)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    result = soup.find('link', attrs={'rel': 'canonical'})
                    
                    if result :
                        channel_link = result.get('href')
                        channel_name = Channel(channel_link).channel_name
                        channels.append([channel_name , channel_link , href])
                
                elif "hashtag" in href:
                    continue
                else : print("\nexeption link : " , href)

        except Exception as e:
            print(f"An error occurred: {str(e)} \nError count = {warning_cnt}")
            warning_cnt += 1
            if warning_cnt > 2 : break

    print("\nTotal YouTube Channels Extracted = ", str(len(channels)))
    return channels

def save_to_csv(channels):
    with open('youtube_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel name' , 'Channel link' , "Extracted from"])
        for channel in channels:
            writer.writerow([channel[0] , channel[1] , channel[2]])

    print("\nsaved as CSV")

if __name__ == '__main__':

    query = 'openinapp.co'
    num_results = 10000
    channels = get_youtube_data(query, num_results)
    if channels :
        save_to_csv(channels)

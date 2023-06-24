from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from mplsoccer import Radar,FontManager,grid
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
import base64
from players import players_dict
from players import teams_dict
import pickle

def analyze_team(team_ext,title):
    url = 'https://fbref.com/en/squads/' + team_ext
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    info_div = soup.find('div', {'id': 'info'})
    p_tags = info_div.find_all('p')
    points_per_game = (float((p_tags[0].text)[41:45]))
    g_scored_per_game = (float((p_tags[2].text)[11:15]))
    g_conc_per_game = (float((p_tags[2].text)[55:59]))
    xG = (float((p_tags[3].text)[4:8]))
    xGC = (float((p_tags[3].text)[24:28]))
    values = [points_per_game,g_scored_per_game,g_conc_per_game,xG,xGC]
    params = ["points_per_game","g_scored_per_game","g_conc_per_game","xG","xGC"]

    #CHANGE
    low  = [0.0,0.0,0.0,0.0,0.0]
    high = [10.0,5.0,5.0,50.0,50.0]
    radar = Radar(params,low,high,num_rings=4,ring_width=1,center_circle_radius=1)
    fig, ax = radar.setup_axis()
    ax.set_title("Team: " + title, fontsize=60, fontweight='bold', fontstyle='italic')

    rings_inner = radar.draw_circles(ax=ax, facecolor='#ffb2b2', edgecolor='#fc5f5f')
    radar_output = radar.draw_radar(values, ax=ax)  # draw the radar
    radar_poly, rings_outer, vertices = radar_output
    range_labels = radar.draw_range_labels(ax=ax, fontsize=15)  # draw the range labels
    param_labels = radar.draw_param_labels(ax=ax, fontsize=15)  # draw the param labels
    plt.savefig('img.png') # save the image
    image = Image.open('img.png')
    image = image.convert('RGB')
    image.save('img.jpg','JPEG')
    image_path = 'img.jpg' # convert the image into numpy array
    img = Image.open(image_path)
    img_arr = np.array(img) 
    os.remove('img.jpg') # delete the image
    return Image.fromarray(img_arr)

    

def analyze_player(name_ext,player):

    base_url = 'https://fbref.com/en/players/'
    url = base_url + name_ext
    standard_ext = '#stats_standard_dom_lg'
    standard_url = url + standard_ext # get the url
    standard_response = requests.get(standard_url) # get the response
    standard_html_content = standard_response.content; # get the html content
    standard_soup = BeautifulSoup(standard_response.content, 'html.parser') # beautify them
    standard_tfoot = list(standard_soup.find("tfoot"))  # extract the footer values
    std_data_list = standard_tfoot[0].find_all("td") # extract the td list
    values = [float(std_data_list[7].text),float(std_data_list[8].text),float(std_data_list[9].text),float(std_data_list[14].text),float(std_data_list[15].text),float(std_data_list[16].text),float(std_data_list[18].text),float(std_data_list[20].text),float(std_data_list[21].text)]
    params = ["Matches","Goals","Assists","Yellow Cards","Red Cards","Expected Goals","expected Assist Goals","Progressive Carries","Progressive Goals"]
    
    #CHANGE

    low = []
    high = []
    for i in range(len(values)):
        low.append(0.0)
        high.append(700.0)

    radar = Radar(params,low,high,num_rings=4,ring_width=1,center_circle_radius=2)
    fig, ax = radar.setup_axis()
    ax.set_title("Player: " + player, fontsize=60, fontweight='bold', fontstyle='italic')
    rings_inner = radar.draw_circles(ax=ax, facecolor='#FFB2B2', edgecolor='#FC5F5F', alpha=0.5)
    radar_output = radar.draw_radar(values, ax=ax,kwargs_radar={'facecolor': '#FF0000', 'alpha': 0.5},kwargs_rings={'facecolor': '#800000', 'alpha': 0.5})  # draw the radar
    radar_poly, rings_outer, vertices = radar_output
    range_labels = radar.draw_range_labels(ax=ax, fontsize=20)  # draw the range labels
    param_labels = radar.draw_param_labels(ax=ax, fontsize=20)  # draw the param labels
    
    plt.savefig('img.png') # save the image
    image = Image.open('img.png')
    image = image.convert('RGB')
    image.save('img.jpg','JPEG')
    image_path = 'img.jpg' # convert the image into numpy array
    img = Image.open(image_path)
    img_arr = np.array(img) 
    os.remove('img.jpg') # delete the image
    return Image.fromarray(img_arr)

def convert_to_lowercase(arr):
        return list(map(str.lower, arr))

def compare_players(name1_ext,name2_ext,player1,player2):

    base_url = 'https://fbref.com/en/players/'
    params = ["Matches","Goals","Assists","Yellow Cards","Red Cards","Expected Goals","expected Assist Goals","Progressive Carries","Progressive Goals"]

    url = base_url + name1_ext
    standard_ext = '#stats_standard_dom_lg'
    standard_url = url + standard_ext # get the url
    standard_response = requests.get(standard_url) # get the response
    standard_html_content = standard_response.content; # get the html content
    standard_soup = BeautifulSoup(standard_response.content, 'html.parser') # beautify them
    standard_tfoot = list(standard_soup.find("tfoot"))  # extract the footer values
    std_data_list = standard_tfoot[0].find_all("td") # extract the td list
    values1 = [float(std_data_list[7].text),float(std_data_list[8].text),float(std_data_list[9].text),float(std_data_list[14].text),float(std_data_list[15].text),float(std_data_list[16].text),float(std_data_list[18].text),float(std_data_list[20].text),float(std_data_list[21].text)]

    url = base_url + name2_ext
    standard_ext = '#stats_standard_dom_lg'
    standard_url = url + standard_ext # get the url
    standard_response = requests.get(standard_url) # get the response
    standard_html_content = standard_response.content; # get the html content
    standard_soup = BeautifulSoup(standard_response.content, 'html.parser') # beautify them
    standard_tfoot = list(standard_soup.find("tfoot"))  # extract the footer values
    std_data_list = standard_tfoot[0].find_all("td") # extract the td list
    values2 = [float(std_data_list[7].text),float(std_data_list[8].text),float(std_data_list[9].text),float(std_data_list[14].text),float(std_data_list[15].text),float(std_data_list[16].text),float(std_data_list[18].text),float(std_data_list[20].text),float(std_data_list[21].text)]    
    
    #CHANGE
    
    low = []
    high = []
    for i in range(len(values1)):
        low.append(0.0)
        high.append(700.0)
    radar = Radar(params,low,high,num_rings=4,ring_width=1,center_circle_radius=1)

    

    fig, ax = radar.setup_axis()
    color1 = "blue"
    color2 = "red"
    rings_inner = radar.draw_circles(ax=ax, facecolor='#ffb2b2', edgecolor='#fc5f5f')
    radar_output = radar.draw_radar_compare(values1, values2, ax=ax,
                                            kwargs_radar={'facecolor': 'blue', 'alpha': 0.8},
                                            kwargs_compare={'facecolor': 'red', 'alpha': 0.4})
    radar_poly, radar_poly2, vertices1, vertices2 = radar_output
    range_labels = radar.draw_range_labels(ax=ax, fontsize=15)
    param_labels = radar.draw_param_labels(ax=ax, fontsize=15)
    plt.savefig('img.png') # save the image
    image = Image.open('img.png')
    image = image.convert('RGB')
    image.save('img.jpg','JPEG')
    image_path = 'img.jpg' # convert the image into numpy array
    img = Image.open(image_path)
    img_arr = np.array(img) 
    os.remove('img.jpg') # delete the image
    return Image.fromarray(img_arr)

def compare_teams(team1_ext,team2_ext,team1,team2):

    params = ["points_per_game","g_scored_per_game","g_conc_per_game","xG","xGC"]

    url = 'https://fbref.com/en/squads/' + team1_ext
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    info_div = soup.find('div', {'id': 'info'})
    p_tags = info_div.find_all('p')
    points_per_game = (float((p_tags[0].text)[41:45]))
    g_scored_per_game = (float((p_tags[2].text)[11:15]))
    g_conc_per_game = (float((p_tags[2].text)[55:59]))
    xG = (float((p_tags[3].text)[4:8]))
    xGC = (float((p_tags[3].text)[24:28]))
    values1 = [points_per_game,g_scored_per_game,g_conc_per_game,xG,xGC]

    url = 'https://fbref.com/en/squads/' + team2_ext
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    info_div = soup.find('div', {'id': 'info'})
    p_tags = info_div.find_all('p')
    points_per_game = (float((p_tags[0].text)[41:45]))
    g_scored_per_game = (float((p_tags[2].text)[11:15]))
    g_conc_per_game = (float((p_tags[2].text)[55:59]))
    xG = (float((p_tags[3].text)[4:8]))
    xGC = (float((p_tags[3].text)[24:28]))
    values2 = [points_per_game,g_scored_per_game,g_conc_per_game,xG,xGC]

    #CHANGE

    low  = [0.0,0.0,0.0,0.0,0.0]
    high = [10.0,5.0,5.0,50.0,50.0]
    radar = Radar(params,low,high,num_rings=4,ring_width=1,center_circle_radius=1)
    fig, ax = radar.setup_axis()
    rings_inner = radar.draw_circles(ax=ax, facecolor='#ffb2b2', edgecolor='#fc5f5f')
    radar_output = radar.draw_radar_compare(values1, values2, ax=ax,
                                             kwargs_radar={'facecolor': 'blue', 'alpha': 0.8},
                                            kwargs_compare={'facecolor': 'red', 'alpha': 0.4})
    radar_poly, radar_poly2, vertices1, vertices2 = radar_output
    range_labels = radar.draw_range_labels(ax=ax, fontsize=15)
    param_labels = radar.draw_param_labels(ax=ax, fontsize=15)
    plt.savefig('img.png') # save the image
    image = Image.open('img.png')
    image = image.convert('RGB')
    image.save('img.jpg','JPEG')
    image_path = 'img.jpg' # convert the image into numpy array
    img = Image.open(image_path)
    img_arr = np.array(img) 
    os.remove('img.jpg') # delete the image
    return Image.fromarray(img_arr)
    


def home(request):
    return render(request, 'home.html')

def analyzeteams(request):
    if(request.method == 'POST'):
        teamname = request.POST['teamname']
        original_teamname = teamname
        team_ext = teams_dict[teamname]
        team_ext = team_ext.lower()
        team_ext = team_ext.replace(" ","")
        analysis_img = analyze_team(team_ext,original_teamname)
        buffered = BytesIO()
        analysis_img.save(buffered,format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        context = {'image_str':img_str,'team': original_teamname}
        return render(request,'analyzeteamssuccess.html',context)
    else:
        return render(request, 'analyzeteams.html')

def analyzeplayers(request):
    if(request.method == 'POST'):
        playername = request.POST['playername']
        original_player_name = playername
        playername = playername.lower()
        playername = playername.replace(" ","")
        name_ext = players_dict[playername]
        analysis_img = analyze_player(name_ext,original_player_name)
        buffered = BytesIO()
        analysis_img.save(buffered,format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        context = {'image_str':img_str,'player': original_player_name}
        return render(request,'analyzeplayerssuccess.html',context)
    else:
        return render(request, 'analyzeplayers.html')

def predictmatches(request):

    home_teams = ['Arsenal', 'Aston Villa', 'Brentford', 'Brighton and Hove Albion',
       'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Leeds United',
       'Leicester City', 'Liverpool', 'Manchester City',
       'Manchester United', 'Newcastle United', 'Norwich City',
       'Southampton', 'Tottenham Hotspur', 'Watford', 'West Ham United',
       'Wolverhampton Wanderers'];

    home_teams = convert_to_lowercase(home_teams)

    away_teams = ['Brentford', 'Chelsea', 'Manchester City', 'Norwich City',
       'Burnley', 'Tottenham', 'Brighton', 'Crystal Palace',
       'Aston Villa', 'Leicester City', 'Watford', 'Liverpool',
       'Newcastle Utd', 'Manchester Utd', 'Everton', 'Southampton',
       'West Ham', 'Leeds United', 'Wolves', 'Arsenal']
        
    away_teams = convert_to_lowercase(away_teams)

    days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']

    if(request.method == 'POST'):

        venue_code = int(request.POST['venue_code'] == 'home')
        team_code  = int(home_teams.index(request.POST['team_code']))
        opp_code   = int(away_teams.index(request.POST['opp_code']))
        hour       = int(request.POST['hour'])
        day_code   = int(days.index(request.POST['day_code']))
        GF         = int(request.POST['GF'])
        xG         = float(request.POST['xG'])
        xGA         = float(request.POST['xGA'])
        SoT        = int(request.POST['SoT'])

        input_array = [[venue_code,team_code,day_code,hour,opp_code,GF,xG,xGA,SoT]]
        
        loaded_model = pickle.load(open("randomforestmodel.pkl","rb"))
        home_team = home_teams[team_code];
        away_team = away_teams[opp_code];
        if(loaded_model.predict(input_array)):
            message = f"{home_team} will win and {away_team} will lose\n"
        else:
            message = f"{home_team} will lose and {away_team} will win\n"
        print(message)
        context = {'message':message}
        return render(request,'predictmatchessuccess.html',context)
    else:
        return render(request, 'predictmatches.html')

def compareplayers(request):
    if(request.method == 'POST'):
        player1name = request.POST['player1name']
        player1 = player1name
        player1name = player1name.lower()
        player1name = player1name.replace(" ","")
        player1_ext = players_dict[player1name]

        player2name = request.POST['player2name']
        player2 = player2name
        player2name = player2name.lower()
        player2name = player2name.replace(" ","")
        player2_ext = players_dict[player2name]

        compare_players_image = compare_players(player1_ext,player2_ext,player1,player2)
        buffered = BytesIO()
        compare_players_image.save(buffered,format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        context = {'image_str':img_str, 'player1': player1, 'player2': player2}
        return render(request,'compareplayerssuccess.html',context)
    else:
        return render(request, 'compareplayers.html')

def compareteams(request):
    if(request.method == 'POST'):

        team1name = request.POST['team1name']
        team1 = team1name
        team1name = team1name.lower()
        team1name = team1name.replace(" ","")
        team1_ext = teams_dict[team1name]

        team2name = request.POST['team2name']
        team2 = team2name
        team2name = team2name.lower()
        team2name = team2name.replace(" ","")
        team2_ext = teams_dict[team2name]
        
        compare_teams_image = compare_teams(team1_ext,team2_ext,team1,team2)
        buffered = BytesIO()
        compare_teams_image.save(buffered,format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        context = {'image_str':img_str,'team1': team1, 'team2':team2}
        return render(request,'compareteamssuccess.html',context)
    else:
        return render(request, 'compareteams.html')
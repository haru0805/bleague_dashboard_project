from django.shortcuts import render
from django.http import HttpResponse, Http404
from bleague_analysis.models import Team, Game, Player, District
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Case, When, F, ExpressionWrapper, FloatField
from django.db import models

# Calculate team statistics for a given team_id
def calculate_team_stats(team_id):
    games = Game.objects.filter(own_team=team_id)
    total_games = games.count()
    wins = games.filter(win_or_lose=1).count()
    losses = games.filter(win_or_lose=0).count()

    return total_games, wins, losses

# Calculate team rankings in the district
def team_rank_in_district(team_id):
    team = Team.objects.get(bleague_id=team_id)
    district_id = team.district_id.id
    teams_in_district = Team.objects.filter(district_id=district_id)

    team_stats = []

    for team in teams_in_district:
        total_games, wins, losses = calculate_team_stats(team.bleague_id)
        win_rate = wins / total_games if total_games != 0 else 0
        team_stats.append({'team_id': team.bleague_id, 'win_rate': win_rate})

    sorted_teams = sorted(team_stats, key=lambda x: x['win_rate'], reverse=True)

    for index, sorted_team in enumerate(sorted_teams, start=1):
        if sorted_team['team_id'] == team_id:
            return index

    return None

# Calculate team rankings overall
def team_rank_overall(team_id):
    all_teams = Team.objects.all()

    team_stats = []

    for team in all_teams:
        total_games, wins, losses = calculate_team_stats(team.bleague_id)
        win_rate = wins / total_games if total_games != 0 else 0
        team_stats.append({'team_id': team.bleague_id, 'win_rate': win_rate})

    sorted_teams = sorted(team_stats, key=lambda x: x['win_rate'], reverse=True)

    for index, sorted_team in enumerate(sorted_teams, start=1):
        if sorted_team['team_id'] == team_id:
            return index

    return None

# Top page view
def top(request):
    team_list = Team.objects.all()
    standings_data = Team.objects.annotate(
        total_games=Count('own_team'),
        wins=Sum(
            Case(
                When(own_team__win_or_lose=1, then=1),
                default=0,
                output_field=models.IntegerField(),
            )
        ),
        loses=Sum(
            Case(
                When(own_team__win_or_lose=0, then=1),
                default=0,
                output_field=models.IntegerField(),
            )
        )
    ).annotate(
        win_percentage=ExpressionWrapper(
            F('wins') / F('total_games'),
            output_field=FloatField(),
        )
    ).order_by('-win_percentage', '-wins', 'name')

    return render(request, 'bleague_analysis/top.html', {'standings_data': standings_data, 'team_list': team_list})

# Team detail view
def team_detail(request, team_id):
    try:
        teams = Team.objects.get(bleague_id=team_id)
    except Team.DoesNotExist:
        raise Http404("チームが存在しません。")

    district_rank = team_rank_in_district(team_id)
    overall_rank = team_rank_overall(team_id)

    page = request.GET.get('page', 1)
    games = Game.objects.select_related('own_team', 'other_team').filter(own_team_id=team_id).order_by('date')
    game_count = games.count()
    wins = games.filter(win_or_lose=1).count()
    loses = games.filter(win_or_lose=0).count()
    win_percentage = wins / game_count
    team_list = Team.objects.all()
    paginator = Paginator(games, 10)  # 10件ずつ表示
    page_obj = paginator.get_page(page)
    players = Player.objects.filter(team_id=team_id)
    context = {'teams': teams, 'games': games, 'players': players, 'page_obj': page_obj, 'team_list': team_list,
               "game_count": game_count, "wins": wins, "loses": loses, "win_percentage": win_percentage,
               "district_rank": district_rank, "overall_rank": overall_rank}
    return render(request, 'bleague_analysis/team_detail.html', context)

# Player detail view
def player_detail(request, team_id, player_id):
    try:
        teams = Team.objects.get(bleague_id=team_id)
    except Team.DoesNotExist:
        raise Http404("チームが存在しません。")
    player_id = str(player_id)
    try:
        players = Player.objects.filter(bleague_id=player_id)
    except Player.DoesNotExist:
        raise Http404("選手が存在しません。")
    team_list = Team.objects.all()
    context = {'teams': teams, 'players': players, 'team_list': team_list}
    return render(request, 'bleague_analysis/player_detail.html', context)

# Team list view
def team_list(request):
    teams = Team.objects.all()
    context = {'teams':teams}
    return render(request, 'bleague_analysis/team_list.html', context)

# District rankings view
def district_rankings(request):
    districts = District.objects.exclude(id=4)
    district_teams = []
    team_list = Team.objects.all()

    for district in districts:
        teams = Team.objects.filter(district_id=district.id)
        team_stats = []

        for team in teams:
            total_games, wins, losses = calculate_team_stats(team.bleague_id)
            win_rate = wins / total_games if total_games != 0 else 0
            team_stats.append({'team': team, 'win_rate': win_rate, 'total_games': total_games, 'wins': wins, 'losses': losses})

        sorted_teams = sorted(team_stats, key=lambda x: x['win_rate'], reverse=True)

        district_teams.append({'district': district, 'teams': sorted_teams})

    context = {'district_teams': district_teams, 'team_list': team_list}
    return render(request, 'bleague_analysis/district_rankings.html', context)


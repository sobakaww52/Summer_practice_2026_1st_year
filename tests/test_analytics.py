import pytest
import pandas as pd
from src.analytics import calculate_home_stats, calculate_away_stats, sort

def test_home_stats_calculation():
    df = pd.DataFrame({
        'home_team_id': [1],
        'away_team_id': [2],
        'home_score': [2],
        'away_score': [1]
    })
    
    result = calculate_home_stats(df)
    
    assert result.loc[0, 'goals_for'] == 2
    assert result.loc[0, 'goal_aganist'] == 1
    assert result.loc[0, 'won'] == 1
    assert result.loc[0, 'points'] == 3

def test_away_stats_calculation():
    df = pd.DataFrame({
        'home_team_id': [1],
        'away_team_id': [2],
        'home_score': [1],
        'away_score': [1]
    })
    
    result = calculate_away_stats(df)
    
    assert result.loc[0, 'goals_for'] == 1
    assert result.loc[0, 'goals_against'] == 1
    assert result.loc[0, 'drawn'] == 1
    assert result.loc[0, 'points'] == 1

def test_sort_standings():
    data = [
        {'team_id': 1, 'points': 3, 'goal_difference': 1, 'goals_for': 2},
        {'team_id': 2, 'points': 6, 'goal_difference': 4, 'goals_for': 5},
        {'team_id': 3, 'points': 3, 'goal_difference': 3, 'goals_for': 4}  
    ]
    
    sorted_data = sort(data)
    
    assert sorted_data[0]['team_id'] == 2
    assert sorted_data[1]['team_id'] == 3
    assert sorted_data[2]['team_id'] == 1
    
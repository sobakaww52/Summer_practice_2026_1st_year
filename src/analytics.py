import pandas as pd
from sqlmodel import Session, select, delete
from .database import engine
from .models import Match, Standing



def calculate_home_stats(df: pd.DataFrame):
    home_df = pd.DataFrame()

    home_df['team_id'] = df['home_team_id']
    home_df['goals_for'] = df['home_score']
    home_df['goal_aganist'] = df['away_score']

    home_df['won'] = (df['home_score'] > df['away_score']).astype(int)
    home_df['drawn'] = (df['away_score'] == df['home_score']).astype(int)
    home_df['lost'] = (df['away_score'] > df['home_score']).astype(int)
    home_df['points'] = home_df['won'] * 3 + home_df['drawn'] * 1

    return home_df

def calculate_away_stats(df: pd.DataFrame):
    away_df = pd.DataFrame()

    away_df['team_id'] = df['away_team_id']
    away_df['goals_for'] = df['away_score']
    away_df['goals_against'] = df['home_score']
    
    away_df['won'] = (df['away_score'] > df['home_score']).astype(int)
    away_df['drawn'] = (df['away_score'] == df['home_score']).astype(int)
    away_df['lost'] = (df['away_score'] < df['home_score']).astype(int)
    away_df['points'] = away_df['won'] * 3 + away_df['drawn'] * 1

    return away_df

def sort(data: list[dict]):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            team_a = data[j]
            team_b = data[j + 1]

            key_a = (team_a['points'], team_a['goal_difference'], team_a['goals_for'])
            key_b = (team_b['points'], team_b['goal_difference'], team_b['goals_for'])

            if key_b > key_a:
                data[j], data[j + 1] = data[j + 1], data[j]

    return data

def update_standings():
    with Session(engine) as session:
        matches = session.exec(select(Match)).all()
        df = pd.DataFrame([m.model_dump() for m in matches])

    full_df = pd.concat([calculate_home_stats(df), calculate_away_stats(df)], ignore_index=True)
    stats = full_df.groupby('team_id').sum().reset_index()

    stats['played'] = stats['won'] + stats['drawn'] + stats['lost']
    stats['goal_difference'] = stats['goals_for'] - stats['goals_against']

    records = stats.to_dict(orient='records')
    sorted_records = sort(records)

    with Session(engine) as session:
        session.exec(delete(Standing))  
        
        for pos, item in enumerate(sorted_records, start=1):
            standing = Standing(
                position=pos,
                team_id=int(item['team_id']),
                played=int(item['played']),
                won=int(item['won']),
                drawn=int(item['drawn']),
                lost=int(item['lost']),
                goals_for=int(item['goals_for']),
                goals_against=int(item['goals_against']),
                goal_difference=int(item['goal_difference']),
                points=int(item['points'])
            )
            session.add(standing)
            
        session.commit()

if __name__ == "__main__":
    update_standings()
from pathlib import Path
import pandas as pd
from sqlmodel import Session, select
from .database import engine
from .models import Team, Match

def load_all_data():
    csv_path = Path(__file__).parent.parent / "data" / "processed" / "matches_clean.csv"

    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')

    all_teams = set(df['HomeTeam']) | set(df['AwayTeam'])

    with Session(engine) as session:
        team_id_map = {}
        for team_name in sorted(all_teams):
                existing = session.exec(
                    select(Team).where(Team.name == team_name)
                ).first()

                if existing:
                    team_id_map[team_name] = existing.id
                else:
                    new_team = Team(name=team_name)
                    session.add(new_team)
                    session.flush()
                    team_id_map[team_name] = new_team.id

        for _, row in df.iterrows():
                match = Match(
                    home_team_id=team_id_map[row['HomeTeam']],
                    away_team_id=team_id_map[row['AwayTeam']],
                    home_score=int(row['FTHG']),
                    away_score=int(row['FTAG']),
                    match_date=row['Date'].date()
                )
                session.add(match)

        session.commit()

def verify_data():
    with Session(engine) as session:
        teams_count = session.exec(select(Team)).all()
        matches_count = session.exec(select(Match)).all()
        print(f"Команд в БД: {len(teams_count)}")
        print(f"Матчей в БД: {len(matches_count)}")

if __name__ == "__main__":
    load_all_data()
    verify_data()
        
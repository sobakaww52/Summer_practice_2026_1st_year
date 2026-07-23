from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)

class Match(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    home_team_id: int = Field(foreign_key="team.id")
    away_team_id: int = Field(foreign_key="team.id")

    home_score: int
    away_score: int
    match_date: date
    round: Optional[int] = None

class Standing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="team.id")
    position: int
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
    
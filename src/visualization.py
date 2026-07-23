import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlmodel import Session, select
from .database import engine
from .models import Standing, Team, Match

PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


def plot_goals_bar_chart():
    with Session(engine) as session:
        query = select(Standing, Team.name).join(Team, Standing.team_id == Team.id)
        results = session.exec(query).all()
        
    data = [{
        "team": team_name,
        "goals_for": s.goals_for,
        "goals_against": s.goals_against,
        "points": s.points
    } for s, team_name in results]
            
    df = pd.DataFrame(data).sort_values(by="points", ascending=False)

    plt.figure(figsize=(12, 6))
    x = np.arange(len(df))
    width = 0.35

    plt.bar(x - width/2, df["goals_for"], width, label="Забито (GF)", color="#2ecc71")
    plt.bar(x + width/2, df["goals_against"], width, label="Пропущено (GA)", color="#e74c3c")

    plt.title("Забитые и пропущенные голы по командам", fontsize=14, fontweight="bold")
    plt.xlabel("Команды", fontsize=12)
    plt.ylabel("Мячи", fontsize=12)
    plt.xticks(x, df["team"], rotation=45, ha="right")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()

    path = os.path.join(PLOTS_DIR, "1_goals_bar_chart.png")
    plt.savefig(path, dpi=300)
    plt.close()


def plot_heatmap():
    """2. Тепловая карта матчей (Matplotlib via imshow)"""
    with Session(engine) as session:
        matches = session.exec(select(Match)).all()
        teams = {t.id: t.name for t in session.exec(select(Team)).all()}

    if not matches:
        return

    df = pd.DataFrame([m.model_dump() for m in matches])
    df['home_team'] = df['home_team_id'].map(teams)
    df['away_team'] = df['away_team_id'].map(teams)

    pivot = df.pivot_table(
        index='home_team', 
        columns='away_team', 
        values='home_score', 
        aggfunc='sum', 
        fill_value=0
    )

    team_names = pivot.index.tolist()
    matrix = pivot.to_numpy()

    fig, ax = plt.subplots(figsize=(10, 8))
    
    cax = ax.imshow(matrix, cmap='YlOrRd')
    fig.colorbar(cax, label='Забито голов хозяевами')

    for i in range(len(team_names)):
        for j in range(len(team_names)):
            ax.text(j, i, int(matrix[i, j]), ha='center', va='center', color='black')

    ax.set_xticks(np.arange(len(team_names)))
    ax.set_yticks(np.arange(len(team_names)))
    ax.set_xticklabels(team_names, rotation=45, ha='right')
    ax.set_yticklabels(team_names)

    plt.title("Тепловая карта: Забитые голы (Хозяева vs Гости)", fontsize=14, fontweight="bold")
    plt.xlabel("Гостевая команда", fontsize=12)
    plt.ylabel("Домашняя команда", fontsize=12)
    plt.tight_layout()

    path = os.path.join(PLOTS_DIR, "2_matches_heatmap.png")
    plt.savefig(path, dpi=300)
    plt.close()


def plot_points_line_chart():
    with Session(engine) as session:
        query = select(Standing, Team.name).join(Team, Standing.team_id == Team.id)
        results = session.exec(query).all()

    df = pd.DataFrame([{
        "position": s.position,
        "team": team_name,
        "points": s.points
    } for s, team_name in results]).sort_values(by="position")

    plt.figure(figsize=(10, 5))
    plt.plot(df["team"], df["points"], marker='o', color='#3498db', linewidth=2, markersize=8)

    plt.title("Распределение набранных очков в турнирной таблице", fontsize=14, fontweight="bold")
    plt.xlabel("Команды (в порядке занятых мест)", fontsize=12)
    plt.ylabel("Очки", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    path = os.path.join(PLOTS_DIR, "3_points_line_chart.png")
    plt.savefig(path, dpi=300)
    plt.close()


if __name__ == "__main__":
    plot_goals_bar_chart()
    plot_heatmap()
    plot_points_line_chart()
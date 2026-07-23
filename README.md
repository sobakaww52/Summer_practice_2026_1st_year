# ⚽ EPL Data Analytics (Season 2007/2008)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Automated%20Testing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

Учебный проект по анализу данных результатов матчей Английской Премьер-Лиги сезона 2007/2008. В рамках проекта реализован ETL-процесс, агрегация статистики команд, кастомная сортировка турнирной таблицы, построение аналитических графиков и покрытие бизнес-логики автотестами.

---

## 🛠 Технологический стек

* **Язык программирования:** Python 3.11+
* **База данных:** PostgreSQL 16 (в Docker-контейнере)
* **ORM & Модели:** SQLModel
* **Обработка данных:** Pandas, NumPy
* **Визуализация:** Matplotlib
* **Тестирование:** Pytest
* **Управление зависимостями:** `uv` / `pip`
* **Контейнеризация:** Docker Compose

---

## 📐 Архитектура базы данных

Проект использует реляционную модель из трех таблиц:
* `Team`: уникальные команды лиги (`id`, `name`).
* `Match`: результаты сыгранных матчей (`home_team_id`, `away_team_id`, `home_score`, `away_score`, `match_date`).
* `Standing`: итоговая турнирная таблица (`position`, `played`, `won`, `drawn`, `lost`, `goals_for`, `goals_against`, `goal_difference`, `points`).

---

## 🚀 Быстрый запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/sobakaww52/Summer-practice-2026-1st-year-.git
cd epl-data-analytics

# VinylMarket 

[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F49?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=flat&logo=jinja&logoColor=white)](https://www.sqlalchemy.org/)

Сервис для продажи и покупки виниловых пластинок.


![Главный экран](images/main.png)


## 🚀 Основные возможности

### 💡 Базовый функционал

- **Поиск пластинок**:
  - Просмотр информации о пластинке и её продавце
  - Поиск по названию/артисту/жанру
  
- **Управление корзиной**:
  - Просмотр добавленных пластинок
  - Добавление/Удаление пластинок 

- **Управление заказами**:
  - Просмотр сделанных заказов
  - Создание заказа
  - Изменение статуса заказа в зависимости от роли

- **Возможности продавца**:
  - Создание/Изменение/Удаление объявлений
  - Просмотр купленных пластинок
  - Изменение статуса заказа


## 🛠 Технологический стек

### Backend
- **Framework**: FastAPI
- **Библиотеки**: sqlalchemy, pydantic, alembic, asyncpg, pyjwt

### Frontend
- **Библиотеки**: jinja2, html, css, javascript


## 🏗 Архитектура проекта

### 🧱 Сервисная структура
| Сервис                      | Назначение                          |
|-----------------------|-------------------------------------|
| **Auth Service**      | Создание аккаунта/Вход в аккаунт пользователя/продавца. Создание/Обновление/Удаление JWT токенов. |
| **Seller Service**  | Создание/Изменение/Удаление объявлений объявлений. Изменение статуса заказа.  |
| **User Service**   | Информация об аккаунте пользователя. Изменение карзины и списка заказов пользователя. |
| **Vinyl Records Service**      | Просмотр информации о пластинке. Поиск по названию/артисту/жанру. |
| **Frontend**              | Пользовательский интерфейс.         |

## 🚀 Быстрый старт

### Запуск проекта

```bash
git clone https://github.com/ResetPlease/Random-coffee-MAI-Tech.git
cd random-coffee
docker compose up -d
```
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
import time

# Definição da tabela Power
class Power(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Sem relacionamento bidirecional

# Modificação da tabela Hero
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    special_power_id: Optional[int] = Field(default=None, foreign_key="power.id")



# Configuração do banco de dados
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

# Criação das tabelas no banco de dados
SQLModel.metadata.create_all(engine)

# Exemplo de inserção de dados
def create_powers_and_heroes():
    with Session(engine) as session:
        power1 = Power(name="Flying")
        power2 = Power(name="Invisibility")
        power3 = Power(name="Poison")
        power4 = Power(name="Super Strength")

        session.add_all([power1, power2, power3, power4])
        session.commit()  # Commit após adicionar os poderes
        
        hero1 = Hero(name="Hero1", secret_name="Secret1", age=30, special_power_id=power1.id)
        hero2 = Hero(name="Hero2", secret_name="Secret2", age=25, special_power_id=power2.id)
        hero3 = Hero(name="Hero3", secret_name="Secret3", age=18, special_power_id=power3.id)
        hero4 = Hero(name="Hero4", secret_name="Secret4", age=40)  # Sem poder associado

        session.add_all([hero1, hero2, hero3, hero4])
        session.commit()  # Commit após adicionar os heróis

# Executa a função para inserir dados
create_powers_and_heroes()

# Consultando os dados com LEFT JOIN
def query_heroes_with_powers():
    with Session(engine) as session:
        # Usamos outerjoin para garantir que todos os heróis sejam retornados, mesmo sem poder associado
        statement = select(Hero, Power).outerjoin(Power, Hero.special_power_id == Power.id)
        results = session.exec(statement).all()

        for hero, power in results:
            power_name = power.name if power else "No Power"  # Define "No Power" se power for None
            print(f"Hero: {hero.name}, Power: {power_name}")

# Executa a função de consulta
query_heroes_with_powers()

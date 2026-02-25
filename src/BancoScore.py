import sqlite3
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # Dentro do executável PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    # Desenvolvimento normal — base é pasta do arquivo atual
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Sobe um nível (de src/ para raiz do projeto)
    base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)

class BancoScore:
    def __init__(self, nome_banco='score.db'):
        # CAMINHO DO BANCO:
        # No PyInstaller, salva na MESMA PASTA do executável
        # No desenvolvimento, salva na raiz do projeto
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller: pasta onde o .exe está rodando
            self.nome_banco = os.path.join(os.path.dirname(sys.executable), nome_banco)
        else:
            # Desenvolvimento: raiz do projeto
            self.nome_banco = resource_path(nome_banco)
        # Cria tabela se não existir
        self.criar_tabela()

    # ============================================================
    # CONEXÃO E TABELA SQLITE

    def conectar(self):
        """Cria conexão com banco SQLite local."""
        return sqlite3.connect(self.nome_banco)

    def criar_tabela(self):
        """Cria tabela de scores se não existir."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_jogador TEXT NOT NULL,
                    pontuacao INTEGER NOT NULL,
                    orbes_energia INTEGER NOT NULL,
                    orbes_vida INTEGER NOT NULL,
                    dificuldade TEXT,
                    data_partida TEXT NOT NULL
                )
            """)
            conn.commit()

    # ============================================================
    # SALVAR SCORE

    def salvar_score(self, nome_jogador, pontuacao, orbes_energia, orbes_vida, dificuldade, data_partida):
        """Salva score no banco SQLite."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scores (
                    nome_jogador, pontuacao, orbes_energia,
                    orbes_vida, dificuldade, data_partida
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome_jogador, pontuacao, orbes_energia,
                  orbes_vida, dificuldade, data_partida))
            conn.commit()

        # Remove scores fora do top 10
        self.limpar_fora_do_top10()

    # ============================================================
    # LISTAR TOP 10

    def listar_top10(self):
        """Retorna top 10 scores no formato de tuplas."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nome_jogador, pontuacao, orbes_energia,
                       orbes_vida, dificuldade, data_partida
                FROM scores
                ORDER BY pontuacao DESC, id ASC
                LIMIT 10
            """)
            return cursor.fetchall()

    # ============================================================
    # VERIFICAR SE ENTRA NO TOP 10
    def entra_no_top10(self, pontuacao):
        """Verifica se uma pontuação merece entrar no ranking."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM scores")
            total = cursor.fetchone()[0]
            if total < 10:
                return True
            cursor.execute("""
                SELECT pontuacao FROM scores
                ORDER BY pontuacao ASC, id DESC
                LIMIT 1
            """)
            menor_top10 = cursor.fetchone()[0]
            return pontuacao > menor_top10

    # LIMPAR SCORES FORA DO TOP 10
    def limpar_fora_do_top10(self):
        """Remove scores que não estão no top 10."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM scores
                WHERE id NOT IN (
                    SELECT id FROM scores
                    ORDER BY pontuacao DESC, id ASC
                    LIMIT 10
                )
            """)
            conn.commit()
import sqlite3
import pandas as pd

def is_table_in_1nf(db_file, table_name):
    """
    Verifies if a table in a SQLite database is in First Normal Form (1NF).
    
    Args:
        db_file (str): Path to the SQLite database file.
        table_name (str): Name of the table to verify.
    
    Returns:
        bool: True if the table is in 1NF, False otherwise.
    """
    conn = sqlite3.connect(db_file)
    try:
        # Load the table into a DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        
        # Check for atomic values (no lists, dictionaries, or arrays)
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, (list, dict, set))).any():
                print(f"Column '{col}' contains non-atomic values.")
                return False
        
        # Check for unique rows
        if df.duplicated().any():
            print("The table contains duplicate rows.")
            return False
        
        # Check for a primary key (unique identifier)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        primary_keys = [col[1] for col in columns_info if col[5] == 1]  # Column with PK flag
        
        if not primary_keys:
            print("The table does not have a primary key.")
            return False
        
        print(f"The table '{table_name}' is in 1NF.")
        return True
    except Exception as e:
        print(f"Error verifying 1NF for table '{table_name}': {e}")
        return False
    finally:
        conn.close()




def is_table_in_2nf(db_file, table_name):
    """
    Verifica se uma tabela em um banco de dados SQLite está na Segunda Forma Normal (2NF).

    Esta função usa heurísticas baseadas no esquema da tabela. A verificação é definitiva
    para tabelas com chaves primárias simples. Para chaves compostas, a função não pode
    provar a dependência funcional e, portanto, adota uma abordagem conservadora,
    sinalizando potenciais violações para revisão manual.

    Args:
        db_file (str): Caminho para o arquivo do banco de dados SQLite.
        table_name (str): Nome da tabela a ser verificada.

    Returns:
        bool: True se a tabela está em 2NF, False caso contrário ou se uma
              violação for suspeita.
    """
    conn = sqlite3.connect(db_file)
    try:
        cursor = conn.cursor()

        # Etapa 1: Obter informações das colunas e identificar a chave primária
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        columns_info = cursor.fetchall()
        
        if not columns_info:
            print(f"Erro: A tabela '{table_name}' não existe no banco de dados.")
            return False

        all_columns = {col[1] for col in columns_info}
        primary_key_columns = {col[1] for col in columns_info if col[5] > 0}

        # Etapa 2: Verificar se existe uma chave primária
        if not primary_key_columns:
            print(f"AVISO: A tabela '{table_name}' não possui chave primária. Não está em 2NF.")
            return False

        # Etapa 3: Se a chave primária é simples (só uma coluna), não pode haver dependência parcial.
        # A tabela está automaticamente em 2NF (assumindo que está em 1NF).
        if len(primary_key_columns) == 1:
            print(f"INFO: A tabela '{table_name}' possui uma chave primária simples. Está em 2NF.")
            return True

        # Etapa 4: Se a chave primária é composta, verificar a dependência parcial.
        # Uma violação ocorre se um atributo não-primo depende de parte da chave composta.
        non_prime_attributes = all_columns - primary_key_columns
        
        # Se não há atributos não-primos, não pode haver dependência parcial.
        # A chave cobre a tabela inteira.
        if not non_prime_attributes:
            print(f"INFO: A tabela '{table_name}' tem uma chave primária composta, mas não possui atributos não-primos. Está em 2NF.")
            return True
            
        # Se há atributos não-primos, existe o RISCO de uma violação da 2NF.
        # Não podemos determinar programaticamente a dependência funcional.
        # Portanto, sinalizamos como uma falha que requer verificação manual.
        print(f"AVISO: A tabela '{table_name}' tem uma chave primária composta e os seguintes atributos não-primos: {non_prime_attributes}.")
        print("      É necessário verificar manualmente se cada um desses atributos depende da CHAVE COMPOSTA INTEIRA.")
        print(f"      Se algum atributo depender de apenas uma parte da chave {primary_key_columns}, a tabela não está em 2NF.")
        return False

    except sqlite3.OperationalError as e:
        print(f"Erro operacional ao verificar a tabela '{table_name}': {e}")
        return False
    except Exception as e:
        print(f"Um erro inesperado ocorreu ao verificar a tabela '{table_name}': {e}")
        return False
    finally:
        conn.close()

def is_table_in_3nf(db_file, table_name):
    """
    Verifica se uma tabela em um banco de dados SQLite está na Terceira Forma Normal (3NF).

    Esta função usa heurísticas baseadas no esquema. Ela primeiro verifica se a tabela
    está em 2NF e, em seguida, procura por indicadores de dependências transitivas,
    como chaves estrangeiras que não fazem parte da chave primária.

    Args:
        db_file (str): Caminho para o arquivo do banco de dados SQLite.
        table_name (str): Nome da tabela a ser verificada.
    
    Returns:
        bool: True se a tabela está em 3NF, False caso contrário.
    """

    
    conn = sqlite3.connect(db_file)
    try:
        cursor = conn.cursor()
        
        # Obter a chave primária
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        columns_info = cursor.fetchall()
        primary_key_columns = {col[1] for col in columns_info if col[5] > 0}
        
        # Etapa 2: Procurar por dependências transitivas.
        # A heurística é verificar se existe uma chave estrangeira (FK)
        # cuja coluna de origem NÃO faz parte da chave primária.
        
        cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
        foreign_keys = cursor.fetchall()
        
        for fk in foreign_keys:
            fk_from_column = fk[3]  # Coluna na tabela atual que é a FK
            
            # Se a coluna da FK não está na chave primária, é um forte indício
            # de uma dependência transitiva.
            if fk_from_column not in primary_key_columns:
                print(f"AVISO: A tabela '{table_name}' possui uma chave estrangeira ('{fk_from_column}') que não é parte da chave primária.")
                print(f"       Isso sugere uma dependência transitiva, o que viola a 3NF.")
                print(f"       Atributos nesta tabela podem depender de '{fk_from_column}' em vez de dependerem da chave primária {primary_key_columns}.")
                return False
        
        # Se passou na verificação de 2NF e não encontrou FKs suspeitas, está em 3NF.
        print(f"INFO: A tabela '{table_name}' está em 2NF e não foram encontrados indicadores de dependência transitiva. A tabela está em 3NF.")
        return True

    except Exception as e:
        print(f"Erro ao verificar 3NF para a tabela '{table_name}': {e}")
        return False
    finally:
        conn.close()

def verify_database_normalization(db_file, table_name=None):
    """
    Verifies the normalization of all tables in a SQLite database.
    
    Args:
        db_file (str): Path to the SQLite database file.
    
    Returns:
        dict: A dictionary with table names as keys and their normalization status as values.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    normalization_status = {}
    

        
    is_1nf = is_table_in_1nf(db_file, table_name)
    is_2nf = is_table_in_2nf(db_file, table_name) if is_1nf else False
    is_3nf = is_table_in_3nf(db_file, table_name) if is_2nf else False
        
    normalization_status[table_name] = {
        '1NF': is_1nf,
        '2NF': is_2nf,
        '3NF': is_3nf
    }
    
    conn.close()
    return normalization_status
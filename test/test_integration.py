import pytest
import pyodbc
import pandas as pd

def get_connection(database_name):
    # À adapter selon votre config
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        f"DATABASE={database_name};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(connection_string)

@pytest.fixture(scope="session")
def crm_conn():
    """Fixture Pytest : connexion à la base CRM"""
    conn = get_connection("CRM")
    yield conn
    conn.close()

@pytest.fixture(scope="session")
def erp_conn():
    """Fixture Pytest : connexion à la base ERP"""
    conn = get_connection("ERP")
    yield conn
    conn.close()

def test_count_clients(crm_conn, erp_conn):
    """
    Test 1 : Vérifier que le nombre de clients est identique entre CRM et ERP
    """
    crm_cursor = crm_conn.cursor()
    erp_cursor = erp_conn.cursor()

    # Requête pour récupérer le nombre de clients dans CRM
    crm_cursor.execute("SELECT COUNT(*) FROM Clients")
    crm_count = crm_cursor.fetchone()[0]

    # Requête pour récupérer le nombre de clients dans ERP
    erp_cursor.execute("SELECT COUNT(*) FROM ClientsERP")
    erp_count = erp_cursor.fetchone()[0]

    assert crm_count == erp_count, f"Nombre de clients différent: CRM={crm_count}, ERP={erp_count}"

def test_compare_clients_data(crm_conn, erp_conn):
    """
    Test 2 : Vérifier que la liste (et les champs) des clients sont identiques
    entre la table CRM.dbo.Clients et ERP.dbo.ClientsERP
    """
    # Charger les données CRM dans un DataFrame
    crm_df = pd.read_sql_query("SELECT ClientID, Nom, Email, Telephone FROM Clients", crm_conn)

    # Charger les données ERP dans un DataFrame
    erp_df = pd.read_sql_query("SELECT ClientID, Nom, Email, Telephone FROM ClientsERP", erp_conn)

    # Option 1 : trier et comparer directement l’égalité des DataFrames
    crm_sorted = crm_df.sort_values(by=["ClientID"]).reset_index(drop=True)
    erp_sorted = erp_df.sort_values(by=["ClientID"]).reset_index(drop=True)

    # Vérifier qu'ils ont la même forme (mêmes lignes, mêmes colonnes)
    assert crm_sorted.shape == erp_sorted.shape, "Les DataFrames CRM/ERP n'ont pas le même nombre de lignes ou colonnes."

    # Vérifier que le contenu est identique
    pd.testing.assert_frame_equal(crm_sorted, erp_sorted, check_like=True)

def test_compare_commandes_data(crm_conn, erp_conn):
    """
    Test 3 : Comparaison ligne à ligne pour les commandes
    """
    crm_df = pd.read_sql_query("SELECT CommandeID, ClientID, Montant, DateCommande FROM Commandes", crm_conn)
    erp_df = pd.read_sql_query("SELECT CommandeID, ClientID, Montant, DateCommande FROM CommandesERP", erp_conn)

    crm_sorted = crm_df.sort_values(by=["CommandeID"]).reset_index(drop=True)
    erp_sorted = erp_df.sort_values(by=["CommandeID"]).reset_index(drop=True)

    assert crm_sorted.shape == erp_sorted.shape, "Les DataFrames CRM/ERP (commandes) n'ont pas la même taille."
    pd.testing.assert_frame_equal(crm_sorted, erp_sorted, check_like=True)

# TP-PYODBC
Valider automatiquement l’intégration de données migrées entre une base source (CRM) et une base cible (ERP).


--création des deux BDD

CREATE DATABASE CRM;
GO

CREATE DATABASE ERP;
GO


USE CRM;
GO

--création des tables
-- Table Clients
CREATE TABLE Clients (
    ClientID INT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Telephone VARCHAR(20) NULL
);

-- Table Commandes
CREATE TABLE Commandes (
    CommandeID INT PRIMARY KEY,
    ClientID INT NOT NULL,
    Montant DECIMAL(10, 2) NOT NULL,
    DateCommande DATETIME NOT NULL,
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);


USE ERP;
GO

-- Table Clients
CREATE TABLE ClientsERP (
    ClientID INT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Telephone VARCHAR(20) NULL
);

-- Table Commandes
CREATE TABLE CommandesERP (
    CommandeID INT PRIMARY KEY,
    ClientID INT NOT NULL,
    Montant DECIMAL(10, 2) NOT NULL,
    DateCommande DATETIME NOT NULL,
    FOREIGN KEY (ClientID) REFERENCES ClientsERP(ClientID)
);

--Insérer des données de test
USE CRM;
GO

INSERT INTO Clients (ClientID, Nom, Email, Telephone)
VALUES
(1, 'Client A', 'clientA@example.com', '0102030405'),
(2, 'Client B', 'clientB@example.com', '0102030406'),
(3, 'Client C', 'clientC@example.com', NULL);

INSERT INTO Commandes (CommandeID, ClientID, Montant, DateCommande)
VALUES
(100, 1, 250.50, '20250110'),
(101, 1, 99.99,  '20250215'),
(102, 2, 150.00, '20250220');

--Simuler la migration (copie de données vers ERP)
USE ERP;
GO

-- Copie de Clients
INSERT INTO ClientsERP (ClientID, Nom, Email, Telephone)
SELECT ClientID, Nom, Email, Telephone
FROM CRM.dbo.Clients;

-- Copie de Commandes
INSERT INTO CommandesERP (CommandeID, ClientID, Montant, DateCommande)
SELECT CommandeID, ClientID, Montant, DateCommande
FROM CRM.dbo.Commandes;

--Comparer le nombre de lignes
--Nombre de clients
SELECT 'CRM' AS Source, COUNT(*) AS NbClients FROM CRM.dbo.Clients
UNION ALL
SELECT 'ERP' AS Source, COUNT(*) AS NbClients FROM ERP.dbo.ClientsERP;

--Nombre de commandes
SELECT 'CRM' AS Source, COUNT(*) AS NbCommandes FROM CRM.dbo.Commandes
UNION ALL
SELECT 'ERP' AS Source, COUNT(*) AS NbCommandes FROM ERP.dbo.CommandesERP;

--Comparer ligne à ligne : requêtes de vérification
-- Clients présents dans CRM mais pas dans ERP
SELECT ClientID, Nom, Email, Telephone
FROM CRM.dbo.Clients

EXCEPT

SELECT ClientID, Nom, Email, Telephone
FROM ERP.dbo.ClientsERP;

--Dans l'autre sens (ERP - CRM) :
-- Clients présents dans ERP mais pas dans CRM
SELECT ClientID, Nom, Email, Telephone
FROM ERP.dbo.ClientsERP

EXCEPT

SELECT ClientID, Nom, Email, Telephone
FROM CRM.dbo.Clients;

--Vérifier l'intégrité du référentiel
USE ERP;
GO

SELECT c.*
FROM CommandesERP c
LEFT JOIN ClientsERP cli ON c.ClientID = cli.ClientID
WHERE cli.ClientID IS NULL;














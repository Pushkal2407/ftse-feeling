DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Follow CASCADE;
DROP TABLE IF EXISTS Company CASCADE;
DROP TABLE IF EXISTS Stock CASCADE;
DROP TABLE IF EXISTS Fundementals CASCADE;
DROP TABLE IF EXISTS News CASCADE;


CREATE TABLE Users(
    userID SERIAL NOT NULL,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phash VARCHAR(256),
    interests VARCHAR[],
    PRIMARY KEY (userID)

);

CREATE TABLE Company(
    companyName VARCHAR(100),
    sector VARCHAR(100),
    description TEXT,
    ticker VARCHAR(100) UNIQUE, -- logo is given by their stock ticker
    executives VARCHAR[],
    stockPrediction FLOAT,
    PRIMARY KEY (ticker)

);



CREATE TABLE Stock(
    ticker VARCHAR(100) NOT NULL UNIQUE,
    updateTime TIMESTAMP NOT NULL,
    openValue FLOAT,
    highValue FLOAT,
    lowValue FLOAT,
    closeValue FLOAT,
    volume INTEGER,
    PRIMARY KEY (ticker),
    FOREIGN KEY (ticker) REFERENCES Company(ticker)


);

CREATE TABLE Fundementals(
    ticker VARCHAR(100) NOT NULL UNIQUE,
    reportDate TIMESTAMP NOT NULL,
    revenueTTM FLOAT,
    netGrossProfit FLOAT,
    ebitda FLOAT,
    PRIMARY KEY (ticker),
    FOREIGN KEY (ticker) REFERENCES Company(ticker)

);



CREATE TABLE Follow(
    userID INTEGER NOT NULL,
    ticker VARCHAR(100) NOT NULL,
    PRIMARY KEY (userID, ticker),
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (ticker) REFERENCES Company(ticker)

);

-- CREATE TABLE News(
--     newsID SERIAL NOT NULL,
--     headline VARCHAR(100),
--     summary TEXT,
--     link VARCHAR(100),
--     sentimentLabel VARCHAR(100), --???
--     sentimentValue FLOAT, --???
--     newspaperName VARCHAR(128),
--     ticker VARCHAR(100) NOT NULL UNIQUE,
--     PRIMARY KEY (newsID),
--     FOREIGN KEY (ticker) REFERENCES Company(ticker)


-- );
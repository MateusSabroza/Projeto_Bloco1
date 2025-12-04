-- Gerado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   em:        2025-12-01 00:49:33 BRT
--   site:      Oracle Database 11g
--   tipo:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE




CREATE TABLE PRODUTO
(
    ID           NUMBER(10)      NOT NULL ,
    NOME         VARCHAR2 (240)  NOT NULL ,
    PRECO        NUMBER (10,2)   NOT NULL, 
    QTD_ESTOQUE  NUMBER(10)      DEFAULT 0 NOT NULL, 
    DESCRICAO    CLOB
)
;

ALTER TABLE PRODUTO
    ADD CONSTRAINT PRODUTO_PK PRIMARY KEY ( ID ) ;


CREATE TABLE VENDA
(
    ID            NUMBER(10)     NOT NULL ,
    DATA_VENDA    DATE           NOT NULL , 
    VALOR_TOTAL   NUMBER (10,2)  DEFAULT 0 
)
;

ALTER TABLE VENDA
    ADD CONSTRAINT VENDA_PK PRIMARY KEY ( ID ) ;



CREATE TABLE ITEM_VENDA
(
    Venda_ID    INTEGER NOT NULL,
    Produto_ID  INTEGER NOT NULL,
    Qtd_pedida  INTEGER NOT NULL,
    Preco_unitario NUMBER (10,2) NOT NULL
)
;

ALTER TABLE ITEM_VENDA
    ADD CONSTRAINT ItemVenda_PK PRIMARY KEY ( Venda_ID, Produto_ID ) ;


ALTER TABLE ITEM_VENDA
    ADD CONSTRAINT ItemVenda_Venda_FK FOREIGN KEY
    (
        Venda_ID
    )
    REFERENCES Venda
    (
        ID
    )
;



ALTER TABLE ITEM_VENDA
    ADD CONSTRAINT ItemVenda_Produto_FK FOREIGN KEY
    (
        Produto_ID
    )
    REFERENCES Produto
    (
        ID
    )
;



CREATE SEQUENCE Produto_Seq START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE Venda_Seq START WITH 1 INCREMENT BY 1 NOCACHE;

CREATE OR REPLACE TRIGGER PRODUTO_TRIG
BEFORE INSERT ON PRODUTO FOR EACH ROW
BEGIN
    :NEW.ID := Produto_Seq.NEXTVAL;
END;
/


CREATE OR REPLACE TRIGGER VENDA_TRIG
BEFORE INSERT ON VENDA FOR EACH ROW
BEGIN
    :NEW.ID := Venda_Seq.NEXTVAL;
END;
/


INSERT INTO PRODUTO (NOME, PRECO, QTD_ESTOQUE, DESCRICAO) 
VALUES ('SQL Pro: Guia Prático para Iniciantes', 89.90, 50, 'Livro de estudo completo sobre modelagem e queries SQL.');

INSERT INTO PRODUTO (NOME, PRECO, QTD_ESTOQUE, DESCRICAO) 
VALUES ('Caneca Amazonense', 29.50, 150, 'Caneca personalizada com o logo da Amazonense.');

INSERT INTO PRODUTO (NOME, PRECO, QTD_ESTOQUE, DESCRICAO) 
VALUES ('Mousepad Ergonômico XL', 45.00, 80, 'Mousepad grande com apoio de pulso.');

INSERT INTO PRODUTO (NOME, PRECO, QTD_ESTOQUE, DESCRICAO) 
VALUES ('Kit Teclado e Mouse sem Fio', 199.90, 45, 'Kit confortável para uso diário de escritório.');


INSERT INTO PRODUTO (NOME, PRECO, QTD_ESTOQUE, DESCRICAO) 
VALUES ('Cadeira Gamer X-Pro', 999.00, 10, 'Cadeira ergonômica com ajuste de altura e inclinação.');


INSERT INTO PRODUTO (NOME, PRECO, QTD_ESTOQUE, DESCRICAO) 
VALUES ('Cabo HDMI 2.1 (3m)', 55.50, 200, 'Cabo de alta velocidade, suporta 8K.');


INSERT INTO PRODUTO (NOME, PRECO, QTD_ESTOQUE, DESCRICAO) 
VALUES ('Headset Noise Cancelling', 350.75, 65, 'Fones de ouvido para comunicação e isolamento de ruído.');


INSERT INTO PRODUTO (NOME, PRECO, QTD_ESTOQUE, DESCRICAO) 
VALUES ('Pen Drive 64GB USB 3.0', 49.99, 120, 'Armazenamento rápido e portátil.');


INSERT INTO PRODUTO (NOME, PRECO, QTD_ESTOQUE, DESCRICAO) 
VALUES ('Webcam Full HD', 125.00, 90, 'Webcam com microfone embutido para videoconferências.');


INSERT INTO PRODUTO (NOME, PRECO, QTD_ESTOQUE, DESCRICAO) 
VALUES ('Filtro de Linha 5 Tomadas', 35.00, 180, 'Proteção contra surtos e picos de energia.');


COMMIT;




-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             3
-- CREATE INDEX                             0
-- ALTER TABLE                              7
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0

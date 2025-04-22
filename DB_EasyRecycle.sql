create database EasyRecycle;

use EasyRecycle;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,                         		-- Chave primária, com auto incremento
    `name` VARCHAR(200) NOT NULL,                                 	-- Nome do usuário, não pode ser nulo
    email VARCHAR(255) NOT NULL UNIQUE,                           	-- Email único, tamanho padrão para emails
    `password` VARCHAR(255) NOT NULL,                          		-- Senha criptografada, pode ter tamanho variável
    phone VARCHAR(15),                                          	-- Número de telefone, considerando o formato internacional
    cep VARCHAR(8),                                              	-- CEP armazenado como string
    points INT DEFAULT 0,                                         	-- Pontuação, padrão 0
    `status` VARCHAR(20) DEFAULT 'active',                    		-- Status do usuário (ativo ou inativo), padrão 'active'
    birth_date DATE,										 		-- Data de nascimento
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,         	-- Data de cadastro, padrão para o momento atual
    last_login_date DATETIME                                     	-- Data do último login
);


create table teste(
nome varchar(200),
data_nascimento date);

insert into teste (Nome, data_nascimento) values ("Andrey", "2005-06-06");
insert into teste (Nome, data_nascimento) values ("Bete", "1972-04-20");
select * from teste;
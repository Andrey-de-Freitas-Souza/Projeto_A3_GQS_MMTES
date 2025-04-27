create database EasyRecycle;

use EasyRecycle;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,                         		-- Chave primária, com auto incremento
    `name` VARCHAR(200) NOT NULL,                                 	-- Nome do usuário, não pode ser nulo
    email VARCHAR(255) NOT NULL UNIQUE,                           	-- Email único, tamanho padrão para emails
    `password` VARCHAR(255) NOT NULL,                          		-- Senha criptografada, pode ter tamanho variável
    phone VARCHAR(15),                                          	-- Número de telefone, considerando o formato internacional
    address VARCHAR(9),                                              -- CEP armazenado como string
    points INT DEFAULT 0,                                         	-- Pontuação, padrão 0
    `status` VARCHAR(20) DEFAULT 'active',                    		-- Status do usuário (ativo ou inativo), padrão 'active'
    birth_date DATE,										 		-- Data de nascimento
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,         	-- Data de cadastro, padrão para o momento atual
    last_login_date DATETIME                                     	-- Data do último login
);

CREATE TABLE collection_point (
    id INT AUTO_INCREMENT PRIMARY KEY,                         		
    `name` VARCHAR(200) NOT NULL,                                 	
	 address VARCHAR(9),
     `number` int
);

INSERT INTO collection_point (`name`, address, `number`) VALUES
('Ponto de Coleta Centro', '01001-000', 123),
('Ponto de Coleta Zona Sul', '04567-890', 456),
('Ponto de Coleta Zona Norte', '02222-333', 789),
('Ponto de Coleta Zona Leste', '03456-789', 101),
('Ponto de Coleta Zona Oeste', '05001-200', 202),
('Ponto de Coleta Bairro Verde', '06070-100', 303),
('Ponto de Coleta Jardim das Flores', '07234-567', 404),
('Ponto de Coleta Vila Nova', '08012-345', 505),
('Ponto de Coleta Estação Central', '01111-222', 606),
('Ponto de Coleta Parque das Árvores', '09090-123', 707);

INSERT INTO collection_point (`name`, address, `number`) VALUES
('Casa', '09668-010', 66);

CREATE TABLE category_item (
    id INT AUTO_INCREMENT PRIMARY KEY,                         		
    `name` VARCHAR(200) NOT NULL,                                 	
	`description`  VARCHAR(1000),
    score_by_kilo int
);
INSERT INTO category_item (`name`, `description`, score_by_kilo) VALUES
('Papel', 'A reciclagem de papel é um processo que transforma os papéis usados em novos produtos. Ela reduz a necessidade de desmatamento, economiza energia e água, além de diminuir a quantidade de resíduos sólidos nos aterros sanitários.', 2),
('Plástico', 'A reciclagem de plástico envolve a coleta, limpeza e transformação de plásticos em novos produtos. Isso ajuda a reduzir a poluição e o consumo de recursos naturais, além de diminuir o impacto ambiental causado pelo descarte inadequado de plásticos.', 8),
('Vidro', 'Vidro pode ser reciclado indefinidamente sem perder qualidade, o que faz sua reciclagem ser uma prática muito eficiente. O processo de reciclagem de vidro economiza energia e recursos, além de evitar o acúmulo de vidro nos aterros sanitários.', 3),
('Metais', 'A reciclagem de metais, como alumínio e aço, é altamente eficiente, pois os metais podem ser reutilizados infinitamente sem perder suas propriedades. Esse processo economiza energia e recursos naturais, além de reduzir a emissão de poluentes.', 4),
('Eletrônicos (Eletroeletrônicos)', 'A reciclagem de eletroeletrônicos envolve a extração de materiais valiosos, como metais preciosos, e o descarte adequado de componentes tóxicos. Isso evita a contaminação ambiental e promove a reutilização de recursos.', 10),
('Orgânicos', 'A reciclagem orgânica, geralmente por meio da compostagem, transforma resíduos de alimentos e outros materiais biodegradáveis em adubo, contribuindo para a redução do volume de resíduos e para a melhoria da qualidade do solo.', 5),
('Têxteis', 'A reciclagem de têxteis envolve o reaproveitamento de materiais têxteis, que podem ser transformados em novos produtos ou reciclados para a produção de fibras. Isso reduz o desperdício e ajuda a diminuir a demanda por novos recursos.', 6),
('Madeira', 'A reciclagem de madeira é um processo que envolve o reaproveitamento de madeira usada para a fabricação de novos produtos ou como fonte de energia. Isso ajuda a reduzir o desperdício e a preservação de florestas, além de diminuir a emissão de gases poluentes.', 5),
('Baterias e Pilhas', 'A reciclagem de baterias e pilhas é crucial para evitar a liberação de substâncias tóxicas no meio ambiente. Através desse processo, materiais valiosos, como metais, podem ser recuperados e reutilizados, enquanto componentes perigosos são descartados de maneira segura.', 10),
('Resíduos Mistos', 'Resíduos mistos consistem em materiais que não se enquadram facilmente em outras categorias, e sua reciclagem envolve a separação e recuperação de componentes valiosos. Embora desafiadora, essa reciclagem contribui para a redução do desperdício e a utilização eficiente de recursos.', 7);

drop table recycle;
drop table recyclable_item;
drop table category_item;


CREATE TABLE recycle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id int,
    FOREIGN KEY (user_id) REFERENCES users(id),
    category_id int,
    FOREIGN KEY (category_id) REFERENCES category_item(id),
    weight_item float,
    point_id int,
    FOREIGN KEY (point_id) REFERENCES collection_point(id),
    date_recycle DATETIME
);

select * from Users;
select * from collection_point;
select * from category_item;
select * from recycle;

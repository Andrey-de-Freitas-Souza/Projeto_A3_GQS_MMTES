create database EasyRecycle;

use EasyRecycle;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,                         		-- Chave primária, com auto incremento
    `name` VARCHAR(200) NOT NULL,                                 	-- Nome do usuário, não pode ser nulo
    email VARCHAR(255) NOT NULL UNIQUE,                           	-- Email único, tamanho padrão para emails
    `password` VARCHAR(255) NOT NULL,                          		-- Senha criptografada, pode ter tamanho variável
	phone VARCHAR(20),                                          	-- Número de telefone, considerando o formato internacional
    address VARCHAR(9),                                              -- CEP armazenado como string
    points INT DEFAULT 0,                                         	-- Pontuação, padrão 0
    `status` VARCHAR(20) DEFAULT 'active',                    		-- Status do usuário (ativo ou inativo), padrão 'active'
    birth_date DATE,										 		-- Data de nascimento
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,         	-- Data de cadastro, padrão para o momento atual
    last_login_date DATETIME                                     	-- Data do último login
);
ALTER TABLE Users ADD COLUMN phone_new VARCHAR(20);
UPDATE Users SET phone_new = phone;
ALTER TABLE Users DROP COLUMN phone;
ALTER TABLE Users CHANGE phone_new phone VARCHAR(20);

update Users set points = 200 where id = 4;
update Users set points = 150 where id = 2;
update Users set points = 175 where id = 3;
update Users set points = 0 where id = 1;


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
('Papel', 'A reciclagem de papel é um processo que transforma os papéis usados em novos produtos. Ela reduz a necessidade de desmatamento, economiza energia e água, além de diminuir a quantidade de resíduos sólidos nos aterros sanitários.', 200),
('Plástico', 'A reciclagem de plástico envolve a coleta, limpeza e transformação de plásticos em novos produtos. Isso ajuda a reduzir a poluição e o consumo de recursos naturais, além de diminuir o impacto ambiental causado pelo descarte inadequado de plásticos.', 800),
('Vidro', 'Vidro pode ser reciclado indefinidamente sem perder qualidade, o que faz sua reciclagem ser uma prática muito eficiente. O processo de reciclagem de vidro economiza energia e recursos, além de evitar o acúmulo de vidro nos aterros sanitários.', 300),
('Metais', 'A reciclagem de metais, como alumínio e aço, é altamente eficiente, pois os metais podem ser reutilizados infinitamente sem perder suas propriedades. Esse processo economiza energia e recursos naturais, além de reduzir a emissão de poluentes.', 400),
('Eletrônicos (Eletroeletrônicos)', 'A reciclagem de eletroeletrônicos envolve a extração de materiais valiosos, como metais preciosos, e o descarte adequado de componentes tóxicos. Isso evita a contaminação ambiental e promove a reutilização de recursos.', 1000),
('Orgânicos', 'A reciclagem orgânica, geralmente por meio da compostagem, transforma resíduos de alimentos e outros materiais biodegradáveis em adubo, contribuindo para a redução do volume de resíduos e para a melhoria da qualidade do solo.', 500),
('Têxteis', 'A reciclagem de têxteis envolve o reaproveitamento de materiais têxteis, que podem ser transformados em novos produtos ou reciclados para a produção de fibras. Isso reduz o desperdício e ajuda a diminuir a demanda por novos recursos.', 600),
('Madeira', 'A reciclagem de madeira é um processo que envolve o reaproveitamento de madeira usada para a fabricação de novos produtos ou como fonte de energia. Isso ajuda a reduzir o desperdício e a preservação de florestas, além de diminuir a emissão de gases poluentes.', 50),
('Baterias e Pilhas', 'A reciclagem de baterias e pilhas é crucial para evitar a liberação de substâncias tóxicas no meio ambiente. Através desse processo, materiais valiosos, como metais, podem ser recuperados e reutilizados, enquanto componentes perigosos são descartados de maneira segura.', 100),
('Resíduos Mistos', 'Resíduos mistos consistem em materiais que não se enquadram facilmente em outras categorias, e sua reciclagem envolve a separação e recuperação de componentes valiosos. Embora desafiadora, essa reciclagem contribui para a redução do desperdício e a utilização eficiente de recursos.', 70);

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

INSERT INTO recycle (user_id, category_id, weight_item, point_id, date_recycle)  VALUES(4,8,500,2,CURRENT_TIMESTAMP);

CREATE TABLE user_friendship (
    id INT AUTO_INCREMENT PRIMARY KEY,
    requesting_user_id INT,
    approver_user_id INT,
    status VARCHAR(10) DEFAULT 'Solicitado',
    date_friend DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (requesting_user_id) REFERENCES users(id),
    FOREIGN KEY (approver_user_id) REFERENCES users(id)
);
insert into user_friendship (requesting_user_id,approver_user_id,status,date_friend) values (4,3,"Solicitado",CURRENT_TIMESTAMP);
insert into user_friendship (requesting_user_id,approver_user_id,status,date_friend) values (5,4,"Solicitado",CURRENT_TIMESTAMP);
select * from user_friendship;
CREATE TABLE user_notification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type_notification VARCHAR(50) NOT NULL,
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    date_notification DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

select * from Users;
select * from collection_point;
select * from category_item;
select * from recycle;
select * from user_notification;
select * from user_friendship;


select recycle.date_recycle, 
	   category_item.`name`, 
       recycle. weight_item,
       collection_point.`name`,
	   category_item.score_by_kilo * (recycle. weight_item/1000) as score
       from recycle 
       left join category_item on recycle.category_id = category_item.id
       left join collection_point on recycle.point_id = collection_point.id
       where user_id = 5
       order by recycle.date_recycle desc;
       
SELECT 	category_item.`name`, 
		sum(recycle.weight_item/ 1000) as weight_item 
FROM recycle 
left join category_item 
on recycle.category_id = category_item.id  
group by category_item.`name`
order by weight_item desc;


SELECT recycle.date_recycle,
		query_1.`name`
from recycle
left join (	SELECT 	category_item.id, 
					category_item.`name`,
					SUM(recycle.weight_item) AS total_weight
			FROM recycle 
			LEFT JOIN category_item ON recycle.category_id = category_item.id  
			GROUP BY category_item.id, category_item.name
			ORDER BY total_weight DESC
			LIMIT 1) query_1
        on query_1.id = recycle.category_id
        where `name` is not null ;

SELECT category_item.`name`, recycle.date_recycle FROM recycle left join category_item on recycle.category_id = category_item.id order by recycle.weight_item desc;

SELECT 
    category_item.id, 
    category_item.name,
    SUM(recycle.weight_item) AS total_weight
FROM recycle 
LEFT JOIN category_item ON recycle.category_id = category_item.id  
GROUP BY category_item.id, category_item.name
ORDER BY total_weight DESC
LIMIT 1;

WITH top_category AS (
  SELECT 
    recycle.category_id
  FROM recycle
  GROUP BY recycle.category_id
  ORDER BY SUM(recycle.weight_item) DESC
  LIMIT 1
)

SELECT 
  category_item.name,
  recycle.date_recycle,
  recycle.weight_item
FROM recycle
JOIN top_category ON recycle.category_id = top_category.category_id
JOIN category_item ON recycle.category_id = category_item.id;



 WITH ranked_categories AS (
    SELECT 
        recycle.category_id,
        SUM(recycle.weight_item) AS total_weight,
        ROW_NUMBER() OVER (ORDER BY SUM(recycle.weight_item) DESC) AS `rank`
    FROM recycle
    GROUP BY recycle.category_id
)
SELECT 
    category_item.name,
    recycle.date_recycle,
    recycle.weight_item,
    category_item.color_hex
FROM recycle
JOIN ranked_categories ON recycle.category_id = ranked_categories.category_id
JOIN category_item ON recycle.category_id = category_item.id
WHERE ranked_categories. `rank`= 3;


select * from user_friendship;
SELECT * FROM user_friendship 
        WHERE (requesting_user_id = 5 AND approver_user_id = 1) 
           OR (requesting_user_id = 1 AND approver_user_id = 5);
           
SELECT users.id, users.name, user_friendship.status, user_friendship.date_friend  
FROM users
JOIN user_friendship ON (users.id = user_friendship.requesting_user_id)
WHERE (user_friendship.approver_user_id = 1)
AND user_friendship.status = 'Solicitado';

SELECT u.id, u.name, uf.status, uf.date_friend
FROM users u
JOIN user_friendship uf ON (u.id = uf.requesting_user_id)
WHERE uf.approver_user_id = 4  -- Troque 1 pelo id de um usuário que você quer testar
AND uf.status = 'Solicitado';


SELECT u.id, u.name, u.points
        FROM user_friendship uf
        JOIN users u ON (
            (uf.requesting_user_id = u.id AND uf.approver_user_id = 4) OR
            (uf.approver_user_id = u.id AND uf.requesting_user_id = 4)
        )
        WHERE uf.status = 'Aprovado';
        
SELECT 
    u.id, 
    u.name, 
    u.points,
    ROW_NUMBER() OVER (ORDER BY u.points DESC) AS ranking
FROM user_friendship uf
JOIN users u ON (
    (uf.requesting_user_id = u.id AND uf.approver_user_id = 4) OR
    (uf.approver_user_id = u.id AND uf.requesting_user_id = 4)
)
WHERE uf.status = 'Aprovado'
ORDER BY u.points DESC;

SELECT 
    all_users.id, 
    all_users.name, 
    all_users.points,
    ROW_NUMBER() OVER (ORDER BY all_users.points DESC) AS ranking
FROM (
    -- Amigos aprovados
    SELECT 
        u.id, 
        u.name, 
        u.points
    FROM user_friendship uf
    JOIN users u ON (
        (uf.requesting_user_id = u.id AND uf.approver_user_id = 4) OR
        (uf.approver_user_id = u.id AND uf.requesting_user_id = 4)
    )
    WHERE uf.status = 'Aprovado'

    UNION

    -- Usuário logado
    SELECT 
        u.id, 
        u.name, 
        u.points
    FROM users u
    WHERE u.id = 4
) AS all_users
ORDER BY all_users.points DESC;

-- Seed OpenClaw Sankhya - Dados ficticios realistas
-- Contexto: Pneubras - distribuidora de pneus

-- Limpar tabelas
DELETE FROM "TGFITE";
DELETE FROM "TGFCAB";
DELETE FROM "TGFPRO";
DELETE FROM "TGFVEND";
DELETE FROM "TGFPAR";
ALTER SEQUENCE "TGFPAR_CODPARC_seq" RESTART WITH 1;
ALTER SEQUENCE "TGFVEND_CODVEND_seq" RESTART WITH 1;
ALTER SEQUENCE "TGFPRO_CODPROD_seq" RESTART WITH 1;
ALTER SEQUENCE "TGFCAB_NUNOTA_seq" RESTART WITH 1;

-- =============================================================================
-- TGFVEND - 10 Vendedores
-- =============================================================================
INSERT INTO "TGFVEND" ("APELIDO", "NOMEVEND", "COMISSAO", "TELEFONE", "EMAIL", "ATIVO") VALUES
('Carlos', 'Carlos Eduardo Silva', 3.5, '81999110001', 'carlos.silva@pneubras.com.br', 'S'),
('Marcos', 'Marcos Aurelio Santos', 3.0, '81999110002', 'marcos.santos@pneubras.com.br', 'S'),
('Fernanda', 'Fernanda Oliveira Costa', 4.0, '81999110003', 'fernanda.costa@pneubras.com.br', 'S'),
('Roberto', 'Roberto Almeida Junior', 3.5, '81999110004', 'roberto.junior@pneubras.com.br', 'S'),
('Patricia', 'Patricia Souza Lima', 3.0, '81999110005', 'patricia.lima@pneubras.com.br', 'S'),
('Anderson', 'Anderson Pereira Gomes', 3.5, '81999110006', 'anderson.gomes@pneubras.com.br', 'S'),
('Juliana', 'Juliana Barbosa Reis', 4.0, '81999110007', 'juliana.reis@pneubras.com.br', 'S'),
('Ricardo', 'Ricardo Mendes Filho', 3.0, '81999110008', 'ricardo.mendes@pneubras.com.br', 'S'),
('Camila', 'Camila Ferreira Nunes', 3.5, '81999110009', 'camila.nunes@pneubras.com.br', 'S'),
('Diego', 'Diego Rocha Cavalcanti', 3.0, '81999110010', 'diego.rocha@pneubras.com.br', 'S');

-- =============================================================================
-- TGFPAR - 50 Clientes
-- =============================================================================
INSERT INTO "TGFPAR" ("NOMEPARC", "RAZAOSOCIAL", "TIPPESSOA", "CGCCPF", "CIDADE", "UF", "TELEFONE", "EMAIL", "LIMCRED", "BAIRRO") VALUES
('Auto Center Silva', 'Auto Center Silva LTDA', 'J', '12.345.678/0001-01', 'Recife', 'PE', '(81)98001-0001', 'c1@auto.com.br', 100000, 'Boa Viagem'),
('Pneus Oliveira', 'Pneus Oliveira LTDA', 'J', '12.345.678/0001-02', 'Fortaleza', 'CE', '(85)98001-0002', 'c2@auto.com.br', 75000, 'Centro'),
('Borracharia Santos', 'Borracharia Santos LTDA', 'J', '12.345.678/0001-03', 'Salvador', 'BA', '(71)98001-0003', 'c3@auto.com.br', 50000, 'Pituba'),
('Mecanica Costa', 'Mecanica Costa LTDA', 'J', '12.345.678/0001-04', 'Natal', 'RN', '(84)98001-0004', 'c4@auto.com.br', 25000, 'Centro'),
('Auto Pecas Lima', 'Auto Pecas Lima LTDA', 'J', '12.345.678/0001-05', 'Joao Pessoa', 'PB', '(83)98001-0005', 'c5@auto.com.br', 150000, 'Manaira'),
('Centro Automotivo Pereira', 'Centro Automotivo Pereira LTDA', 'J', '12.345.678/0001-06', 'Maceio', 'AL', '(82)98001-0006', 'c6@auto.com.br', 50000, 'Pajucara'),
('Garage Almeida', 'Garage Almeida LTDA', 'J', '12.345.678/0001-07', 'Aracaju', 'SE', '(79)98001-0007', 'c7@auto.com.br', 75000, 'Centro'),
('Auto Service Gomes', 'Auto Service Gomes LTDA', 'J', '12.345.678/0001-08', 'Teresina', 'PI', '(86)98001-0008', 'c8@auto.com.br', 100000, 'Centro'),
('Rodas Ferreira', 'Rodas Ferreira LTDA', 'J', '12.345.678/0001-09', 'Sao Luis', 'MA', '(98)98001-0009', 'c9@auto.com.br', 50000, 'Renascenca'),
('Pneumaticos Barbosa', 'Pneumaticos Barbosa LTDA', 'J', '12.345.678/0001-10', 'Caruaru', 'PE', '(81)98001-0010', 'c10@auto.com.br', 200000, 'Centro'),
('Auto Center Martins', 'Auto Center Martins LTDA', 'J', '12.345.678/0001-11', 'Petrolina', 'PE', '(87)98001-0011', 'c11@auto.com.br', 75000, 'Centro'),
('Pneus Rocha', 'Pneus Rocha LTDA', 'J', '12.345.678/0001-12', 'Campina Grande', 'PB', '(83)98001-0012', 'c12@auto.com.br', 100000, 'Centro'),
('Borracharia Cavalcanti', 'Borracharia Cavalcanti LTDA', 'J', '12.345.678/0001-13', 'Feira de Santana', 'BA', '(75)98001-0013', 'c13@auto.com.br', 50000, 'Centro'),
('Mecanica Araujo', 'Mecanica Araujo LTDA', 'J', '12.345.678/0001-14', 'Garanhuns', 'PE', '(87)98001-0014', 'c14@auto.com.br', 25000, 'Centro'),
('Auto Pecas Melo', 'Auto Pecas Melo LTDA', 'J', '12.345.678/0001-15', 'Juazeiro do Norte', 'CE', '(88)98001-0015', 'c15@auto.com.br', 150000, 'Centro'),
('Centro Automotivo Ribeiro', 'Centro Automotivo Ribeiro LTDA', 'J', '12.345.678/0001-16', 'Mossoro', 'RN', '(84)98001-0016', 'c16@auto.com.br', 50000, 'Centro'),
('Garage Cardoso', 'Garage Cardoso LTDA', 'J', '12.345.678/0001-17', 'Parnamirim', 'RN', '(84)98001-0017', 'c17@auto.com.br', 75000, 'Centro'),
('Auto Service Souza', 'Auto Service Souza LTDA', 'J', '12.345.678/0001-18', 'Olinda', 'PE', '(81)98001-0018', 'c18@auto.com.br', 100000, 'Centro'),
('Rodas Santos', 'Rodas Santos LTDA', 'J', '12.345.678/0001-19', 'Jaboatao', 'PE', '(81)98001-0019', 'c19@auto.com.br', 50000, 'Centro'),
('Pneumaticos Lima', 'Pneumaticos Lima LTDA', 'J', '12.345.678/0001-20', 'Paulista', 'PE', '(81)98001-0020', 'c20@auto.com.br', 200000, 'Centro'),
('Auto Center Nunes', 'Auto Center Nunes LTDA', 'J', '12.345.678/0001-21', 'Recife', 'PE', '(81)98001-0021', 'c21@auto.com.br', 100000, 'Imbiribeira'),
('Pneus Dias', 'Pneus Dias LTDA', 'J', '12.345.678/0001-22', 'Recife', 'PE', '(81)98001-0022', 'c22@auto.com.br', 75000, 'Afogados'),
('Borracharia Teixeira', 'Borracharia Teixeira LTDA', 'J', '12.345.678/0001-23', 'Fortaleza', 'CE', '(85)98001-0023', 'c23@auto.com.br', 50000, 'Aldeota'),
('Mecanica Campos', 'Mecanica Campos LTDA', 'J', '12.345.678/0001-24', 'Salvador', 'BA', '(71)98001-0024', 'c24@auto.com.br', 25000, 'Barra'),
('Auto Pecas Freitas', 'Auto Pecas Freitas LTDA', 'J', '12.345.678/0001-25', 'Natal', 'RN', '(84)98001-0025', 'c25@auto.com.br', 150000, 'Ponta Negra'),
('Centro Automotivo Moreira', 'Centro Automotivo Moreira LTDA', 'J', '12.345.678/0001-26', 'Recife', 'PE', '(81)98001-0026', 'c26@auto.com.br', 100000, 'Derby'),
('Garage Pinto', 'Garage Pinto LTDA', 'J', '12.345.678/0001-27', 'Fortaleza', 'CE', '(85)98001-0027', 'c27@auto.com.br', 75000, 'Meireles'),
('Auto Service Cunha', 'Auto Service Cunha LTDA', 'J', '12.345.678/0001-28', 'Salvador', 'BA', '(71)98001-0028', 'c28@auto.com.br', 50000, 'Itapua'),
('Rodas Vieira', 'Rodas Vieira LTDA', 'J', '12.345.678/0001-29', 'Joao Pessoa', 'PB', '(83)98001-0029', 'c29@auto.com.br', 200000, 'Tambauzinho'),
('Pneumaticos Correia', 'Pneumaticos Correia LTDA', 'J', '12.345.678/0001-30', 'Maceio', 'AL', '(82)98001-0030', 'c30@auto.com.br', 100000, 'Jatiuca'),
('Auto Center Lopes', 'Auto Center Lopes LTDA', 'J', '12.345.678/0001-31', 'Recife', 'PE', '(81)98001-0031', 'c31@auto.com.br', 75000, 'Pina'),
('Pneus Castro', 'Pneus Castro LTDA', 'J', '12.345.678/0001-32', 'Caruaru', 'PE', '(81)98001-0032', 'c32@auto.com.br', 50000, 'Boa Vista'),
('Borracharia Monteiro', 'Borracharia Monteiro LTDA', 'J', '12.345.678/0001-33', 'Petrolina', 'PE', '(87)98001-0033', 'c33@auto.com.br', 100000, 'Centro'),
('Mecanica Xavier', 'Mecanica Xavier LTDA', 'J', '12.345.678/0001-34', 'Teresina', 'PI', '(86)98001-0034', 'c34@auto.com.br', 25000, 'Joquei'),
('Auto Pecas Ramos', 'Auto Pecas Ramos LTDA', 'J', '12.345.678/0001-35', 'Sao Luis', 'MA', '(98)98001-0035', 'c35@auto.com.br', 150000, 'Calhau'),
('Centro Automotivo Pires', 'Centro Automotivo Pires LTDA', 'J', '12.345.678/0001-36', 'Aracaju', 'SE', '(79)98001-0036', 'c36@auto.com.br', 100000, 'Atalaia'),
('Garage Nascimento', 'Garage Nascimento LTDA', 'J', '12.345.678/0001-37', 'Recife', 'PE', '(81)98001-0037', 'c37@auto.com.br', 75000, 'Madalena'),
('Auto Service Farias', 'Auto Service Farias LTDA', 'J', '12.345.678/0001-38', 'Fortaleza', 'CE', '(85)98001-0038', 'c38@auto.com.br', 50000, 'Fatima'),
('Rodas Barros', 'Rodas Barros LTDA', 'J', '12.345.678/0001-39', 'Salvador', 'BA', '(71)98001-0039', 'c39@auto.com.br', 200000, 'Ondina'),
('Pneumaticos Mendes', 'Pneumaticos Mendes LTDA', 'J', '12.345.678/0001-40', 'Natal', 'RN', '(84)98001-0040', 'c40@auto.com.br', 100000, 'Tirol'),
('Auto Center Torres', 'Auto Center Torres LTDA', 'J', '12.345.678/0001-41', 'Recife', 'PE', '(81)98001-0041', 'c41@auto.com.br', 75000, 'Espinheiro'),
('Pneus Bezerra', 'Pneus Bezerra LTDA', 'J', '12.345.678/0001-42', 'Campina Grande', 'PB', '(83)98001-0042', 'c42@auto.com.br', 50000, 'Mirante'),
('Borracharia Dantas', 'Borracharia Dantas LTDA', 'J', '12.345.678/0001-43', 'Mossoro', 'RN', '(84)98001-0043', 'c43@auto.com.br', 100000, 'Centro'),
('Mecanica Sampaio', 'Mecanica Sampaio LTDA', 'J', '12.345.678/0001-44', 'Feira de Santana', 'BA', '(75)98001-0044', 'c44@auto.com.br', 25000, 'Centro'),
('Auto Pecas Alencar', 'Auto Pecas Alencar LTDA', 'J', '12.345.678/0001-45', 'Juazeiro do Norte', 'CE', '(88)98001-0045', 'c45@auto.com.br', 150000, 'Centro'),
('Centro Automotivo Brito', 'Centro Automotivo Brito LTDA', 'J', '12.345.678/0001-46', 'Recife', 'PE', '(81)98001-0046', 'c46@auto.com.br', 100000, 'Gracas'),
('Garage Nogueira', 'Garage Nogueira LTDA', 'J', '12.345.678/0001-47', 'Olinda', 'PE', '(81)98001-0047', 'c47@auto.com.br', 75000, 'Casa Caiada'),
('Auto Service Duarte', 'Auto Service Duarte LTDA', 'J', '12.345.678/0001-48', 'Jaboatao', 'PE', '(81)98001-0048', 'c48@auto.com.br', 50000, 'Piedade'),
('Rodas Medeiros', 'Rodas Medeiros LTDA', 'J', '12.345.678/0001-49', 'Paulista', 'PE', '(81)98001-0049', 'c49@auto.com.br', 200000, 'Centro'),
('Pneumaticos Guimaraes', 'Pneumaticos Guimaraes LTDA', 'J', '12.345.678/0001-50', 'Garanhuns', 'PE', '(87)98001-0050', 'c50@auto.com.br', 100000, 'Centro');

-- =============================================================================
-- TGFPRO - 100 Produtos (80 pneus + 20 acessorios)
-- =============================================================================
INSERT INTO "TGFPRO" ("DESCRPROD", "REFERENCIA", "CODGRUPOPROD", "MARCA", "VLRCUSTO", "VLRVENDA", "ESTOQUE", "ESTMIN", "PESOBRUTO", "NCM", "ATIVO") VALUES
('Pneu Pirelli 175/70R13', 'PIR17570R13', 1, 'Pirelli', 220.00, 320.00, 80, 10, 7.5, '40111000', 'S'),
('Pneu Pirelli 185/65R14', 'PIR18565R14', 1, 'Pirelli', 280.00, 400.00, 60, 10, 8.2, '40111000', 'S'),
('Pneu Pirelli 195/55R15', 'PIR19555R15', 1, 'Pirelli', 320.00, 460.00, 45, 8, 8.8, '40111000', 'S'),
('Pneu Pirelli 205/55R16', 'PIR20555R16', 1, 'Pirelli', 380.00, 550.00, 55, 10, 9.5, '40111000', 'S'),
('Pneu Pirelli 215/50R17', 'PIR21550R17', 1, 'Pirelli', 450.00, 650.00, 30, 5, 10.2, '40111000', 'S'),
('Pneu Pirelli 225/45R17', 'PIR22545R17', 1, 'Pirelli', 480.00, 690.00, 25, 5, 10.5, '40111000', 'S'),
('Pneu Pirelli 225/50R18', 'PIR22550R18', 1, 'Pirelli', 520.00, 750.00, 20, 5, 11.0, '40111000', 'S'),
('Pneu Pirelli 265/65R17', 'PIR26565R17', 1, 'Pirelli', 550.00, 800.00, 35, 5, 13.0, '40111000', 'S'),
('Pneu Michelin 175/70R13', 'MIC17570R13', 1, 'Michelin', 240.00, 350.00, 70, 10, 7.6, '40111000', 'S'),
('Pneu Michelin 185/65R14', 'MIC18565R14', 1, 'Michelin', 300.00, 430.00, 50, 10, 8.3, '40111000', 'S'),
('Pneu Michelin 195/55R15', 'MIC19555R15', 1, 'Michelin', 350.00, 500.00, 40, 8, 8.9, '40111000', 'S'),
('Pneu Michelin 205/55R16', 'MIC20555R16', 1, 'Michelin', 400.00, 580.00, 45, 10, 9.6, '40111000', 'S'),
('Pneu Michelin 215/50R17', 'MIC21550R17', 1, 'Michelin', 480.00, 690.00, 25, 5, 10.3, '40111000', 'S'),
('Pneu Michelin 225/45R17', 'MIC22545R17', 1, 'Michelin', 500.00, 720.00, 20, 5, 10.6, '40111000', 'S'),
('Pneu Michelin 235/55R18', 'MIC23555R18', 1, 'Michelin', 560.00, 810.00, 15, 5, 11.5, '40111000', 'S'),
('Pneu Michelin 275/70R16', 'MIC27570R16', 1, 'Michelin', 580.00, 840.00, 30, 5, 13.5, '40111000', 'S'),
('Pneu Goodyear 175/65R14', 'GOO17565R14', 1, 'Goodyear', 200.00, 290.00, 90, 15, 7.8, '40111000', 'S'),
('Pneu Goodyear 185/70R14', 'GOO18570R14', 1, 'Goodyear', 230.00, 330.00, 75, 10, 8.0, '40111000', 'S'),
('Pneu Goodyear 195/65R15', 'GOO19565R15', 1, 'Goodyear', 280.00, 400.00, 60, 10, 8.5, '40111000', 'S'),
('Pneu Goodyear 205/60R15', 'GOO20560R15', 1, 'Goodyear', 310.00, 450.00, 50, 8, 9.0, '40111000', 'S'),
('Pneu Goodyear 205/65R16', 'GOO20565R16', 1, 'Goodyear', 360.00, 520.00, 40, 8, 9.8, '40111000', 'S'),
('Pneu Goodyear 215/55R17', 'GOO21555R17', 1, 'Goodyear', 420.00, 600.00, 30, 5, 10.0, '40111000', 'S'),
('Pneu Goodyear 225/55R17', 'GOO22555R17', 1, 'Goodyear', 440.00, 630.00, 25, 5, 10.4, '40111000', 'S'),
('Pneu Goodyear 235/60R18', 'GOO23560R18', 1, 'Goodyear', 500.00, 720.00, 20, 5, 11.2, '40111000', 'S'),
('Pneu Continental 175/70R13', 'CON17570R13', 1, 'Continental', 210.00, 300.00, 85, 10, 7.4, '40111000', 'S'),
('Pneu Continental 185/65R14', 'CON18565R14', 1, 'Continental', 270.00, 390.00, 65, 10, 8.1, '40111000', 'S'),
('Pneu Continental 195/55R15', 'CON19555R15', 1, 'Continental', 310.00, 450.00, 50, 8, 8.7, '40111000', 'S'),
('Pneu Continental 205/55R16', 'CON20555R16', 1, 'Continental', 370.00, 530.00, 40, 10, 9.4, '40111000', 'S'),
('Pneu Continental 215/50R17', 'CON21550R17', 1, 'Continental', 440.00, 630.00, 28, 5, 10.1, '40111000', 'S'),
('Pneu Continental 225/45R17', 'CON22545R17', 1, 'Continental', 470.00, 680.00, 22, 5, 10.4, '40111000', 'S'),
('Pneu Continental 245/45R19', 'CON24545R19', 1, 'Continental', 580.00, 840.00, 15, 5, 12.0, '40111000', 'S'),
('Pneu Continental 255/40R19', 'CON25540R19', 1, 'Continental', 600.00, 870.00, 12, 5, 12.5, '40111000', 'S'),
('Pneu Bridgestone 175/70R13', 'BRI17570R13', 1, 'Bridgestone', 230.00, 330.00, 75, 10, 7.6, '40111000', 'S'),
('Pneu Bridgestone 185/65R14', 'BRI18565R14', 1, 'Bridgestone', 290.00, 420.00, 55, 10, 8.2, '40111000', 'S'),
('Pneu Bridgestone 195/55R15', 'BRI19555R15', 1, 'Bridgestone', 330.00, 480.00, 42, 8, 8.8, '40111000', 'S'),
('Pneu Bridgestone 205/55R16', 'BRI20555R16', 1, 'Bridgestone', 390.00, 560.00, 38, 10, 9.5, '40111000', 'S'),
('Pneu Bridgestone 215/50R17', 'BRI21550R17', 1, 'Bridgestone', 460.00, 660.00, 22, 5, 10.2, '40111000', 'S'),
('Pneu Bridgestone 225/50R18', 'BRI22550R18', 1, 'Bridgestone', 530.00, 760.00, 18, 5, 11.0, '40111000', 'S'),
('Pneu Bridgestone 235/55R18', 'BRI23555R18', 1, 'Bridgestone', 550.00, 790.00, 15, 5, 11.3, '40111000', 'S'),
('Pneu Bridgestone 265/65R17', 'BRI26565R17', 1, 'Bridgestone', 560.00, 810.00, 20, 5, 13.0, '40111000', 'S'),
('Pneu Firestone 175/65R14', 'FIR17565R14', 1, 'Firestone', 190.00, 270.00, 95, 15, 7.5, '40111000', 'S'),
('Pneu Firestone 185/70R14', 'FIR18570R14', 1, 'Firestone', 210.00, 300.00, 80, 10, 7.9, '40111000', 'S'),
('Pneu Firestone 195/65R15', 'FIR19565R15', 1, 'Firestone', 260.00, 370.00, 65, 10, 8.4, '40111000', 'S'),
('Pneu Firestone 205/60R15', 'FIR20560R15', 1, 'Firestone', 290.00, 420.00, 50, 8, 8.9, '40111000', 'S'),
('Pneu Firestone 205/65R16', 'FIR20565R16', 1, 'Firestone', 340.00, 490.00, 35, 8, 9.6, '40111000', 'S'),
('Pneu Firestone 215/55R17', 'FIR21555R17', 1, 'Firestone', 400.00, 570.00, 28, 5, 9.9, '40111000', 'S'),
('Pneu Firestone 225/55R17', 'FIR22555R17', 1, 'Firestone', 420.00, 600.00, 20, 5, 10.2, '40111000', 'S'),
('Pneu Firestone 235/60R18', 'FIR23560R18', 1, 'Firestone', 480.00, 690.00, 15, 5, 11.0, '40111000', 'S'),
('Pneu Dunlop 175/70R13', 'DUN17570R13', 1, 'Dunlop', 200.00, 290.00, 100, 15, 7.3, '40111000', 'S'),
('Pneu Dunlop 185/65R14', 'DUN18565R14', 1, 'Dunlop', 250.00, 360.00, 70, 10, 8.0, '40111000', 'S'),
('Pneu Dunlop 195/55R15', 'DUN19555R15', 1, 'Dunlop', 300.00, 430.00, 55, 8, 8.6, '40111000', 'S'),
('Pneu Dunlop 205/55R16', 'DUN20555R16', 1, 'Dunlop', 350.00, 500.00, 45, 10, 9.3, '40111000', 'S'),
('Pneu Dunlop 215/50R17', 'DUN21550R17', 1, 'Dunlop', 420.00, 600.00, 30, 5, 10.0, '40111000', 'S'),
('Pneu Dunlop 225/45R17', 'DUN22545R17', 1, 'Dunlop', 450.00, 650.00, 22, 5, 10.3, '40111000', 'S'),
('Pneu Dunlop 225/50R18', 'DUN22550R18', 1, 'Dunlop', 490.00, 710.00, 18, 5, 10.8, '40111000', 'S'),
('Pneu Dunlop 245/45R19', 'DUN24545R19', 1, 'Dunlop', 550.00, 790.00, 12, 5, 11.8, '40111000', 'S'),
('Pneu Yokohama 175/65R14', 'YOK17565R14', 1, 'Yokohama', 195.00, 280.00, 90, 15, 7.4, '40111000', 'S'),
('Pneu Yokohama 185/70R14', 'YOK18570R14', 1, 'Yokohama', 220.00, 320.00, 70, 10, 7.8, '40111000', 'S'),
('Pneu Yokohama 195/65R15', 'YOK19565R15', 1, 'Yokohama', 270.00, 390.00, 55, 10, 8.3, '40111000', 'S'),
('Pneu Yokohama 205/60R15', 'YOK20560R15', 1, 'Yokohama', 300.00, 430.00, 45, 8, 8.8, '40111000', 'S'),
('Pneu Yokohama 215/55R17', 'YOK21555R17', 1, 'Yokohama', 410.00, 590.00, 25, 5, 9.8, '40111000', 'S'),
('Pneu Yokohama 225/55R17', 'YOK22555R17', 1, 'Yokohama', 430.00, 620.00, 20, 5, 10.1, '40111000', 'S'),
('Pneu Yokohama 235/60R18', 'YOK23560R18', 1, 'Yokohama', 490.00, 700.00, 15, 5, 10.9, '40111000', 'S'),
('Pneu Yokohama 255/40R19', 'YOK25540R19', 1, 'Yokohama', 570.00, 820.00, 10, 5, 12.2, '40111000', 'S'),
('Pneu Hankook 175/70R13', 'HAN17570R13', 1, 'Hankook', 185.00, 265.00, 110, 15, 7.2, '40111000', 'S'),
('Pneu Hankook 185/65R14', 'HAN18565R14', 1, 'Hankook', 240.00, 340.00, 80, 10, 7.9, '40111000', 'S'),
('Pneu Hankook 195/55R15', 'HAN19555R15', 1, 'Hankook', 280.00, 400.00, 60, 8, 8.5, '40111000', 'S'),
('Pneu Hankook 205/55R16', 'HAN20555R16', 1, 'Hankook', 330.00, 470.00, 50, 10, 9.2, '40111000', 'S'),
('Pneu Hankook 215/50R17', 'HAN21550R17', 1, 'Hankook', 400.00, 570.00, 35, 5, 9.9, '40111000', 'S'),
('Pneu Hankook 225/45R17', 'HAN22545R17', 1, 'Hankook', 430.00, 620.00, 25, 5, 10.2, '40111000', 'S'),
('Pneu Hankook 235/55R18', 'HAN23555R18', 1, 'Hankook', 480.00, 690.00, 18, 5, 10.7, '40111000', 'S'),
('Pneu Hankook 265/65R17', 'HAN26565R17', 1, 'Hankook', 500.00, 720.00, 22, 5, 12.5, '40111000', 'S'),
('Pneu Kumho 175/65R14', 'KUM17565R14', 1, 'Kumho', 180.00, 260.00, 120, 15, 7.1, '40111000', 'S'),
('Pneu Kumho 185/70R14', 'KUM18570R14', 1, 'Kumho', 200.00, 290.00, 90, 10, 7.6, '40111000', 'S'),
('Pneu Kumho 195/65R15', 'KUM19565R15', 1, 'Kumho', 250.00, 360.00, 70, 10, 8.2, '40111000', 'S'),
('Pneu Kumho 205/60R15', 'KUM20560R15', 1, 'Kumho', 280.00, 400.00, 55, 8, 8.7, '40111000', 'S'),
('Pneu Kumho 205/65R16', 'KUM20565R16', 1, 'Kumho', 320.00, 460.00, 40, 8, 9.3, '40111000', 'S'),
('Pneu Kumho 215/55R17', 'KUM21555R17', 1, 'Kumho', 380.00, 550.00, 30, 5, 9.7, '40111000', 'S'),
('Pneu Kumho 225/55R17', 'KUM22555R17', 1, 'Kumho', 400.00, 580.00, 22, 5, 10.0, '40111000', 'S'),
('Pneu Kumho 235/60R18', 'KUM23560R18', 1, 'Kumho', 460.00, 660.00, 18, 5, 10.6, '40111000', 'S'),
-- Acessorios (20)
('Camara de Ar Aro 13', 'CAM13', 2, 'Nacional', 25.00, 45.00, 200, 10, 0.8, '40130000', 'S'),
('Camara de Ar Aro 14', 'CAM14', 2, 'Nacional', 28.00, 50.00, 180, 10, 0.9, '40130000', 'S'),
('Camara de Ar Aro 15', 'CAM15', 2, 'Nacional', 30.00, 55.00, 160, 10, 1.0, '40130000', 'S'),
('Camara de Ar Aro 16', 'CAM16', 2, 'Nacional', 35.00, 60.00, 140, 10, 1.1, '40130000', 'S'),
('Protetor de Aro 13', 'PRT13', 2, 'Nacional', 12.00, 22.00, 300, 10, 0.3, '40000000', 'S'),
('Protetor de Aro 14', 'PRT14', 2, 'Nacional', 14.00, 25.00, 280, 10, 0.3, '40000000', 'S'),
('Protetor de Aro 15', 'PRT15', 2, 'Nacional', 15.00, 28.00, 260, 10, 0.4, '40000000', 'S'),
('Bico de Pneu Cromado (jg)', 'BCOCR', 2, 'Nacional', 8.00, 18.00, 500, 10, 0.1, '40000000', 'S'),
('Bico de Pneu Preto (jg)', 'BCOPR', 2, 'Nacional', 5.00, 12.00, 600, 10, 0.1, '40000000', 'S'),
('Calibrador Manual', 'CALIB', 3, 'Nacional', 45.00, 85.00, 50, 10, 0.5, '40000000', 'S'),
('Chave de Roda Cruz', 'CHCRZ', 3, 'Nacional', 35.00, 65.00, 80, 10, 1.5, '40000000', 'S'),
('Macaco Hidraulico 2T', 'MACHD', 3, 'Nacional', 120.00, 220.00, 40, 10, 4.0, '40000000', 'S'),
('Cera para Pneu 500ml', 'CERPN', 4, 'Nacional', 18.00, 35.00, 300, 10, 0.6, '40000000', 'S'),
('Limpa Pneu Spray', 'LMPSP', 4, 'Nacional', 15.00, 28.00, 350, 10, 0.4, '40000000', 'S'),
('Selante para Pneu', 'SELPN', 4, 'Nacional', 22.00, 42.00, 200, 10, 0.5, '40000000', 'S'),
('Roda de Ferro Aro 13', 'RDF13', 5, 'Nacional', 80.00, 150.00, 100, 10, 5.0, '40000000', 'S'),
('Roda de Ferro Aro 14', 'RDF14', 5, 'Nacional', 90.00, 170.00, 90, 10, 5.5, '40000000', 'S'),
('Roda de Ferro Aro 15', 'RDF15', 5, 'Nacional', 100.00, 190.00, 80, 10, 6.0, '40000000', 'S'),
('Roda de Liga Leve Aro 15', 'RDL15', 5, 'Nacional', 250.00, 480.00, 60, 10, 4.5, '40000000', 'S'),
('Roda de Liga Leve Aro 17', 'RDL17', 5, 'Nacional', 350.00, 650.00, 40, 10, 5.0, '40000000', 'S');

-- =============================================================================
-- TGFCAB + TGFITE - Pedidos distribuidos em 3 meses
-- Fev: ~160 pedidos, Mar: ~200 pedidos, Abr (1-7): ~80 pedidos
-- Vendedores 1,2,3 com queda ~15-25% em abril vs marco
-- Clientes 41-50 compram em marco mas nao em abril (inativos)
-- =============================================================================

-- Funcao auxiliar para gerar pedidos
DO $$
DECLARE
    v_nunota INTEGER;
    v_codparc INTEGER;
    v_codvend INTEGER;
    v_codprod INTEGER;
    v_vlrunit NUMERIC;
    v_qtd INTEGER;
    v_vlrtot NUMERIC;
    v_vlrnota NUMERIC;
    v_dtneg TIMESTAMP;
    v_numnota INTEGER := 1000;
    v_seq INTEGER;
    v_num_itens INTEGER;
    v_i INTEGER;
    v_j INTEGER;
    v_skip BOOLEAN;
    v_rand FLOAT;
BEGIN
    -- FEVEREIRO: 160 pedidos
    FOR v_i IN 1..160 LOOP
        v_codparc := 1 + floor(random() * 50)::int;
        v_codvend := 1 + floor(random() * 10)::int;
        v_dtneg := '2026-02-01'::timestamp + (floor(random() * 27) || ' days')::interval
                   + (floor(random() * 10 + 8) || ' hours')::interval;
        v_numnota := v_numnota + 1;
        v_vlrnota := 0;
        v_num_itens := 2 + floor(random() * 4)::int;

        INSERT INTO "TGFCAB" ("NUMNOTA", "CODPARC", "CODVEND", "CODTIPOPER", "DTNEG", "DTFATUR", "VLRNOTA", "STATUSNOTA", "CODEMP")
        VALUES (v_numnota, v_codparc, v_codvend, 1001, v_dtneg, v_dtneg + interval '1 day', 0, 'L', 1)
        RETURNING "NUNOTA" INTO v_nunota;

        FOR v_j IN 1..v_num_itens LOOP
            v_codprod := 1 + floor(random() * 100)::int;
            SELECT "VLRVENDA" INTO v_vlrunit FROM "TGFPRO" WHERE "CODPROD" = v_codprod;
            IF v_vlrunit IS NULL THEN v_vlrunit := 300; END IF;
            v_vlrunit := v_vlrunit * (0.85 + random() * 0.15);
            v_qtd := 1 + floor(random() * 15)::int;
            v_vlrtot := round((v_qtd * v_vlrunit)::numeric, 2);
            v_vlrnota := v_vlrnota + v_vlrtot;

            INSERT INTO "TGFITE" ("NUNOTA", "SEQUENCIA", "CODPROD", "QTDNEG", "VLRUNIT", "VLRTOT", "VLRDESC")
            VALUES (v_nunota, v_j, v_codprod, v_qtd, round(v_vlrunit::numeric, 2), v_vlrtot, 0);
        END LOOP;

        UPDATE "TGFCAB" SET "VLRNOTA" = round(v_vlrnota::numeric, 2) WHERE "NUNOTA" = v_nunota;
    END LOOP;

    -- MARCO: 200 pedidos (melhor mes)
    FOR v_i IN 1..200 LOOP
        v_codparc := 1 + floor(random() * 50)::int;
        v_codvend := 1 + floor(random() * 10)::int;
        v_dtneg := '2026-03-01'::timestamp + (floor(random() * 30) || ' days')::interval
                   + (floor(random() * 10 + 8) || ' hours')::interval;
        v_numnota := v_numnota + 1;
        v_vlrnota := 0;
        v_num_itens := 2 + floor(random() * 4)::int;

        INSERT INTO "TGFCAB" ("NUMNOTA", "CODPARC", "CODVEND", "CODTIPOPER", "DTNEG", "DTFATUR", "VLRNOTA", "STATUSNOTA", "CODEMP")
        VALUES (v_numnota, v_codparc, v_codvend, 1001, v_dtneg, v_dtneg + interval '1 day', 0, 'L', 1)
        RETURNING "NUNOTA" INTO v_nunota;

        FOR v_j IN 1..v_num_itens LOOP
            v_codprod := 1 + floor(random() * 100)::int;
            SELECT "VLRVENDA" INTO v_vlrunit FROM "TGFPRO" WHERE "CODPROD" = v_codprod;
            IF v_vlrunit IS NULL THEN v_vlrunit := 300; END IF;
            v_vlrunit := v_vlrunit * (0.85 + random() * 0.15);
            v_qtd := 1 + floor(random() * 15)::int;
            v_vlrtot := round((v_qtd * v_vlrunit)::numeric, 2);
            v_vlrnota := v_vlrnota + v_vlrtot;

            INSERT INTO "TGFITE" ("NUNOTA", "SEQUENCIA", "CODPROD", "QTDNEG", "VLRUNIT", "VLRTOT", "VLRDESC")
            VALUES (v_nunota, v_j, v_codprod, v_qtd, round(v_vlrunit::numeric, 2), v_vlrtot, 0);
        END LOOP;

        UPDATE "TGFCAB" SET "VLRNOTA" = round(v_vlrnota::numeric, 2) WHERE "NUNOTA" = v_nunota;
    END LOOP;

    -- ABRIL (1-7): ~80 pedidos com queda para vendedores 1,2,3 e sem clientes 41-50
    FOR v_i IN 1..120 LOOP
        v_codvend := 1 + floor(random() * 10)::int;
        v_skip := false;

        -- Vendedores 1,2,3: skip ~35% dos pedidos (queda)
        IF v_codvend IN (1, 2, 3) AND random() < 0.35 THEN
            v_skip := true;
        END IF;
        -- Vendedores 4,5: skip ~20% (queda leve)
        IF v_codvend IN (4, 5) AND random() < 0.20 THEN
            v_skip := true;
        END IF;

        IF NOT v_skip THEN
            -- Clientes 41-50 nao compram em abril
            LOOP
                v_codparc := 1 + floor(random() * 50)::int;
                EXIT WHEN v_codparc < 41;
            END LOOP;

            v_dtneg := '2026-04-01'::timestamp + (floor(random() * 6) || ' days')::interval
                       + (floor(random() * 10 + 8) || ' hours')::interval;
            v_numnota := v_numnota + 1;
            v_vlrnota := 0;
            v_num_itens := 2 + floor(random() * 4)::int;

            INSERT INTO "TGFCAB" ("NUMNOTA", "CODPARC", "CODVEND", "CODTIPOPER", "DTNEG", "DTFATUR", "VLRNOTA", "STATUSNOTA", "CODEMP")
            VALUES (v_numnota, v_codparc, v_codvend, 1001, v_dtneg, v_dtneg + interval '1 day', 0, 'L', 1)
            RETURNING "NUNOTA" INTO v_nunota;

            FOR v_j IN 1..v_num_itens LOOP
                v_codprod := 1 + floor(random() * 100)::int;
                SELECT "VLRVENDA" INTO v_vlrunit FROM "TGFPRO" WHERE "CODPROD" = v_codprod;
                IF v_vlrunit IS NULL THEN v_vlrunit := 300; END IF;
                v_vlrunit := v_vlrunit * (0.85 + random() * 0.15);
                v_qtd := 1 + floor(random() * 15)::int;
                v_vlrtot := round((v_qtd * v_vlrunit)::numeric, 2);
                v_vlrnota := v_vlrnota + v_vlrtot;

                INSERT INTO "TGFITE" ("NUNOTA", "SEQUENCIA", "CODPROD", "QTDNEG", "VLRUNIT", "VLRTOT", "VLRDESC")
                VALUES (v_nunota, v_j, v_codprod, v_qtd, round(v_vlrunit::numeric, 2), v_vlrtot, 0);
            END LOOP;

            UPDATE "TGFCAB" SET "VLRNOTA" = round(v_vlrnota::numeric, 2) WHERE "NUNOTA" = v_nunota;
        END IF;
    END LOOP;
END $$;

-- Verificacao final
SELECT 'TGFPAR' AS tabela, COUNT(*) AS total FROM "TGFPAR"
UNION ALL SELECT 'TGFVEND', COUNT(*) FROM "TGFVEND"
UNION ALL SELECT 'TGFPRO', COUNT(*) FROM "TGFPRO"
UNION ALL SELECT 'TGFCAB', COUNT(*) FROM "TGFCAB"
UNION ALL SELECT 'TGFITE', COUNT(*) FROM "TGFITE";

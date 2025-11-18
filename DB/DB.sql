-- DROPS DE TABLAS Y PROCEDURES POR SEGURIDAD
DROP TABLE IF EXISTS USUARIO;
DROP TABLE IF EXISTS PRODUCTO;
DROP TABLE IF EXISTS MENU;
DROP PROCEDURE IF EXISTS trgInsIdProducto;
DROP PROCEDURE IF EXISTS trUpdIdProducto;


CREATE TABLE IF NOT EXISTS USUARIO (
    idUsuario VARCHAR(25) PRIMARY KEY,
    usuario VARCHAR(25) NOT NULL UNIQUE,
    contrasen VARCHAR(30) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS PRODUCTO (
    idProducto VARCHAR(30) PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    imagen VARCHAR(100) NOT NULL,
    descripcion VARCHAR(150) NOT NULL,
    CONSTRAINT chk_precio CHECK (precio > 0)
);


CREATE TABLE IF NOT EXISTS TIPO_COMIDA (
    idTipo INTEGER PRIMARY KEY,
    nombre VARCHAR(25) NOT NULL,
    CONSTRAINT chk_id CHECK (idTipo BETWEEN 1 AND 5)
);

INSERT INTO TIPO_COMIDA (idTipo, nombre) VALUES
(1, 'Desayuno'),
(2, 'Almuerzo'),
(3, 'Cena'),
(4, 'Bebidas'),
(5, 'Postres');

CREATE TABLE IF NOT EXISTS MENU_DIA (
    idDiaMenu INTEGER PRIMARY KEY,
    nombreDia VARCHAR(15) NOT NULL,
    CONSTRAINT chk_idDiaMenu CHECK (idDiaMenu BETWEEN 1 AND 7)
);

INSERT INTO MENU_DIA (idDiaMenu, nombreDia) VALUES
(1, 'Lunes'),
(2, 'Martes'),
(3, 'Miercoles'),
(4, 'Jueves'),
(5, 'Viernes'),
(6, 'Sabado'),
(7, 'Domingo');


-- INSERTAR USUARIO ADMINISTRADOR
INSERT INTO USUARIO (idUsuario, usuario, contrasen, nombre) VALUES
('USR001', 'admin', '123', 'Administrador');


-- TABLA RELACION MENU-PRODUCTO-DIA
CREATE TABLE IF NOT EXISTS MENU_PRODUCTO (
    idMenuProducto SERIAL PRIMARY KEY,
    idProducto VARCHAR(30) NOT NULL,
    idTipo INTEGER NOT NULL,
    idDiaMenu INTEGER NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto) ON DELETE CASCADE,
    FOREIGN KEY (idTipo) REFERENCES TIPO_COMIDA(idTipo),
    FOREIGN KEY (idDiaMenu) REFERENCES MENU_DIA(idDiaMenu),
    UNIQUE(idProducto, idTipo, idDiaMenu)
);

-- TABLA EXCEPCIONES DE MENU (Promociones y descuentos especiales)
CREATE TABLE IF NOT EXISTS MENU_EXCEPCION (
    idExcepcion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    descuento_porcentaje DECIMAL(5,2) DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT chk_descuento CHECK (descuento_porcentaje BETWEEN 0 AND 100),
    CONSTRAINT chk_fechas CHECK (fecha_fin >= fecha_inicio)
);

-- TABLA PRODUCTOS EN EXCEPCIONES
CREATE TABLE IF NOT EXISTS EXCEPCION_PRODUCTO (
    idExcepcionProducto SERIAL PRIMARY KEY,
    idExcepcion INTEGER NOT NULL,
    idProducto VARCHAR(30) NOT NULL,
    precio_especial DECIMAL(10,2),
    FOREIGN KEY (idExcepcion) REFERENCES MENU_EXCEPCION(idExcepcion) ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto) ON DELETE CASCADE,
    UNIQUE(idExcepcion, idProducto)
);


-- TRIGGER PARA CREAR IDPRODUCTO AUTOMATICO

CREATE OR REPLACE FUNCTION generar_id_producto()
RETURNS TRIGGER AS $$
DECLARE 
    anno INTEGER;
BEGIN
    anno := EXTRACT(YEAR FROM CURRENT_DATE);
    NEW.idProducto := CONCAT('PROD', anno, NEW.nombre);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trgInsIdProducto
BEFORE INSERT ON PRODUCTO
FOR EACH ROW
EXECUTE FUNCTION generar_id_producto();

CREATE TRIGGER trUpdIdProducto
BEFORE UPDATE ON PRODUCTO
FOR EACH ROW
EXECUTE FUNCTION generar_id_producto();


-- INSERTAR PRODUCTOS DEL RESTAURANTE
-- Desactivar triggers temporalmente para insertar con IDs específicos
ALTER TABLE PRODUCTO DISABLE TRIGGER trgInsIdProducto;
ALTER TABLE PRODUCTO DISABLE TRIGGER trUpdIdProducto;

-- PRODUCTOS ORGANIZADOS POR TIPO DE COMIDA
INSERT INTO PRODUCTO (idProducto, nombre, precio, imagen, descripcion) VALUES
-- Desayunos
('PROD2025CaféAmericano', 'Café Americano', 6000, 'cafe.jpg', 'Café premium colombiano'),
('PROD2025Cappuccino', 'Cappuccino', 8000, 'cappuccino.jpg', 'Espresso con leche vaporizada'),
('PROD2025TéChaiLatte', 'Té Chai Latte', 9000, 'chai.jpg', 'Té especiado con leche y canela'),
('PROD2025JugoNatural', 'Jugo Natural', 8000, 'jugo.jpg', 'Naranja, manzana, fresa o mango'),
('PROD2025PandeAjo', 'Pan de Ajo', 7000, 'pan_ajo.jpg', 'Pan tostado con mantequilla y ajo'),
('PROD2025ChurrosconChocolate', 'Churros con Chocolate', 11000, 'churros.jpg', 'Churros recién hechos con chocolate caliente'),

-- Almuerzos
('PROD2025ChurrascoPremium', 'Churrasco Premium', 45000, 'churrasco.jpg', '500g de carne con papas y ensalada'),
('PROD2025SalmónGrillado', 'Salmón Grillado', 38000, 'salmon.jpg', 'Con vegetales salteados y arroz'),
('PROD2025PaellaValenciana', 'Paella Valenciana', 35000, 'paella.jpg', 'Arroz con mariscos y pollo'),
('PROD2025LasañaBoloñesa', 'Lasaña Boloñesa', 32000, 'lasagna.jpg', 'Pasta, carne, bechamel y queso gratinado'),
('PROD2025CostillasBBQ', 'Costillas BBQ', 40000, 'costillas.jpg', 'Costillas a la parrilla con salsa BBQ'),
('PROD2025PolloalaParrilla', 'Pollo a la Parrilla', 25000, 'pollo_parrilla.jpg', 'Pechuga marinada con hierbas'),
('PROD2025SteakArgentino', 'Steak Argentino', 50000, 'steak.jpg', '500g de carne de res premium'),
('PROD2025EnsaladaCésar', 'Ensalada César', 18000, 'cesar.jpg', 'Lechuga, pollo, crutones y parmesano'),
('PROD2025ArrozBlanco', 'Arroz Blanco', 6000, 'arroz.jpg', 'Arroz jazmín cocido'),
('PROD2025PapasFrancesas', 'Papas Francesas', 8000, 'papas_francesas.jpg', 'Papas crujientes con sal de mar'),

-- Cenas
('PROD2025PizzaMargherita', 'Pizza Margherita', 24000, 'pizza_margherita.jpg', 'Tomate, mozzarella, albahaca fresca'),
('PROD2025PizzaPepperoni', 'Pizza Pepperoni', 26000, 'pizza_pepperoni.jpg', 'Pepperoni, mozzarella y orégano'),
('PROD2025HamburguesaGourmet', 'Hamburguesa Gourmet', 28000, 'hamburguesa.jpg', 'Carne angus, queso brie, rúgula y tomate'),
('PROD2025PastaCarbonara', 'Pasta Carbonara', 22000, 'carbonara.jpg', 'Pasta con bacon, crema y parmesano'),
('PROD2025FiletedePescado', 'Filete de Pescado', 30000, 'filete_pescado.jpg', 'Con salsa de limón y vegetales'),
('PROD2025PechugaRellena', 'Pechuga Rellena', 32000, 'pechuga_rellena.jpg', 'Pechuga rellena de jamón y queso'),
('PROD2025RaviolesdeRicotta', 'Ravioles de Ricotta', 28000, 'ravioles.jpg', 'Ravioles caseros con salsa boloñesa'),
('PROD2025AlitasBuffalo', 'Alitas Buffalo', 18000, 'alitas.jpg', '8 alitas picantes con salsa ranch'),

-- Bebidas
('PROD2025LimonadaNatural', 'Limonada Natural', 7000, 'limonada.jpg', 'Limón fresco con hierbabuena'),
('PROD2025Coca-Cola', 'Coca-Cola', 5000, 'coca_cola.jpg', '350ml - Regular o Zero'),
('PROD2025AguaconGas', 'Agua con Gas', 4000, 'agua_gas.jpg', '500ml - San Pellegrino'),
('PROD2025TéHelado', 'Té Helado', 7000, 'te_helado.jpg', 'Té refrescante con limón'),
('PROD2025CervezaNacional', 'Cerveza Nacional', 8000, 'cerveza_nacional.jpg', 'Poker, Águila o Club Colombia'),
('PROD2025VinoTinto', 'Vino Tinto', 15000, 'vino_tinto.jpg', 'Copa de vino tinto reserva'),
('PROD2025VinoBlanco', 'Vino Blanco', 15000, 'vino_blanco.jpg', 'Copa de vino blanco seco'),
('PROD2025MojitoClásico', 'Mojito Clásico', 18000, 'mojito.jpg', 'Ron, hierbabuena, limón y soda'),

-- Postres
('PROD2025Tiramisú', 'Tiramisú', 16000, 'tiramisu.jpg', 'Clásico postre italiano con café'),
('PROD2025CheesecakedeFrutos', 'Cheesecake de Frutos', 14000, 'cheesecake.jpg', 'Con salsa de frutos rojos'),
('PROD2025BrownieconHelado', 'Brownie con Helado', 12000, 'brownie.jpg', 'Brownie caliente con helado de vainilla'),
('PROD2025FlandeCaramelo', 'Flan de Caramelo', 10000, 'flan.jpg', 'Tradicional flan casero'),
('PROD2025TresLeches', 'Tres Leches', 11000, 'tres_leches.jpg', 'Torta húmeda con tres leches'),
('PROD2025HeladoArtesanal', 'Helado Artesanal', 8000, 'helado.jpg', 'Vainilla, chocolate o fresa - 2 bolas'),
('PROD2025TortadeChocolate', 'Torta de Chocolate', 13000, 'torta_chocolate.jpg', 'Torta húmeda con ganache');

-- Reactivar triggers
ALTER TABLE PRODUCTO ENABLE TRIGGER trgInsIdProducto;
ALTER TABLE PRODUCTO ENABLE TRIGGER trUpdIdProducto;


-- FUNCIÓN PARA ASIGNAR MENÚ AUTOMÁTICAMENTE POR DÍA
CREATE OR REPLACE FUNCTION asignar_menu_automatico()
RETURNS void AS $$
DECLARE
    productos_desayuno TEXT[] := ARRAY['Café Americano', 'Cappuccino', 'Té Chai Latte', 'Jugo Natural', 'Pan de Ajo', 'Churros con Chocolate'];
    productos_almuerzo TEXT[] := ARRAY['Churrasco Premium', 'Salmón Grillado', 'Paella Valenciana', 'Lasaña Boloñesa', 'Costillas BBQ', 'Pollo a la Parrilla', 'Steak Argentino'];
    productos_cena TEXT[] := ARRAY['Pizza Margherita', 'Pizza Pepperoni', 'Hamburguesa Gourmet', 'Pasta Carbonara', 'Filete de Pescado', 'Pechuga Rellena', 'Ravioles de Ricotta'];
    productos_bebidas TEXT[] := ARRAY['Limonada Natural', 'Coca-Cola', 'Agua con Gas', 'Té Helado', 'Cerveza Nacional', 'Vino Tinto', 'Vino Blanco', 'Mojito Clásico'];
    productos_postres TEXT[] := ARRAY['Tiramisú', 'Cheesecake de Frutos', 'Brownie con Helado', 'Flan de Caramelo', 'Tres Leches', 'Helado Artesanal', 'Torta de Chocolate'];
    
    dia_actual INTEGER;
    producto_nombre TEXT;
    producto_id VARCHAR(30);
BEGIN
    -- Limpiar asignaciones previas
    DELETE FROM MENU_PRODUCTO;
    
    -- TIPO 1: DESAYUNO - Todos los productos disponibles todos los días
    INSERT INTO MENU_PRODUCTO (idProducto, idTipo, idDiaMenu)
    SELECT p.idProducto, 1, d.idDiaMenu
    FROM PRODUCTO p
    CROSS JOIN MENU_DIA d
    WHERE p.nombre = ANY(productos_desayuno);
    
    -- TIPO 2: ALMUERZO - Rotar productos por día (cada día un plato diferente)
    FOR dia_actual IN 1..7 LOOP
        -- Asignar plato principal rotativo
        SELECT idProducto INTO producto_id
        FROM PRODUCTO
        WHERE nombre = productos_almuerzo[((dia_actual - 1) % array_length(productos_almuerzo, 1)) + 1];
        
        INSERT INTO MENU_PRODUCTO (idProducto, idTipo, idDiaMenu)
        VALUES (producto_id, 2, dia_actual);
        
        -- Agregar ensalada y acompañamientos (siempre disponibles)
        INSERT INTO MENU_PRODUCTO (idProducto, idTipo, idDiaMenu)
        SELECT idProducto, 2, dia_actual
        FROM PRODUCTO
        WHERE nombre IN ('Ensalada César', 'Papas Francesas', 'Arroz Blanco');
    END LOOP;
    
    -- TIPO 3: CENA - Rotar productos por día
    FOR dia_actual IN 1..7 LOOP
        SELECT idProducto INTO producto_id
        FROM PRODUCTO
        WHERE nombre = productos_cena[((dia_actual - 1) % array_length(productos_cena, 1)) + 1];
        
        INSERT INTO MENU_PRODUCTO (idProducto, idTipo, idDiaMenu)
        VALUES (producto_id, 3, dia_actual);
        
        -- Agregar acompañamiento si es pizza o hamburguesa
        IF dia_actual IN (1, 2, 4) THEN
            INSERT INTO MENU_PRODUCTO (idProducto, idTipo, idDiaMenu)
            SELECT idProducto, 3, dia_actual
            FROM PRODUCTO
            WHERE nombre = 'Alitas Buffalo';
        END IF;
    END LOOP;
    
    -- TIPO 4: BEBIDAS - Todas disponibles todos los días
    INSERT INTO MENU_PRODUCTO (idProducto, idTipo, idDiaMenu)
    SELECT p.idProducto, 4, d.idDiaMenu
    FROM PRODUCTO p
    CROSS JOIN MENU_DIA d
    WHERE p.nombre = ANY(productos_bebidas);
    
    -- TIPO 5: POSTRES - Todos disponibles todos los días
    INSERT INTO MENU_PRODUCTO (idProducto, idTipo, idDiaMenu)
    SELECT p.idProducto, 5, d.idDiaMenu
    FROM PRODUCTO p
    CROSS JOIN MENU_DIA d
    WHERE p.nombre = ANY(productos_postres);
    
END;
$$ LANGUAGE plpgsql;

-- EJECUTAR LA FUNCIÓN PARA ASIGNAR MENÚ INICIAL
SELECT asignar_menu_automatico();


-- INSERTAR EXCEPCIONES DE MENÚ (Promociones especiales)

-- Promoción 1: Lunes de Descuento en Carnes (20% descuento)
INSERT INTO MENU_EXCEPCION (nombre, descripcion, fecha_inicio, fecha_fin, descuento_porcentaje, activo) VALUES
('Lunes de Carnes', 'Todos los lunes 20% de descuento en carnes premium', '2025-11-01', '2025-12-31', 20, TRUE);

-- Asignar productos a la excepción
INSERT INTO EXCEPCION_PRODUCTO (idExcepcion, idProducto, precio_especial)
SELECT 1, idProducto, precio * 0.80
FROM PRODUCTO
WHERE nombre IN ('Churrasco Premium', 'Steak Argentino', 'Costillas BBQ');

-- Promoción 2: Martes de Pizzas (30% descuento)
INSERT INTO MENU_EXCEPCION (nombre, descripcion, fecha_inicio, fecha_fin, descuento_porcentaje, activo) VALUES
('Martes de Pizzas', 'Martes con 30% de descuento en todas las pizzas', '2025-11-01', '2025-12-31', 30, TRUE);

INSERT INTO EXCEPCION_PRODUCTO (idExcepcion, idProducto, precio_especial)
SELECT 2, idProducto, precio * 0.70
FROM PRODUCTO
WHERE nombre LIKE '%Pizza%';

-- Promoción 3: Miércoles de Mariscos (15% descuento)
INSERT INTO MENU_EXCEPCION (nombre, descripcion, fecha_inicio, fecha_fin, descuento_porcentaje, activo) VALUES
('Miércoles de Mariscos', 'Miércoles frescos con 15% en mariscos', '2025-11-01', '2025-12-31', 15, TRUE);

INSERT INTO EXCEPCION_PRODUCTO (idExcepcion, idProducto, precio_especial)
SELECT 3, idProducto, precio * 0.85
FROM PRODUCTO
WHERE nombre IN ('Salmón Grillado', 'Paella Valenciana', 'Filete de Pescado');

-- Promoción 4: Jueves de Pastas (25% descuento)
INSERT INTO MENU_EXCEPCION (nombre, descripcion, fecha_inicio, fecha_fin, descuento_porcentaje, activo) VALUES
('Jueves de Pastas', 'Jueves italiano con 25% en pastas', '2025-11-01', '2025-12-31', 25, TRUE);

INSERT INTO EXCEPCION_PRODUCTO (idExcepcion, idProducto, precio_especial)
SELECT 4, idProducto, precio * 0.75
FROM PRODUCTO
WHERE nombre IN ('Pasta Carbonara', 'Lasaña Boloñesa', 'Ravioles de Ricotta');

-- Promoción 5: Viernes Social (2x1 en bebidas alcohólicas)
INSERT INTO MENU_EXCEPCION (nombre, descripcion, fecha_inicio, fecha_fin, descuento_porcentaje, activo) VALUES
('Viernes Social', 'Viernes con 2x1 en bebidas alcohólicas', '2025-11-01', '2025-12-31', 50, TRUE);

INSERT INTO EXCEPCION_PRODUCTO (idExcepcion, idProducto, precio_especial)
SELECT 5, idProducto, precio * 0.50
FROM PRODUCTO
WHERE nombre IN ('Cerveza Nacional', 'Vino Tinto', 'Vino Blanco', 'Mojito Clásico');

-- Promoción 6: Fin de Semana Familiar (10% descuento en combos)
INSERT INTO MENU_EXCEPCION (nombre, descripcion, fecha_inicio, fecha_fin, descuento_porcentaje, activo) VALUES
('Fin de Semana Familiar', 'Sábados y domingos 10% en platos principales', '2025-11-01', '2025-12-31', 10, TRUE);

INSERT INTO EXCEPCION_PRODUCTO (idExcepcion, idProducto, precio_especial)
SELECT 6, idProducto, precio * 0.90
FROM PRODUCTO
WHERE nombre IN ('Hamburguesa Gourmet', 'Pollo a la Parrilla', 'Pechuga Rellena');

-- Promoción 7: Happy Hour Postres (20% descuento 3pm-6pm)
INSERT INTO MENU_EXCEPCION (nombre, descripcion, fecha_inicio, fecha_fin, descuento_porcentaje, activo) VALUES
('Happy Hour Postres', 'Todos los días de 3pm a 6pm: 20% en postres', '2025-11-01', '2025-12-31', 20, TRUE);

INSERT INTO EXCEPCION_PRODUCTO (idExcepcion, idProducto, precio_especial)
SELECT 7, idProducto, precio * 0.80
FROM PRODUCTO
WHERE nombre IN ('Tiramisú', 'Cheesecake de Frutos', 'Brownie con Helado', 'Tres Leches');



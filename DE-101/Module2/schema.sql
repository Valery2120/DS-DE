CREATE  TABLE customer ( 
	customer_id          integer  NOT NULL  ,
	customer_name        varchar(100)    ,
	CONSTRAINT pk_customer PRIMARY KEY ( customer_id )
 );

CREATE  TABLE date ( 
	order_date           date  NOT NULL  ,
	ship_date            date  NOT NULL  ,
	"year"               integer  NOT NULL  ,
	quater               integer  NOT NULL  ,
	"month"              integer  NOT NULL  ,
	week                 integer  NOT NULL  ,
	"day"                integer  NOT NULL  ,
	CONSTRAINT pk_date PRIMARY KEY ( order_date, ship_date )
 );

CREATE  TABLE location ( 
	location_id          integer  NOT NULL  ,
	country              varchar(15)    ,
	"state"              varchar(15)    ,
	region               varchar(10)    ,
	city                 varchar(15)    ,
	postal_code          integer    ,
	CONSTRAINT pk_tbl PRIMARY KEY ( location_id )
 );

CREATE  TABLE manager ( 
	manager_id           integer  NOT NULL  ,
	manager_name         varchar(100)    ,
	CONSTRAINT pk_manager PRIMARY KEY ( manager_id )
 );

CREATE  TABLE product ( 
	product_id           integer  NOT NULL  ,
	category             varchar    ,
	sub_category         varchar    ,
	product_name         varchar(100)    ,
	segment              varchar    ,
	CONSTRAINT pk_product PRIMARY KEY ( product_id )
 );

CREATE  TABLE returns ( 
	order_id             varchar  NOT NULL  ,
	returned             varchar    ,
	CONSTRAINT pk_tbl_0 PRIMARY KEY ( order_id )
 );

CREATE  TABLE shipping ( 
	shipping_id          integer  NOT NULL  ,
	ship_mode            varchar(15)    ,
	CONSTRAINT pk_shipping PRIMARY KEY ( shipping_id )
 );

CREATE  TABLE sales ( 
	row_id               integer  NOT NULL  ,
	order_id             varchar(15)  NOT NULL  ,
	sales                decimal  NOT NULL  ,
	quantity             integer  NOT NULL  ,
	discount             decimal    ,
	profit               decimal  NOT NULL  ,
	manager_id           integer  NOT NULL  ,
	location_id          integer  NOT NULL  ,
	customer_id          integer  NOT NULL  ,
	product_id           integer  NOT NULL  ,
	shipping_id          integer  NOT NULL  ,
	order_date           date  NOT NULL  ,
	ship_date            date  NOT NULL  ,
	CONSTRAINT pk_sales PRIMARY KEY ( row_id ),
	CONSTRAINT fk_sales_manager FOREIGN KEY ( manager_id ) REFERENCES manager( manager_id )   ,
	CONSTRAINT fk_sales_location FOREIGN KEY ( location_id ) REFERENCES "location"( location_id )   ,
	CONSTRAINT fk_sales_customer FOREIGN KEY ( customer_id ) REFERENCES customer( customer_id )   ,
	CONSTRAINT fk_sales_product FOREIGN KEY ( product_id ) REFERENCES product( product_id )   ,
	CONSTRAINT fk_sales_shipping FOREIGN KEY ( shipping_id ) REFERENCES shipping( shipping_id )   ,
	CONSTRAINT fk_sales_sales FOREIGN KEY ( order_id ) REFERENCES "returns"( order_id )   ,
	CONSTRAINT fk_sales_date FOREIGN KEY ( order_date, ship_date ) REFERENCES "date"( order_date, ship_date )   
 );

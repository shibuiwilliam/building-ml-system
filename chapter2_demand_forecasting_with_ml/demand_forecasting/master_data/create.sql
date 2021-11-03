CREATE TABLE IF NOT EXISTS regions (
	id VARCHAR(32) NOT NULL,
	name VARCHAR(255) NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (name)
);

CREATE INDEX IF NOT EXISTS idx_regions_name ON regions(name);

CREATE TABLE IF NOT EXISTS stores (
	id VARCHAR(32) NOT NULL,
    region_id VARCHAR(32) NOT NULL,
	name VARCHAR(255) NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (name),
    FOREIGN KEY(region_id) REFERENCES regions(id)
);

CREATE INDEX IF NOT EXISTS idx_stores_region_id ON stores(region_id);
CREATE INDEX IF NOT EXISTS idx_stores_name ON stores(name);

CREATE TABLE IF NOT EXISTS items (
	id VARCHAR(32) NOT NULL,
	name VARCHAR(255) NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (name)
);

CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);

CREATE TABLE IF NOT EXISTS item_prices (
	id VARCHAR(32) NOT NULL,
	item_id VARCHAR(32) NOT NULL,
    price INTEGER NOT NULL,
    applied_from DATE NOT NULL,
    applied_to DATE,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS idx_item_prices_applied_from ON item_prices(applied_from);
CREATE INDEX IF NOT EXISTS idx_item_prices_applied_to ON item_prices(applied_to);


CREATE TABLE IF NOT EXISTS item_sales (
	id VARCHAR(32) NOT NULL,
    date DATE NOT NULL,
    day_of_week VARCHAR(3) NOT NULL,
    store_id VARCHAR(32) NOT NULL,
	item_id VARCHAR(32) NOT NULL,
    item_price_id VARCHAR(32) NOT NULL,
    sales INTEGER NOT NULL,
    total_sales_amount INTEGER NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS idx_item_sales_date ON item_sales(date);
CREATE INDEX IF NOT EXISTS idx_item_sales_day_of_week ON item_sales(day_of_week);
CREATE INDEX IF NOT EXISTS idx_item_sales_store_id ON item_sales(store_id);
CREATE INDEX IF NOT EXISTS idx_item_sales_item_id ON item_sales(item_id);
CREATE INDEX IF NOT EXISTS idx_item_sales_item_price_id ON item_sales(item_price_id);
CREATE INDEX IF NOT EXISTS idx_item_sales_sales ON item_sales(sales);

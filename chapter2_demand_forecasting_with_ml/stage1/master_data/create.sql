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
	applied_to DATE NOT NULL DEFAULT DATE('2099-12-31'),
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(item_id) REFERENCES items(id)
);

CREATE INDEX IF NOT EXISTS idx_item_prices_item_id ON item_prices(item_id);

CREATE INDEX IF NOT EXISTS idx_item_prices_applied_from ON item_prices(applied_from);

CREATE INDEX IF NOT EXISTS idx_item_prices_applied_to ON item_prices(applied_to);

CREATE TABLE IF NOT EXISTS item_sales (
	id VARCHAR(32) NOT NULL,
	store_id VARCHAR(32) NOT NULL,
	item_id VARCHAR(32) NOT NULL,
	date DATE NOT NULL,
	day_of_week VARCHAR(3) NOT NULL,
	week_of_year INTEGER NOT NULL,
	sales INTEGER NOT NULL,
	total_sales_amount INTEGER NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(store_id) REFERENCES stores(id),
	FOREIGN KEY(item_id) REFERENCES items(id)
);

CREATE INDEX IF NOT EXISTS idx_item_sales_item_id ON item_sales(item_id);

CREATE INDEX IF NOT EXISTS idx_item_sales_sales ON item_sales(sales);

CREATE INDEX IF NOT EXISTS idx_item_sales_date ON item_sales(date);

CREATE INDEX IF NOT EXISTS idx_item_sales_day_of_week ON item_sales(day_of_week);

CREATE INDEX IF NOT EXISTS idx_item_sales_week_of_year ON item_sales(week_of_year);

CREATE INDEX IF NOT EXISTS idx_item_sales_store_id ON item_sales(store_id);

CREATE TABLE IF NOT EXISTS item_weekly_sales_predictions (
	id VARCHAR(32) NOT NULL,
	store_id VARCHAR(32) NOT NULL,
	item_id VARCHAR(32) NOT NULL,
	year INTEGER NOT NULL,
	week_of_year INTEGER NOT NULL,
	prediction NUMERIC NOT NULL,
	predicted_at DATE NOT NULL,
	version INTEGER NOT NULL DEFAULT 0,
	mlflow_experiment_id INTEGER NOT NULL,
	mlflow_run_id VARCHAR(64) NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(store_id) REFERENCES stores(id),
	FOREIGN KEY(item_id) REFERENCES items(id)
);

CREATE INDEX IF NOT EXISTS idx_item_weekly_sales_predictions_item_id ON item_weekly_sales_predictions(item_id);

CREATE INDEX IF NOT EXISTS idx_item_weekly_sales_predictions_store_id ON item_weekly_sales_predictions(store_id);

CREATE INDEX IF NOT EXISTS idx_item_weekly_sales_predictions_year ON item_weekly_sales_predictions(year);

CREATE INDEX IF NOT EXISTS idx_item_weekly_sales_predictions_week_of_year ON item_weekly_sales_predictions(week_of_year);

CREATE INDEX IF NOT EXISTS idx_item_weekly_sales_predictions_version ON item_weekly_sales_predictions(version);
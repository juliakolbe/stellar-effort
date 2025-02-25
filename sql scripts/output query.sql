create table output (
rocket_id INT primary key auto_increment,
fuel_left decimal(7, 2),
landing_eta int,
landing_distance decimal(10, 2),
velocity decimal(8,2),
acceleration decimal (8,2)
);
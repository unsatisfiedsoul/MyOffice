use my_app_db;
create table motor_list(id int not null auto_increment, motor_id varchar(100) not null, motor_name varchar(100) not null, hp varchar(50) not null, rpm varchar(50) not null, amp varchar(50) not null, section varchar(100) not null, primary key(id));
alter table motor_list add section varchar(100) not null;
select * from operator_data order by section,dcs_id;
select * from motor_list;
create table motor_list(id int not null auto_increment, motor_id varchar(100) not null, motor_name varchar(100) not null, hp varchar(50) not null, rpm varchar(50) not null, amp varchar(50) not null,updates date not null, section varchar(100) not null, primary key(id));
select * from operator_data order by dcs_id;
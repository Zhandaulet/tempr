drop table if exists places;

create table `places` ( 
  `id` int not null auto_increment,
  `city` varchar(20) DEFAULT NULL,
  `county` varchar(20) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
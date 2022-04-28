create table `people` (
  `id_people` int not null auto_increment,
  `given_name` varchar(80) default null,
  `family_name` varchar(80) default null,
  `date_of_birth` date default null,
  `place_id` int null,
  INDEX `idx_place_id` (`place_id`),
  FOREIGN KEY (`place_id`)
  REFERENCES `places`(`id`)
  on DELETE CASCADE,
  primary key (`id_people`)
);
CREATE DATABASE IF NOT EXISTS HHparser;
USE HHparser;

CREATE TABLE IF NOT EXISTS `resume` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `salary` varchar(55) DEFAULT NULL,
  `specialization` text,
  `busyness_mode` text,
  `work_schedule` text,
  `work_experience` text,
  `key_skills` text,
  `citizenship` text,
  `location` text,
  `job_search_status` text,
  `resume_link` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `vacancy` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `salary` varchar(255) DEFAULT NULL,
  `skills` text,
  `experience` varchar(255) DEFAULT NULL,
  `employment_mode` varchar(255) DEFAULT NULL,
  `description` text,
  `vacancy_link` text,
  `location` varchar(100) DEFAULT NULL,
  `employer` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

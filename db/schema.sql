create database `library`;


create table `library`.`Patron` (
  `patron_id`       int unsigned    not null auto_increment,
  `name`            varchar(50)     not null,
  -- max email len = 254 (http://stackoverflow.com/a/574698/700375)
  `email`           varchar(254)    null default null,
  `phone`           varchar(25)     null default null,
--`date_of_birth`   date            null default null,
  -- it would be great if MySQL had CHECK constraints so I could verify no user
  -- has a password without a salt... too bad we're using MySQL like a bunch of
  -- yammering dogs on a speedboat, instead of PostgreSQL like the advanced,
  -- spacefaring civ we truly are
--`password`        char(64)        null default null,
--`salt`            char(16)        null default null,

constraint "Patron_pk"
    primary key (`patron_id`)
);


create table `library`.`Creation` (
  `creation_id`     int unsigned        not null auto_increment,
  `main_title`      varchar(4000)       not null,
  `release_year`    smallint unsigned   null default null,

constraint "Creation_pk"
    primary key (`creation_id`)
);


create table `library`.`CreationAttribute` (
  `creation_attribute_id`   int unsigned    not null auto_increment,
  `name`                    varchar(100)    not null,
  `help_text`               TEXT            null default null,

constraint "CreationAttribute_pk"
    primary key (`creation_attribute_id`)
);


-- A well-recognized problem for library databases is the sheer complexity of
-- bilbiographic data (see the MARC and BIBFRAME standards). Necessary details
-- for a given work may vary widely between any given set of works. In addition,
-- attempting to determine every possible attribute ahead of time is a herculean
-- task beyond the scope of this project. Therefore, I am implementing a
-- semi-structured entity-attribute-value data model which allows admins to
-- define custom attributes as needed. This allows the
create table `library.CreationAV` (
  `creation_attribute_id`   int unsigned    not null,
  `creation_id`             int unsigned    not null,
  `attribute_value`         varchar(1000)   not null,

constraint "CreationAV_pk"
    primary key (`creation_attribute_id`, `creation_id`),
constraint "CreationAV_CreationAttribute_fk"
    foreign key (`creation_attribute_id`)
    references `CreationAttribute` (`creation_attribute_id`),
constraint "CreationAV_Creation_fk"
    foreign key (`creation_id`)
    references `Creation` (`creation_id`)
);


-- Any entity that is authoritative over a given work. For example, an authority
-- could be an author, publisher, editor, translator, producer, recording
-- artist, or record label, amongst other things.
-- In an ideal implementation, there would be a means for adding semi-structured
-- data to an Authority, such as a JSON-encoded field or an EAV model.
create table `library`.`Authority` (
  `authority_id`    int unsigned                    not null auto_increment,
  `name`            varchar(4000)                   not null,
  `type`            ENUM('person', 'org', 'place')  not null,

constraint "Authority_pk"
    primary key (`authority_id`)
);


create table `library`.`Role` (
  `role_id`         int unsigned    not null auto_increment,
  `name`            varchar(30)     not null,

constraint "Role_pk"
    primary key (`role_id`)
);


-- Glue table between works and authorities, with an additional FK to the
-- authority's role in the work. This allows for situations where an authority
-- takes on multiple roles, such as on the album "2001" by Dr. Dre, where Dre
-- is both the main credited artist and executive producer.
create table `library`.`CreationAuthority` (
  `creation_id`     int unsigned    not null,
  `authority_id`    int unsigned    not null,
  `role_id`         int unsigned    not null,

constraint "CreationAuthority_pk"
    primary key (`creation_id`, `authority_id`, `role_id`),
constraint "CreationAuthority_Creation_fk"
    foreign key (`creation_id`)
    references `Creation` (`creation_id`),
constraint "CreationAuthority_Authority_fk"
    foreign key (`authority_id`)
    references `Authority` (`authority_id`),
constraint "CreationAuthority_Role_fk"
    foreign key (`role_id`)
    references `Role` (`role_id`)
);


-- Creations may be classified by a standard list of subjects.
create table `library`.`Subject` (
  `subject_id`      int unsigned    not null auto_increment,
  `name`            varchar(250)    not null,

constraint "Subject_pk"
    primary key (`subject_id`)
);


-- Glue table for Creation and Subject, since multiple subjects may apply.
create table `library`.`CreationSubject` (
  `creation_id`     int unsigned    not null auto_increment,
  `subject`         int unsigned    not null,

constraint "CreationSubject_pk"
    primary key (`creation_id`, `subject`),
constraint "CreationSubject_Creation_fk"
    foreign key (`creation_id`)
    references `Creation` (`creation_id`),
constraint "CreationSubject_Subject_fk"
    foreign key (`subject`)
    references `Subject` (`subject_id`)
);


-- A resource is in a particular medium, such as CD, VHS, Book, Journal Article,
-- and so on.
create table `library`.`Medium` (
  `medium_id`       int unsigned    not null auto_increment,
  `name`            varchar(32)     not null,

constraint "Medium_pk"
    primary key (`medium_id`)
);


create table `library`.`Resource` (
  `resource_id`     int unsigned    not null auto_increment,
  `call_number`     varchar(32)     not null,
  `barcode`         varchar(100)    null default null,
  `creation_id`     int unsigned    not null,
  `medium`          int unsigned    not null,

constraint "Resource_pk"
    primary key (`resource_id`),
constraint "Resource_Creation_fk"
    foreign key (`creation_id`)
    references `Creation` (`creation_id`),
constraint "Resource_Medium_fk"
    foreign key (`medium`)
    references `Medium` (`medium_id`)
);


create table `library`.`Loan` (
  `out_date`        datetime        not null,
  `patron_id`       int unsigned    not null,
  `resource_id`     int unsigned    not null,
  `return_date`     datetime        null default null,
  `due_date`        date            null default null,

constraint "Loan_pk"
    primary key (`out_date`, `patron_id`, `resource_id`),
constraint "Loan_Patron_fk"
    foreign key (`patron_id`)
    references `Patron` (`patron_id`),
constraint "Loan_Resource_fk"
    foreign key (`resource_id`)
    references `Resource` (`resource_id`)
);


-- This table is used to keep track of people who have permissions to do things.
create table `library`.`Librarian` (
  `librarian_id`    int unsigned    not null auto_increment,
  `username`        varchar(35)     not null,
  `password`        char(64)        not null,
  `salt`            char(16)        not null,
  `user_level`      int             not null,

constraint "Librarian_pk"
    primary key (`librarian_id`)
);
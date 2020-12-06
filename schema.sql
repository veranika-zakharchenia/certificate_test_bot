CREATE TYPE certificate_statuses AS ENUM ('Valid', 'Invalid');
CREATE TABLE certificates (
    id  bigserial not null
        constraint certificate_id_pk
            primary key,
    status certificate_statuses default 'Valid' not null,
    name VARCHAR (255) not null unique,
    granted_user_id VARCHAR (255),
    issue_date TIMESTAMP,
    expiry_date TIMESTAMP not null
);

ALTER TABLE certificates OWNER TO certificates_owner;
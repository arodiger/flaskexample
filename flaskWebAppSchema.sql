
-- Table: public.webchat

-- DROP TABLE IF EXISTS public.webchat;

CREATE TABLE IF NOT EXISTS public.webchat
(
    username text COLLATE pg_catalog."default",
    message text COLLATE pg_catalog."default",
    time_stamp text COLLATE pg_catalog."default",
    loadhistory text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.webchat
    OWNER to arod;





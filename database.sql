-- 법령 정보를 저장하는 테이블
CREATE TABLE `law` (
    `id`                  BIGINT          NOT NULL AUTO_INCREMENT,
    `law_id`              VARCHAR(20)     NOT NULL,
    `law_name`            VARCHAR(255)    NOT NULL,
    `promulgation_number` VARCHAR(20)     NULL,
    `promulgation_date`   DATE            NULL,
    `effective_date`      DATE            NULL,
    `ministry_name`       VARCHAR(100)    NULL,
    `details`             JSON            NULL,
    `created_at`          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_law_id` (`law_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- 조문 정보를 저장하는 테이블
CREATE TABLE `article` (
    `id`               BIGINT          NOT NULL AUTO_INCREMENT,
    `law_id`           BIGINT          NOT NULL,
    `article_number`   VARCHAR(20)     NOT NULL,
    `article_title`    VARCHAR(255)    NULL,
    `content`          TEXT            NULL,
    `effective_date`   DATE            NULL,
    `created_at`       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_law_id` (`law_id`),
    CONSTRAINT `fk_article_law`
        FOREIGN KEY (`law_id`)
        REFERENCES `law` (`id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

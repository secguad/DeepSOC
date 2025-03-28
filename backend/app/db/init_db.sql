-- 创建数据库
CREATE DATABASE IF NOT EXISTS darkweb_monitor DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE darkweb_monitor;

-- 创建关键词表
CREATE TABLE IF NOT EXISTS keywords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(255) NOT NULL COMMENT '关键词',
    category VARCHAR(50) NOT NULL COMMENT '类别',
    risk_level VARCHAR(20) NOT NULL COMMENT '风险等级',
    description TEXT COMMENT '描述',
    created_by VARCHAR(50) NOT NULL COMMENT '创建人',
    created_at DATETIME NOT NULL COMMENT '创建时间',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新人',
    updated_at DATETIME NOT NULL COMMENT '更新时间',
    UNIQUE KEY uk_word (word)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='关键词表';

-- 创建告警表
CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    link VARCHAR(512) NOT NULL COMMENT '链接',
    type VARCHAR(50) NOT NULL COMMENT '类型',
    src_site VARCHAR(255) NOT NULL COMMENT '来源站点',
    date DATETIME NOT NULL COMMENT '日期',
    keywords VARCHAR(512) NOT NULL COMMENT '关键词',
    channel_id VARCHAR(50) NOT NULL COMMENT '渠道ID',
    channel_name VARCHAR(50) NOT NULL COMMENT '渠道名称',
    risk_level VARCHAR(20) NOT NULL COMMENT '风险等级',
    status VARCHAR(20) NOT NULL COMMENT '状态',
    processed_by VARCHAR(50) COMMENT '处理人',
    processed_at DATETIME COMMENT '处理时间',
    process_comment TEXT COMMENT '处理说明',
    INDEX idx_date (date),
    INDEX idx_status (status),
    INDEX idx_risk_level (risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='告警表'; 
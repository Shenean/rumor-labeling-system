CREATE TABLE IF NOT EXISTS samples (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '样本ID',
    content TEXT NOT NULL COMMENT '文本内容',
    source VARCHAR(100) COMMENT '来源平台或来源描述',
    language VARCHAR(20) DEFAULT 'zh' COMMENT '文本语言 (如 zh / en)',
    rumor_label VARCHAR(20) COMMENT '模型预测或自动标注标签 (真/假/待验证)',
    event_id INT COMMENT '关联事件ID (外键, 指向事件表)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='样本表';

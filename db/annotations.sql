CREATE TABLE IF NOT EXISTS annotations (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '标注记录ID',
    sample_id INT NOT NULL COMMENT '样本ID (外键, 指向样本表)',
    user_id INT NOT NULL COMMENT '用户ID (外键, 指向用户表, 标注者)',
    label VARCHAR(20) NOT NULL COMMENT '用户给出的标签',
    comment TEXT COMMENT '标注备注或说明',
    annotated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '标注时间',
    FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='标注记录表';

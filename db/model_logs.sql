CREATE TABLE IF NOT EXISTS model_logs (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
    model_name VARCHAR(50) COMMENT '模型名称或类型',
    input_data TEXT COMMENT '输入数据 (如样本文本或ID)',
    output_label VARCHAR(20) COMMENT '模型输出标签',
    confidence FLOAT COMMENT '模型输出置信度',
    user_id INT COMMENT '发起调用的用户ID (外键, 可选)',
    called_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '调用时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模型调用日志表';

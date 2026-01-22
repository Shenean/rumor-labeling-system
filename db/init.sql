-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '登录用户名 (唯一)',
    password_hash VARCHAR(128) NOT NULL COMMENT '密码哈希值',
    email VARCHAR(100) COMMENT '邮件地址 (可选)',
    role VARCHAR(20) DEFAULT 'annotator' COMMENT '用户角色 (如 admin / annotator)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 事件表
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '事件ID',
    title VARCHAR(200) COMMENT '事件标题或主题',
    description TEXT COMMENT '事件描述 (可选)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='事件表';

-- 样本表
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

-- 任务表
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '任务ID',
    name VARCHAR(100) NOT NULL COMMENT '任务名称',
    description TEXT COMMENT '任务描述',
    assignee_id INT COMMENT '指派执行用户ID (外键, 选填)',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '任务状态 (如 pending / done)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (assignee_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务表';

-- 标注记录表
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

-- 模型调用日志表
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

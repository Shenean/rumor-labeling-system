为了完整实现前端项目，我将按照以下步骤进行构建，引入 `Element Plus` 作为 UI 组件库以加快开发速度并保证界面专业性。

### 1. 基础依赖与环境配置
*   **安装依赖**：安装 `element-plus`, `@element-plus/icons-vue` (图标库), `sass` (样式预处理)。
*   **全局配置**：在 `main.ts` 中引入 Element Plus 和图标库。

### 2. 状态管理与路由设计
*   **User Store (`store/user.ts`)**：管理用户登录状态、Token、用户信息及权限角色。
*   **路由配置 (`router/index.ts`)**：
    *   配置 **路由守卫** (Navigation Guard)，实现登录拦截。
    *   定义 **动态路由** 结构，区分 "公共页面"（如登录）和 "后台布局页面"（Dashboard 等）。

### 3. 核心布局组件 (`layout/`)
*   实现后台管理系统的标准布局：
    *   **Sidebar**：侧边栏菜单，根据路由自动生成。
    *   **Navbar**：顶部导航，包含面包屑、语言切换、用户头像/登出。
    *   **AppMain**：内容渲染区域。

### 4. 业务模块页面实现 (`views/`)
我将为报告中提到的每个模块创建对应的页面文件，并实现核心 UI 逻辑：

*   **登录页 (`login/Login.vue`)**：账号密码表单，集成后端 JWT 登录接口。
*   **仪表盘 (`dashboard/Dashboard.vue`)**：展示统计卡片（模拟数据）。
*   **谣言检测 (`rumor/Detect.vue`)**：输入文本框、调用检测 API、结果展示区域。
*   **样本管理 (`sample/SampleList.vue`)**：表格展示样本，支持分页、搜索、删除。
*   **标注任务 (`annotation/`)**：
    *   `TaskList.vue`：任务列表。
    *   `Workspace.vue`：标注工作台（核心页面），包含文本展示和标签选择。
*   **事件聚合 (`event/EventList.vue`)**：事件列表与聚合操作。
*   **系统管理 (`system/UserList.vue`)**：用户管理表格。

### 5. API 服务封装 (`services/`)
*   拆分 API 模块：`auth.ts`, `rumor.ts`, `sample.ts`, `annotation.ts` 等，对应后端的 Blueprints。

### 6. 多语言配置 (`locales/`)
*   完善 `zh.json` 和 `en.json`，覆盖菜单和常用按钮文本。

请确认是否开始执行此构建计划？
<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>Total Samples</template>
          <div class="card-num">1,204</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>Pending Tasks</template>
          <div class="card-num">56</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>Detected Rumors</template>
          <div class="card-num text-danger">89</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>My Annotations</template>
          <div class="card-num text-success">342</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card header="Recent Activities">
          <el-timeline>
            <el-timeline-item timestamp="2023-10-01" placement="top">
              Event "Earthquake" created
            </el-timeline-item>
            <el-timeline-item timestamp="2023-09-30" placement="top">
              Batch import 200 samples
            </el-timeline-item>
            <el-timeline-item timestamp="2023-09-28" placement="top">
              User 'admin' logged in
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="System Status">
          <el-progress type="dashboard" :percentage="80" status="success">
            <template #default="{ percentage }">
              <span class="percentage-value">{{ percentage }}%</span>
              <span class="percentage-label">Model Accuracy</span>
            </template>
          </el-progress>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.card-num {
  font-size: 28px;
  font-weight: bold;
}
.text-danger { color: #f56c6c; }
.text-success { color: #67c23a; }
</style>

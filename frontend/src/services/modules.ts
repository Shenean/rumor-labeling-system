import api from './api'

export const authService = {
  login(data: any) {
    return api.post('/auth/login', data)
  },
  logout() {
    return api.post('/auth/logout')
  },
  getCurrentUser() {
    return api.get('/auth/user')
  },
  changePassword(data: any) {
    return api.put('/auth/change_password', data)
  }
}

export const sampleService = {
  getSamples(params?: any) {
    return api.get('/samples', { params })
  },
  createSample(data: any) {
    return api.post('/samples', data)
  },
  getSample(id: number) {
    return api.get(`/samples/${id}`)
  },
  updateSample(id: number, data: any) {
    return api.put(`/samples/${id}`, data)
  },
  deleteSample(id: number) {
    return api.delete(`/samples/${id}`)
  },
  batchImport(samples: any[]) {
    return api.post('/samples/batch_import', { samples })
  }
}

export const taskService = {
  getTasks(params?: any) {
    return api.get('/tasks', { params })
  },
  createTask(data: any) {
    return api.post('/tasks', data)
  },
  getTask(taskId: number) {
    return api.get(`/tasks/${taskId}`)
  },
  getTaskSamples(taskId: number) {
    return api.get(`/tasks/${taskId}/samples`)
  },
  claimTask(taskId: number) {
    return api.post(`/tasks/${taskId}/claim`)
  },
  unclaimTask(taskId: number) {
    return api.post(`/tasks/${taskId}/unclaim`)
  },
  getTaskProgress(taskId: number) {
    return api.get(`/tasks/${taskId}/progress`)
  }
}

export const annotationService = {
  submitAnnotation(data: any) {
    return api.post('/annotation/submit', data)
  },
  submitTaskSampleLabel(taskId: number, sampleId: number, data: any) {
    return api.post(`/tasks/${taskId}/samples/${sampleId}/label`, data)
  }
}

export const rumorService = {
  detect(text: string) {
    return api.post('/detect', { text })
  }
}

export const eventService = {
  getEvents(params?: any) {
    return api.get('/events', { params })
  },
  clusterEvents() {
    return api.post('/events/cluster')
  }
}

export const settingsService = {
  getConfig() {
    return api.get('/settings/config')
  },
  updateConfig(data: any) {
    return api.put('/settings/config', data)
  },
  getRoles() {
    return api.get('/settings/roles')
  },
  getUsers(params?: any) {
    return api.get('/settings/users', { params })
  },
  updateUserRoles(userId: number, roles: string[]) {
    return api.put(`/settings/users/${userId}/roles`, { roles })
  },
  getLogs(params?: any) {
    return api.get('/settings/logs', { params })
  }
}

export const exportService = {
  exportSamples() {
    return api.get('/export/samples', { responseType: 'blob' as any })
  },
  exportAnnotations(params?: any) {
    return api.get('/export/annotations', { params, responseType: 'blob' as any })
  },
  exportAudits() {
    return api.get('/export/audits', { responseType: 'blob' as any })
  },
  exportReports(data: any) {
    return api.post('/export/reports', data, { responseType: 'blob' as any })
  }
}

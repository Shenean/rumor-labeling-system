import api from './api'

export const authService = {
  login(data: any) {
    // Mock login for now, replace with api.post('/users/login', data)
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: {
            token: 'mock-token-12345',
            user: {
              id: 1,
              username: data.username,
              role: data.username === 'admin' ? 'admin' : 'annotator'
            }
          }
        })
      }, 500)
    })
  }
}

export const sampleService = {
  getSamples(params?: any) {
    return api.get('/samples', { params })
  },
  createSample(data: any) {
    return api.post('/samples', data)
  },
  updateSample(id: number, data: any) {
    return api.put(`/samples/${id}`, data)
  },
  deleteSample(id: number) {
    return api.delete(`/samples/${id}`)
  }
}

export const taskService = {
  getTasks(params?: any) {
    return api.get('/annotation/tasks', { params })
  },
  createTask(data: any) {
    return api.post('/annotation/tasks', data)
  }
}

export const annotationService = {
  submitAnnotation(data: any) {
    return api.post('/annotation/submit', data)
  }
}

export const rumorService = {
  detect(text: string) {
    return api.post('/rumor/detect', { text })
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

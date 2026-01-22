import unittest

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.config import TestingConfig
from app.models import User, Sample


class SmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            admin = User(username='admin', password_hash=generate_password_hash('admin123'), role='admin')
            annotator = User(username='annotator', password_hash=generate_password_hash('annotator123'), role='annotator')
            reviewer = User(username='reviewer', password_hash=generate_password_hash('reviewer123'), role='reviewer')
            db.session.add_all([admin, annotator, reviewer])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _login(self, username, password):
        res = self.client.post('/api/auth/login', json={'username': username, 'password': password})
        self.assertEqual(res.status_code, 200)
        return res.get_json()['data']['token']

    def test_end_to_end_flow(self):
        admin_token = self._login('admin', 'admin123')
        annotator_token = self._login('annotator', 'annotator123')
        reviewer_token = self._login('reviewer', 'reviewer123')

        res = self.client.post(
            '/api/samples',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'content': 'test rumor sample', 'source': 'unit-test', 'language': 'zh'}
        )
        self.assertEqual(res.status_code, 201)

        with self.app.app_context():
            sample_id = Sample.query.first().id

        res = self.client.post(
            '/api/tasks',
            headers={'Authorization': f'Bearer {admin_token}'},
            json={'name': 'task1', 'description': 'desc', 'sample_ids': [sample_id], 'assignees': [2]}
        )
        self.assertEqual(res.status_code, 201)
        task_id = res.get_json()['data']['id']

        res = self.client.get('/api/tasks', headers={'Authorization': f'Bearer {annotator_token}'})
        self.assertEqual(res.status_code, 200)

        res = self.client.get(f'/api/tasks/{task_id}/samples', headers={'Authorization': f'Bearer {annotator_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(isinstance(res.get_json()['data'], list))

        res = self.client.post(
            f'/api/tasks/{task_id}/samples/{sample_id}/label',
            headers={'Authorization': f'Bearer {annotator_token}'},
            json={'label': 'Rumor', 'comments': 'test'}
        )
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/api/review/tasks', headers={'Authorization': f'Bearer {reviewer_token}'})
        self.assertEqual(res.status_code, 200)

        res = self.client.post(
            f'/api/review/tasks/{task_id}',
            headers={'Authorization': f'Bearer {reviewer_token}'},
            json={'approved': True, 'comments': 'ok'}
        )
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/api/export/annotations', headers={'Authorization': f'Bearer {admin_token}'})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.headers.get('Content-Type', '').startswith('application/vnd.openxmlformats-officedocument'))


if __name__ == '__main__':
    unittest.main()


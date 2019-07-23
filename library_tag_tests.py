# from django.contrib.auth.models import Group, User
from django.test import TestCase

from tastypie.test import ResourceTestCaseMixin

from workbench.models import Tag
from workbench.models import Dataset

from services.databricks.models import Library
from workbench.models import FunctionalArea

class LibraryManagementTest(ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super(LibraryManagementTest, self).setUp()
        demo_data = {
            "name": "test-library-",
            "path": "https://nexus.devops.amgen.com/repository/gcoanalytics_pypi/simple",
            "description": "sample desc",
            "is_active": True,
            "library_mode": "internal",
            "library_type": "pypi"
        }
        for i in range(1, 6):
            demo_data['name'] = demo_data['name'] + str(i)
            Library.objects.create(**demo_data)

    def test_login_page(self):
        res = self.api_client.get('/login/?next=/landing/')
        self.assertEquals(res.status_code, 200)

    def test_add_library(self):
        url = '/api/v1/manage/library/add'
        data = {
            "description": "sample desc",
            "internal": "on",
            "lib_type": "internal",
            "name": "test-library",
            "path": "https://nexus.devops.amgen.com/repository/gcoanalytics_pypi/simple",
            "role": "functional_admin",
            "type": "pypi"
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 200)

    def test_add_library_name_dublicate(self):
        url = '/api/v1/manage/library/add'
        data = {
            "description": "sample description",
            "internal": "on",
            "lib_type": "internal",
            "name": "test-library-1",
            "path": "https://nexus.devops.amgen.com/repository/gcoanalytics_pypi/simple",
            "role": "functional_admin",
            "type": "pypi"
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 500)

    def test_add_library_name_required(self):
        url = '/api/v1/manage/library/add'
        data = {
            "description": "sample desc",
            "internal": "on",
            "lib_type": "internal",
            "path": "https://nexus.devops.amgen.com/repository/gcoanalytics_pypi/simple",
            "role": "functional_admin",
            "type": "pypi"
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 400)

    def test_add_library_description_required(self):
        url = '/api/v1/manage/library/add'
        data = {
            "internal": "on",
            "lib_type": "internal",
            "name": "test-library-2",
            "path": "testing",
            "role": "functional_admin",
            "type": "pypi"
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 400)

    def test_add_library_path_required(self):
        url = '/api/v1/manage/library/add'
        data = {
            "description": "sample desc",
            "internal": "on",
            "lib_type": "internal",
            "name": "test-library-path",
            "role": "functional_admin",
            "type": "pypi"
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 400)

    def test_edit_library(self):
        lib = Library.objects.first()
        url = '/api/v1/manage/library'
        data = {
            "lib_type": "internal",
            "library_id": lib.id,
            "description": "testing",
            "internal": "on",
            "role": "functional_admin",
            "path": "https://nexus.devops.amgen.com/repository/gcoanalytics_pypi/simple",
            "type": "pypi",
            "name": lib.name
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 200)


class TagTestManagement(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(TagTestManagement, self).setUp()
        demo_data1 = {
            'name': 'test_tag-',
            'color': 'rgb(104,56,79)',
            'description': 'Demo Description',
            'is_active': True
        }
        for i in range(1, 6):
            demo_data1['name'] = 'test_tag-' + str(i)
            Tag.objects.create(**demo_data1)

    def test_add_tag(self):
        url = '/api/v1/manage/tag/add'
        data = {        	
            'color': 'rgb(104,63,172)',	
            'description': 'sample tag',
            'name': 'test_tag-12',
            'role': 'system_admin'
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 200)

    def test_add_tag_Null_values(self):
        url = '/api/v1/manage/tag/add'
        data = {
            'color': '',
            'description': '',
            'name': None,
            'role': ''
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 500)

    def test_add_tag_duplicate_values(self):
        url = '/api/v1/manage/tag/add'
        data = {
            'color': '',
            'description': 'sample tag ',
            'name': 'test_tag-3',
            'role': 'system_admin'
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 400)

    def test_edit_tag(self):
        url = '/api/v1/manage/tag'
        tag = Tag.objects.first()
        data = {        	
            'color': 'rgb(104,63,172)',	
            'description': 'sample updated description tag test',
            'tag_id': tag.id,
            'name': tag.name,
            'role': 'system_admin'
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 200)

    def test_add_tag_role_required(self):
        url = '/api/v1/manage/tag/add'
        data = {
            'color': 'rgb(103,23,67)',
            'description': 'sample tag description',
            'name': 'test_tag-8',
            'role': None
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 200)

    def test_add_tag_name_required(self):
        url = '/api/v1/manage/tag/add'
        data = {
            'color': 'rgb(103,23,67)',
            'description': 'sample tag description',
            'name': None,
            'role': 'system_admin'
        }
        res = self.api_client.post(url, format='json', data=data)
        self.assertEquals(res.status_code, 500)
